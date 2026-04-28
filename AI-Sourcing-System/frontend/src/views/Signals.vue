<template>
  <div class="p-8">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Signals</h2>
        <p class="text-gray-500 mt-1">Raw investment signals from all sources</p>
      </div>
      <button @click="showCreate = true" class="btn-primary">+ New Signal</button>
    </div>
    
    <!-- Filters -->
    <div class="flex gap-3 mb-6">
      <select v-model="filterStatus" class="border border-gray-200 rounded-lg px-3 py-2 text-sm">
        <option value="">All Status</option>
        <option value="raw">Raw</option>
        <option value="parsed">Parsed</option>
        <option value="screened">Screened</option>
        <option value="rejected">Rejected</option>
      </select>
      <select v-model="filterSector" class="border border-gray-200 rounded-lg px-3 py-2 text-sm">
        <option value="">All Sectors</option>
        <option v-for="s in sectors" :key="s" :value="s">{{ s }}</option>
      </select>
      <button @click="loadSignals" class="btn-secondary">Refresh</button>
    </div>
    
    <!-- Signals Table -->
    <div class="card overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50">
          <tr>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Source</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Content</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Company</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Sector</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Status</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Confidence</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="s in signals" :key="s.id" class="hover:bg-gray-50">
            <td class="px-4 py-3">
              <span class="badge-gray capitalize">{{ s.source }}</span>
            </td>
            <td class="px-4 py-3 max-w-md">
              <p class="truncate">{{ s.raw_content }}</p>
            </td>
            <td class="px-4 py-3">{{ s.mentioned_company || '-' }}</td>
            <td class="px-4 py-3">{{ s.sector || '-' }}</td>
            <td class="px-4 py-3">
              <span :class="statusBadge(s.status)">{{ s.status }}</span>
            </td>
            <td class="px-4 py-3">
              <div class="flex items-center">
                <div class="w-16 bg-gray-100 rounded-full h-1.5 mr-2">
                  <div class="bg-blue-500 h-1.5 rounded-full" :style="{ width: (s.confidence * 100) + '%' }"></div>
                </div>
                <span class="text-xs">{{ (s.confidence * 100).toFixed(0) }}%</span>
              </div>
            </td>
            <td class="px-4 py-3">
              <button 
                v-if="s.status === 'raw'"
                @click="processSignal(s.id)"
                :disabled="processing[s.id]"
                class="text-blue-600 hover:text-blue-800 text-xs font-medium"
              >
                {{ processing[s.id] ? 'Processing...' : 'Run Pipeline' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="signals.length === 0" class="p-8 text-center text-gray-400">
        No signals found
      </div>
    </div>
    
    <!-- Create Signal Modal -->
    <div v-if="showCreate" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-lg">
        <h3 class="text-lg font-semibold mb-4">Create New Signal</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Source</label>
            <select v-model="newSignal.source" class="w-full border rounded-lg px-3 py-2">
              <option value="manual">Manual</option>
              <option value="twitter">Twitter</option>
              <option value="reddit">Reddit</option>
              <option value="polymarket">Polymarket</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Content</label>
            <textarea v-model="newSignal.raw_content" rows="4" class="w-full border rounded-lg px-3 py-2"></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Sector</label>
            <select v-model="newSignal.sector" class="w-full border rounded-lg px-3 py-2">
              <option value="">Auto-detect</option>
              <option v-for="s in sectors" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
        </div>
        <div class="flex justify-end gap-3 mt-6">
          <button @click="showCreate = false" class="btn-secondary">Cancel</button>
          <button @click="createSignal" class="btn-primary">Create</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { listSignals, createSignal as apiCreateSignal, processSignal as apiProcessSignal } from '@/api/client'

const signals = ref<any[]>([])
const filterStatus = ref('')
const filterSector = ref('')
const showCreate = ref(false)
const processing = ref<Record<string, boolean>>({})

const sectors = ['AI', 'Web3', 'Healthcare', 'HardTech', 'Consumer', 'Enterprise', 'Fintech', 'Climate']

const newSignal = ref({
  source: 'manual',
  raw_content: '',
  sector: '',
})

function statusBadge(status: string) {
  const map: Record<string, string> = {
    raw: 'badge-gray',
    parsed: 'badge-blue',
    screened: 'badge-green',
    rejected: 'badge-red',
    archived: 'badge-gray',
  }
  return `badge ${map[status] || 'badge-gray'}`
}

async function loadSignals() {
  const params: any = {}
  if (filterStatus.value) params.status = filterStatus.value
  if (filterSector.value) params.sector = filterSector.value
  const res = await listSignals(params)
  signals.value = res.data
}

async function createSignal() {
  await apiCreateSignal(newSignal.value)
  showCreate.value = false
  newSignal.value = { source: 'manual', raw_content: '', sector: '' }
  await loadSignals()
}

async function processSignal(id: string) {
  processing.value[id] = true
  try {
    await apiProcessSignal(id)
    await loadSignals()
  } finally {
    processing.value[id] = false
  }
}

onMounted(loadSignals)
</script>
