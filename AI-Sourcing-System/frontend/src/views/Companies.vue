<template>
  <div class="p-8">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Companies</h2>
        <p class="text-gray-500 mt-1">Tracked companies across all stages</p>
      </div>
      <button @click="showCreate = true" class="btn-primary">+ New Company</button>
    </div>
    
    <!-- Filters -->
    <div class="flex gap-3 mb-6">
      <select v-model="filterStatus" class="border border-gray-200 rounded-lg px-3 py-2 text-sm">
        <option value="">All Status</option>
        <option value="sourcing">Sourcing</option>
        <option value="screening">Screening</option>
        <option value="due_diligence">DD</option>
        <option value="ic_pending">IC Pending</option>
        <option value="ic_approved">IC Approved</option>
        <option value="ic_rejected">IC Rejected</option>
      </select>
      <input v-model="searchQuery" placeholder="Search companies..." class="border border-gray-200 rounded-lg px-3 py-2 text-sm w-64">
    </div>
    
    <!-- Companies Table -->
    <div class="card overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50">
          <tr>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Company</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Sector</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Stage</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Status</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Manager</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">IC Score</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Decision</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Contact</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="c in companies" :key="c.id" class="hover:bg-gray-50">
            <td class="px-4 py-3">
              <div>
                <p class="font-medium">{{ c.name }}</p>
                <p class="text-xs text-gray-400 truncate max-w-xs">{{ c.description }}</p>
              </div>
            </td>
            <td class="px-4 py-3">{{ c.sector || '-' }}</td>
            <td class="px-4 py-3">{{ c.stage || '-' }}</td>
            <td class="px-4 py-3">
              <span :class="statusBadge(c.status)">{{ formatStatus(c.status) }}</span>
            </td>
            <td class="px-4 py-3 text-xs">{{ c.assigned_manager || 'Unassigned' }}</td>
            <td class="px-4 py-3">
              <span v-if="c.avg_ic_score" class="font-bold" :class="scoreColor(c.avg_ic_score)">
                {{ c.avg_ic_score.toFixed(1) }}
              </span>
              <span v-else class="text-gray-400">-</span>
            </td>
            <td class="px-4 py-3">
              <span v-if="c.decision_signal" :class="decisionBadge(c.decision_signal)">
                {{ c.decision_signal }}
              </span>
              <span v-else class="text-gray-400">-</span>
            </td>
            <td class="px-4 py-3">
              <span :class="contactBadge(c.contact_status)">{{ c.contact_status }}</span>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="companies.length === 0" class="p-8 text-center text-gray-400">
        No companies found
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { listCompanies } from '@/api/client'

const companies = ref<any[]>([])
const filterStatus = ref('')
const searchQuery = ref('')
const showCreate = ref(false)

function statusBadge(status: string) {
  const map: Record<string, string> = {
    sourcing: 'badge-gray',
    screening: 'badge-blue',
    due_diligence: 'badge-yellow',
    ic_pending: 'badge-yellow',
    ic_approved: 'badge-green',
    ic_rejected: 'badge-red',
    portfolio: 'badge-green',
    passed: 'badge-gray',
  }
  return `badge ${map[status] || 'badge-gray'}`
}

function formatStatus(status: string) {
  return status.replace(/_/g, ' ')
}

function scoreColor(score: number) {
  if (score >= 8) return 'text-green-600'
  if (score >= 6) return 'text-blue-600'
  if (score >= 4) return 'text-yellow-600'
  return 'text-red-600'
}

function decisionBadge(signal: string) {
  const map: Record<string, string> = {
    strong_buy: 'badge-green',
    buy: 'badge-green',
    hold: 'badge-yellow',
    pass: 'badge-red',
    strong_pass: 'badge-red',
  }
  return `badge ${map[signal] || 'badge-gray'}`
}

function contactBadge(status: string) {
  const map: Record<string, string> = {
    not_contacted: 'badge-gray',
    contacting: 'badge-yellow',
    contacted: 'badge-green',
  }
  return `badge ${map[status] || 'badge-gray'}`
}

async function loadCompanies() {
  const params: any = {}
  if (filterStatus.value) params.status = filterStatus.value
  if (searchQuery.value) params.search = searchQuery.value
  const res = await listCompanies(params)
  companies.value = res.data
}

watch([filterStatus, searchQuery], loadCompanies)
onMounted(loadCompanies)
</script>
