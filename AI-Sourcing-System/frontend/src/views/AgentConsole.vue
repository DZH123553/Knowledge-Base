<template>
  <div class="p-8">
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-900">Agent Console</h2>
      <p class="text-gray-500 mt-1">Trigger workflows and manage agents</p>
    </div>
    
    <!-- Agent Config -->
    <div class="card mb-8">
      <h3 class="text-lg font-semibold mb-4">Agent Configuration</h3>
      <div class="grid grid-cols-3 gap-6">
        <div>
          <p class="text-sm font-medium text-gray-500 mb-2">Investment Managers ({{ agentConfig.investment_managers?.length || 0 }})</p>
          <div class="space-y-1 max-h-60 overflow-y-auto">
            <div v-for="a in agentConfig.investment_managers" :key="a.id" class="text-xs bg-gray-50 rounded px-2 py-1">
              <span class="font-medium">{{ a.name }}</span>
              <span class="text-gray-400"> — {{ a.sector }}</span>
            </div>
          </div>
        </div>
        <div>
          <p class="text-sm font-medium text-gray-500 mb-2">Risk Control ({{ agentConfig.risk_controls?.length || 0 }})</p>
          <div class="space-y-1">
            <div v-for="a in agentConfig.risk_controls" :key="a.id" class="text-xs bg-gray-50 rounded px-2 py-1">
              <span class="font-medium">{{ a.name }}</span>
              <span class="text-gray-400"> — {{ a.focus }}</span>
            </div>
          </div>
        </div>
        <div>
          <p class="text-sm font-medium text-gray-500 mb-2">IC Members ({{ agentConfig.ic_members?.length || 0 }})</p>
          <div class="space-y-1">
            <div v-for="a in agentConfig.ic_members" :key="a.id" class="text-xs bg-gray-50 rounded px-2 py-1">
              <span class="font-medium">{{ a.name }}</span>
              <span class="text-gray-400"> — {{ a.persona?.slice(0, 20) }}...</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Actions -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Auto IC Trigger -->
      <div class="card">
        <h3 class="text-lg font-semibold mb-4">🚀 Auto Trigger IC</h3>
        <p class="text-sm text-gray-500 mb-4">输入公司名称，自动走完 Screen → DD → Risk → IC 全流程</p>
        <div class="space-y-3">
          <input v-model="icForm.company_name" placeholder="Company Name" class="w-full border rounded-lg px-3 py-2">
          <textarea v-model="icForm.description" placeholder="Description (optional)" rows="3" class="w-full border rounded-lg px-3 py-2"></textarea>
          <button 
            @click="triggerIC" 
            :disabled="icLoading"
            class="btn-primary w-full"
          >
            {{ icLoading ? 'Running...' : 'Run Full Pipeline' }}
          </button>
        </div>
        <div v-if="icResult" class="mt-4 bg-gray-50 rounded-lg p-4 text-sm">
          <p><strong>Company:</strong> {{ icResult.company_name }}</p>
          <p><strong>DD Score:</strong> {{ icResult.dd_score }}</p>
          <p><strong>Risk Level:</strong> {{ icResult.risk_level_avg?.toFixed(2) }}</p>
          <p><strong>IC Score:</strong> <span class="font-bold" :class="scoreColor(icResult.ic_score)">{{ icResult.ic_score }}</span></p>
          <p><strong>Decision:</strong> <span :class="outcomeBadge(icResult.decision)">{{ icResult.decision }}</span></p>
        </div>
      </div>
      
      <!-- Human Feedback -->
      <div class="card">
        <h3 class="text-lg font-semibold mb-4">📝 Human Feedback</h3>
        <p class="text-sm text-gray-500 mb-4">投资经理对Agent输出的反馈，触发记忆更新</p>
        <div class="space-y-3">
          <input v-model="feedbackForm.company_id" placeholder="Company ID" class="w-full border rounded-lg px-3 py-2">
          <select v-model="feedbackForm.manager_name" class="w-full border rounded-lg px-3 py-2">
            <option value="">Select Manager</option>
            <option>Peter Chen</option>
            <option>Bin</option>
            <option>TQT</option>
            <option>Jianing</option>
          </select>
          <select v-model="feedbackForm.contact_status" class="w-full border rounded-lg px-3 py-2">
            <option value="">Contact Status</option>
            <option value="not_contacted">Not Contacted</option>
            <option value="contacting">Contacting</option>
            <option value="contacted">Contacted</option>
          </select>
          <div class="grid grid-cols-2 gap-2">
            <input v-model.number="feedbackForm.project_rating" type="number" min="1" max="10" placeholder="Project (1-10)" class="border rounded-lg px-3 py-2">
            <input v-model.number="feedbackForm.team_rating" type="number" min="1" max="10" placeholder="Team (1-10)" class="border rounded-lg px-3 py-2">
          </div>
          <textarea v-model="feedbackForm.text_feedback" placeholder="Text feedback..." rows="2" class="w-full border rounded-lg px-3 py-2"></textarea>
          <button 
            @click="submitFeedback" 
            :disabled="feedbackLoading"
            class="btn-primary w-full"
          >
            {{ feedbackLoading ? 'Submitting...' : 'Submit Feedback' }}
          </button>
        </div>
        <div v-if="feedbackResult" class="mt-4 bg-green-50 text-green-800 rounded-lg p-3 text-sm">
          {{ feedbackResult }}
        </div>
      </div>
    </div>
    
    <!-- Batch Process -->
    <div class="card mt-6">
      <h3 class="text-lg font-semibold mb-4">⚡ Batch Process</h3>
      <p class="text-sm text-gray-500 mb-4">批量处理所有待处理信号</p>
      <div class="flex items-center gap-4">
        <input v-model.number="batchLimit" type="number" min="1" max="50" class="border rounded-lg px-3 py-2 w-24">
        <button @click="runBatch" :disabled="batchLoading" class="btn-primary">
          {{ batchLoading ? 'Processing...' : `Process ${batchLimit} Signals` }}
        </button>
      </div>
      <div v-if="batchResult" class="mt-4 bg-gray-50 rounded-lg p-4 text-sm">
        <p>Processed: {{ batchResult.processed }}</p>
        <p>Success: {{ batchResult.success }}</p>
        <p>Failed: {{ batchResult.failed }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getAgentConfig, autoTriggerIC, submitHumanFeedback, batchProcess } from '@/api/client'

const agentConfig = ref<any>({})
const icForm = ref({ company_name: '', description: '' })
const icLoading = ref(false)
const icResult = ref<any>(null)

const feedbackForm = ref({
  company_id: '',
  manager_name: '',
  contact_status: '',
  project_rating: null as number | null,
  team_rating: null as number | null,
  text_feedback: '',
})
const feedbackLoading = ref(false)
const feedbackResult = ref('')

const batchLimit = ref(10)
const batchLoading = ref(false)
const batchResult = ref<any>(null)

function scoreColor(score: number) {
  if (score >= 7.5) return 'text-green-600'
  if (score >= 6) return 'text-blue-600'
  if (score >= 5) return 'text-yellow-600'
  return 'text-red-600'
}

function outcomeBadge(outcome: string) {
  const map: Record<string, string> = {
    proceed: 'badge-green',
    abandon: 'badge-red',
    table: 'badge-yellow',
  }
  return `badge ${map[outcome] || 'badge-gray'}`
}

async function loadConfig() {
  const res = await getAgentConfig()
  agentConfig.value = res.data
}

async function triggerIC() {
  icLoading.value = true
  try {
    const res = await autoTriggerIC(icForm.value)
    icResult.value = res.data
  } catch (e: any) {
    icResult.value = { error: e.response?.data?.detail || 'Failed' }
  } finally {
    icLoading.value = false
  }
}

async function submitFeedback() {
  feedbackLoading.value = true
  try {
    const res = await submitHumanFeedback(feedbackForm.value)
    feedbackResult.value = `Feedback saved! Memory updated for agent.`
    feedbackForm.value = { company_id: '', manager_name: '', contact_status: '', project_rating: null, team_rating: null, text_feedback: '' }
  } catch (e: any) {
    feedbackResult.value = `Error: ${e.response?.data?.detail || 'Failed'}`
  } finally {
    feedbackLoading.value = false
  }
}

async function runBatch() {
  batchLoading.value = true
  try {
    const res = await batchProcess({ max_signals: batchLimit.value })
    batchResult.value = res.data
  } finally {
    batchLoading.value = false
  }
}

onMounted(loadConfig)
</script>
