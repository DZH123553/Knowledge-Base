#!/usr/bin/env python3
"""
Morphos Job Matching Server
Calls Boss Zhipin real API to get actual job listings with jobIds
"""

import os
import json
import re
import random
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests

app = Flask(__name__, static_folder='.')
CORS(app)

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')
BOSS_COOKIE = ""

def load_config():
    global BOSS_COOKIE
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
            BOSS_COOKIE = cfg.get('boss_cookie', '')
    except:
        BOSS_COOKIE = ""

load_config()

BOSS_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://www.zhipin.com/',
    'X-Requested-With': 'XMLHttpRequest',
}

def boss_search(query: str, city: str = "101010100", page: int = 1, page_size: int = 15):
    """Search real jobs on Boss Zhipin"""
    if not BOSS_COOKIE:
        return {"error": "NO_COOKIE", "message": "Boss cookie not configured"}
    
    url = "https://www.zhipin.com/wapi/zpgeek/search/joblist.json"
    headers = {**BOSS_HEADERS, 'Cookie': BOSS_COOKIE}
    params = {
        "scene": "1",
        "query": query,
        "city": city,
        "page": str(page),
        "pageSize": str(page_size),
    }
    
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        data = resp.json()
        
        if data.get("code") != 0:
            return {"error": "API_ERROR", "message": data.get('message', 'Boss API error'), "raw": data}
        
        job_list = data.get("zpData", {}).get("jobList", [])
        formatted = []
        for job in job_list:
            formatted.append({
                "jobId": job.get("encryptJobId", ""),
                "securityId": job.get("securityId", ""),
                "jobName": job.get("jobName", ""),
                "company": job.get("brandName", ""),
                "salary": job.get("salaryDesc", ""),
                "city": job.get("cityName", ""),
                "district": job.get("areaDistrict", ""),
                "businessDistrict": job.get("businessDistrict", ""),
                "experience": job.get("jobExperience", ""),
                "degree": job.get("jobDegree", ""),
                "skills": job.get("skills", []),
                "welfare": job.get("welfareList", []),
                "bossName": job.get("bossName", ""),
                "bossTitle": job.get("bossTitle", ""),
                "companyScale": job.get("brandScaleName", ""),
                "companyStage": job.get("brandStageName", ""),
                "industry": job.get("brandIndustry", ""),
                "logo": job.get("brandLogo", ""),
                "detailLink": f"https://www.zhipin.com/job_detail/{job.get('encryptJobId', '')}.html",
                "chatLink": f"https://www.zhipin.com/job_detail/{job.get('encryptJobId', '')}.html",
            })
        return {"jobs": formatted, "total": data.get("zpData", {}).get("totalCount", 0)}
    
    except requests.exceptions.Timeout:
        return {"error": "TIMEOUT", "message": "请求超时，请重试"}
    except Exception as e:
        return {"error": "EXCEPTION", "message": str(e)}


def calculate_match_score(job, user_profile):
    """Score a real job against user profile (0-100)"""
    score = 45  # Base score
    reasons = []
    
    user_skills = [s.lower() for s in user_profile.get("skills", [])]
    job_skills = [s.lower() for s in job.get("skills", [])]
    
    # 1. Skill matching (0-35 pts)
    if job_skills and user_skills:
        matched = 0
        for js in job_skills:
            for us in user_skills:
                if js in us or us in js:
                    matched += 1
                    break
        skill_score = min(35, (matched / max(len(job_skills), 1)) * 35)
        score += skill_score
        if matched > 0:
            reasons.append(f"技能匹配 {matched} 项")
    
    # 2. Experience matching (0-15 pts)
    user_exp_text = user_profile.get("experience", "").lower()
    job_exp = job.get("experience", "")
    user_years = re.findall(r'(\d+)', user_exp_text)
    job_years = re.findall(r'(\d+)', job_exp)
    if user_years and job_years:
        user_min = int(user_years[0])
        job_req = int(job_years[0])
        if user_min >= job_req:
            score += 15
            reasons.append("经验符合要求")
        elif user_min >= job_req - 1:
            score += 8
            reasons.append("经验基本符合")
    
    # 3. City matching (0-5 pts)
    user_city = user_profile.get("city", "").lower()
    job_city = job.get("city", "").lower()
    if user_city and job_city and user_city in job_city:
        score += 5
        reasons.append("城市匹配")
    
    return {"score": min(99, round(score)), "reasons": reasons}


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/api/config/status')
def config_status():
    return jsonify({"cookie_configured": bool(BOSS_COOKIE), "cookie_length": len(BOSS_COOKIE)})

@app.route('/api/config', methods=['POST'])
def save_config():
    global BOSS_COOKIE
    data = request.json or {}
    cookie = data.get('cookie', '').strip()
    if cookie:
        BOSS_COOKIE = cookie
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump({"boss_cookie": cookie}, f, ensure_ascii=False, indent=2)
        return jsonify({"success": True})
    return jsonify({"error": "No cookie provided"}), 400

@app.route('/api/jobs/match', methods=['POST'])
def api_match():
    data = request.json or {}
    keywords = data.get('keywords', [])
    user_profile = data.get('userProfile', {})
    city = user_profile.get('city', '101010100')
    
    if not BOSS_COOKIE:
        return jsonify({"error": "NO_COOKIE", "message": "请先配置 Boss直聘 Cookie"}), 401
    
    if not keywords:
        return jsonify({"error": "NO_KEYWORDS"}), 400
    
    # Search each keyword
    all_jobs = []
    for kw in keywords[:3]:
        result = boss_search(kw, city, page=1, page_size=15)
        if "jobs" in result:
            all_jobs.extend(result["jobs"])
    
    # Deduplicate
    seen = set()
    unique_jobs = []
    for job in all_jobs:
        jid = job.get("jobId", "")
        if jid and jid not in seen:
            seen.add(jid)
            unique_jobs.append(job)
    
    # Score each job
    scored = []
    for job in unique_jobs:
        match = calculate_match_score(job, user_profile)
        scored.append({
            **job,
            "matchScore": match["score"],
            "matchReasons": match["reasons"],
        })
    
    scored.sort(key=lambda x: x["matchScore"], reverse=True)
    top5 = scored[:5]
    
    return jsonify({
        "keywords": keywords,
        "total_found": len(unique_jobs),
        "recommendations": top5,
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"[Morphos] Server on port {port}")
    print(f"[Morphos] Cookie: {bool(BOSS_COOKIE)}")
    app.run(host='0.0.0.0', port=port, debug=False)
