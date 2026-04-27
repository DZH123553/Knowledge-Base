<template>
  <div class="p-8">
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-900">Reports</h2>
      <p class="text-gray-500 mt-1">Due Diligence and Risk reports</p>
    </div>
    
    <!-- Tabs -->
    <div class="flex gap-4 mb-6 border-b border-gray-200">
      <button
        @click="activeTab = 'dd'"
        :class="['pb-3 px-1 text-sm font-medium border-b-2 transition-colors', activeTab === 'dd' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700']"
      >
        DD Reports
      </button>
      <button
        @click="activeTab = 'risk'"
        :class="['pb-3 px-1 text-sm font-medium border-b-2 transition-colors', activeTab === 'risk' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700']"
      >
        Risk Reports
      </button>
    </div>
    
    <!-- DD Reports -->
    <div v-if="activeTab === 'dd'" class="space-y-4">
      <div v-for="r in ddReports" :key="r.id" class="card">
        <div class="flex items-start justify-between">
          <div>
            <p class="text-xs text-gray-400">{{ r.agent_name }} — {{ formatDate(r.created_at) }}</p>
            <h4 class="font-semibold mt-1">Company: {{ r.company_id?.slice(0, 8) }}...</h4>
          </div>
          <div class="text-right">
            <p class="text-2xl font-bold" :class="scoreColor(r.overall_score)">{{ r.overall_score?.toFixed(1) }}</p>
            <span :class="recommendationBadge(r.recommendation)">{{ r.recommendation }}</span>
          </div>
        </div>
        <div class="grid grid-cols-5 gap-3 mt-4 text-center">
          <div class="bg-gray-50 rounded-lg p-2">
            <p class="text-xs text-gray-500">Market</p>
            <p class="font-bold">{{ r.market_score?.toFixed(1) }}</p>
          </div>
          <div class="bg-gray-50 rounded-lg p-2">
            <p class="text-xs text-gray-500">Team</p>
            <p class="font-bold">{{ r.team_score?.toFixed(1) }}</p>
          </div>
          <div class="bg-gray-50 rounded-lg p-2">
            <p class="text-xs text-gray-500">Product</p>
            <p class="font-bold">{{ r.product_score?.toFixed(1) }}</p>
          </div>
          <div class="bg-gray-50 rounded-lg p-2">
            <p class="text-xs text-gray-500">Traction</p>
            <p class="font-bold">{{ r.traction_score?.toFixed(1) }}</p>
          </div>
          <div class="bg-gray-50 rounded-lg p-2">
            <p class="text-xs text-gray-500">Moat</p>
            <p class="font-bold">{{ r.moat_score?.toFixed(1) }}</p>
          </div>
        </div>
        <div class="mt-4 space-y-2 text-sm">
          <p v-if="r.market_position"><strong>Position:</strong> {{ r.market_position }}</p>
          <p v-if="r.team_summary"><strong>Team:</strong> {{ r.team_summary }}</p>
          <p v-if="r.moat"><strong>Moat:</strong> {{ r.moat }}</p>
        </div>
      </div>
    </div>
    
    <!-- Risk Reports -->
    <div v-else class="space-y-4">
      <div v-for="r in riskReports" :key="r.id" class="card">
        <div class="flex items-start justify-between">
          <div>
            <p class="text-xs text-gray-400">{{ r.agent_name }} — {{ formatDate(r.created_at) }}</p>
            <h4 class="font-semibold mt-1">Company: {{ r.company_id?.slice(0, 8) }}...</h4>
          </div>
          <div class="text-right">
            <p class="text-2xl font-bold" :class="riskColor(r.risk_level)">{{ r.risk_level?.toFixed(1) }}</p>
            <p class="text-xs text-gray-500">Risk Level</p>
          </div>
        </div>
        <div v-if="r.red_flags?.length" class="mt-4">
          <p class="text-sm font-medium text-red-600 mb-2">Red Flags:</p>
          <ul class="list-disc list-inside text-sm text-gray-700 space-y-1">
            <li v-for="flag in r.red_flags" :key="flag">{{ flag }}</li>
          </ul>
        </div>
        <div v-if="r.mitigations" class="mt-4">
          <p class="text-sm font-medium text-green-600 mb-1">Mitigations:</p>
          <p class="text-sm text-gray-700">{{ r.mitigations }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { listInvestmentReports, listRiskReports } from '@/api/client'

const activeTab = ref('dd')
const ddReports = ref<any[]>([])
const riskReports = ref<any[]>([])

function scoreColor(score: number) {
  if (score >= 8) return 'text-green-600'
  if (score >= 6) return 'text-blue-600'
  if (score >= 4) return 'text-yellow-600'
  return 'text-red-600'
}

function riskColor(level: number) {
  if (level <= 3) return 'text-green-600'
  if (level <= 6) return 'text-yellow-600'
  return 'text-red-600'
}

function recommendationBadge(rec: string) {
  const map: Record<string, string> = {
    proceed: 'badge-green',
    watch: 'badge-yellow',
    abandon: 'badge-red',
  }
  return `badge ${map[rec] || 'badge-gray'}`
}

function formatDate(date: string) {
  if (!date) return '-'
  return new Date(date).toLocaleDateString()
}

async function loadReports() {
  const [ddRes, riskRes] = await Promise.all([
    listInvestmentReports({ limit: 20 }),
    listRiskReports({ limit: 20 }),
  ])
  ddReports.value = ddRes.data
  riskReports.value = riskRes.data
}

onMounted(loadReports)
</script>
