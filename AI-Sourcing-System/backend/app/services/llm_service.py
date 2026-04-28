"""
Sourcing System — LLM 服务层
封装 OpenAI / 本地 LLM 调用，支持 Agent 提示词管理
"""
import os
import json
import httpx
from typing import List, Dict, Any, Optional, AsyncGenerator
from dataclasses import dataclass

from ..core.config import get_settings

settings = get_settings()

@dataclass
class LLMMessage:
    role: str  # system / user / assistant
    content: str

class LLMService:
    """LLM 服务：支持 OpenAI API 和兼容接口"""
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY", "")
        self.base_url = settings.OPENAI_BASE_URL or "https://api.openai.com/v1"
        self.model = settings.LLM_MODEL
        self.temperature = settings.LLM_TEMPERATURE
        self.max_tokens = settings.LLM_MAX_TOKENS
        self.client = httpx.AsyncClient(timeout=120.0)
    
    async def chat(
        self,
        messages: List[LLMMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_mode: bool = False,
    ) -> str:
        """单次对话调用"""
        if not self.api_key:
            # Mock mode: 返回模拟响应
            return self._mock_response(messages)
        
        payload = {
            "model": self.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature or self.temperature,
            "max_tokens": max_tokens or self.max_tokens,
        }
        
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        try:
            resp = await self.client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f'{{"error": "LLM调用失败: {str(e)}"}}' if json_mode else f"LLM调用失败: {str(e)}"
    
    async def chat_stream(
        self,
        messages: List[LLMMessage],
        temperature: Optional[float] = None,
    ) -> AsyncGenerator[str, None]:
        """流式对话调用"""
        if not self.api_key:
            yield self._mock_response(messages)
            return
        
        payload = {
            "model": self.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature or self.temperature,
            "stream": True,
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        async with self.client.stream(
            "POST",
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
        ) as resp:
            async for line in resp.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                        delta = chunk["choices"][0]["delta"].get("content", "")
                        if delta:
                            yield delta
                    except:
                        pass
    
    def _mock_response(self, messages: List[LLMMessage]) -> str:
        """Mock mode：无API key时返回结构化模拟数据"""
        last_msg = messages[-1].content[:50] if messages else ""
        return json.dumps({
            "mock": True,
            "note": "未配置 OPENAI_API_KEY，返回模拟数据",
            "input_preview": last_msg,
            "mock_score": 6.5,
            "mock_recommendation": "proceed",
        }, ensure_ascii=False)
    
    # ───────────── Agent 专用提示词模板 ─────────────
    
    def build_system_prompt(self, agent_role: str, agent_name: str, sector: str = "") -> str:
        """构建Agent系统提示词"""
        base = f"""你是一个专业的风险投资{agent_role}，名字是{agent_name}。
你的任务是以严谨的机构投资视角分析项目，输出结构化评估。
请使用中文回答，保持专业、简洁、数据驱动。"""
        
        if sector:
            base += f"\n你专注的赛道是：{sector}。请用该赛道的专业视角分析。"
        
        return base
    
    def build_screening_prompt(self, signal_content: str, sector: str) -> List[LLMMessage]:
        """构建初筛提示词"""
        system = self.build_system_prompt("投资经理", "ScreeningAgent", sector)
        user = f"""请对以下投资信号进行初筛，判断是否有进一步分析的价值：

信号内容：
{signal_content}

请输出JSON格式：
{{
    "company_name": "识别出的公司名",
    "has_value": true/false,
    "reason": "判断理由（50字内）",
    "sector": "赛道",
    "stage_guess": "猜测阶段",
    "confidence": 0-1
}}"""
        return [LLMMessage("system", system), LLMMessage("user", user)]
    
    def build_dd_prompt(
        self,
        company_name: str,
        description: str,
        sector: str,
        web_data: str = "",
    ) -> List[LLMMessage]:
        """构建DD报告提示词"""
        system = self.build_system_prompt("投资经理", "DD-Agent", sector)
        user = f"""请为以下项目生成初步尽调报告：

公司名称：{company_name}
赛道：{sector}
简介：{description}

网络检索数据：
{web_data or "（暂无）"}

请输出JSON格式：
{{
    "tam": "TAM分析（含数据）",
    "sam": "SAM分析",
    "som": "SOM分析",
    "market_position": "竞争格局与市场身位",
    "team_summary": "团队背景",
    "investor_background": "历史投资人情况",
    "product_analysis": "产品/技术评估",
    "traction": "增长数据与里程碑",
    "moat": "护城河分析",
    "market_score": 0-10,
    "team_score": 0-10,
    "product_score": 0-10,
    "traction_score": 0-10,
    "moat_score": 0-10,
    "overall_score": 0-10,
    "recommendation": "proceed/abandon/watch",
    "conviction": 0-10,
    "key_risks": ["风险1", "风险2"]
}}"""
        return [LLMMessage("system", system), LLMMessage("user", user)]
    
    def build_risk_prompt(
        self,
        company_name: str,
        dd_report: Dict[str, Any],
    ) -> List[LLMMessage]:
        """构建风险分析提示词"""
        system = self.build_system_prompt("风控经理", "RiskControlAgent")
        user = f"""请对以下项目进行独立风险分析：

公司：{company_name}
DD报告摘要：
{json.dumps(dd_report, ensure_ascii=False, indent=2)[:3000]}

请输出JSON格式：
{{
    "market_risk": "市场风险分析",
    "team_risk": "团队风险分析",
    "financial_risk": "财务/融资风险",
    "regulatory_risk": "监管风险",
    "competitive_risk": "竞争风险",
    "execution_risk": "执行风险",
    "risk_level": 0-10,
    "red_flags": ["红旗1", "红旗2"],
    "mitigations": "风险缓释建议"
}}"""
        return [LLMMessage("system", system), LLMMessage("user", user)]
    
    def build_ic_prompt(
        self,
        company_name: str,
        sector: str,
        dd_report: Dict[str, Any],
        risk_report: Dict[str, Any],
        agent_persona: str = "generalist",
    ) -> List[LLMMessage]:
        """构建IC成员投票提示词
        原系统规则：6=proceed, 4=abandon（没有5分制）
        """
        system = self.build_system_prompt("投委会成员", f"IC-{agent_persona}")
        system += """\n\n投委会评分规则：
- 6分 = 明确推进 (proceed)
- 4分 = 明确放弃 (abandon)
- 没有5分制，避免模糊
- 加权平均得出最终分数"""
        
        user = f"""请对以下项目进行投委会投票：

公司：{company_name}
赛道：{sector}

DD报告：
{json.dumps(dd_report, ensure_ascii=False, indent=2)[:2000]}

风险报告：
{json.dumps(risk_report, ensure_ascii=False, indent=2)[:1500]}

请输出JSON格式：
{{
    "score": 0-10,
    "vote": "invest/pass/abstain",
    "reasoning": "投票理由（100字内）",
    "key_concerns": ["关注点1"],
    "key_strengths": ["亮点1"]
}}"""
        return [LLMMessage("system", system), LLMMessage("user", user)]

# 全局单例
_llm_service: Optional[LLMService] = None

def get_llm_service() -> LLMService:
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
