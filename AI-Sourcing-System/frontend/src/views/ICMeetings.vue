<template>
  <div class="p-8">
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-900">IC Meetings</h2>
      <p class="text-gray-500 mt-1">Investment Committee decisions and rankings</p>
    </div>
    
    <!-- Weekly Ranking -->
    <div class="card mb-8">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold">Weekly IC Ranking — Week {{ currentWeek }}</h3>
        <div class="flex gap-2">
          <button @click="currentWeek--" class="btn-secondary text-sm">← Prev</button>
          <button @click="currentWeek++" class="btn-secondary text-sm">Next →</button>
        </div>
      </div>
      
      <table class="w-full text-sm">
        <thead class="bg-gray-50">
          <tr>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Rank</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Company</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Sector</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Votes</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Final Score</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Signal</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Outcome</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="r in rankings" :key="r.final_rank" class="hover:bg-gray-50">
            <td class="px-4 py-3 font-bold">#{{ r.final_rank }}</td>
            <td class="px-4 py-3 font-medium">{{ r.company_name }}</td>
            <td class="px-4 py-3">{{ r.sector }}</td>
            <td class="px-4 py-3">{{ r.invest_votes }}/{{ r.total_votes }}</td>
            <td class="px-4 py-3">
              <span class="font-bold" :class="scoreColor(r.final_score)">{{ r.final_score?.toFixed(2) }}</span>
            </td>
            <td class="px-4 py-3">
              <span :class="decisionBadge(r.decision_signal)">{{ r.decision_signal }}</span>
            </td>
            <td class="px-4 py-3">
              <span :class="outcomeBadge(r.outcome)">{{ r.outcome }}</span>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="rankings.length === 0" class="p-8 text-center text-gray-400">
        No meetings for this week
      </div>
    </div>
    
    <!-- All Meetings -->
    <div class="card">
      <h3 class="text-lg font-semibold mb-4">All Meetings</h3>
      <table class="w-full text-sm">
        <thead class="bg-gray-50">
          <tr>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Date</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Company ID</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Score</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Outcome</th>
            <th class="text-left px-4 py-3 font-medium text-gray-500">Summary</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="m in meetings" :key="m.id" class="hover:bg-gray-50">
            <td class="px-4 py-3 text-xs">{{ formatDate(m.meeting_date) }}</td>
            <td class="px-4 py-3 font-mono text-xs">{{ m.company_id?.slice(0, 8) }}...</td>
            <td class="px-4 py-3 font-bold">{{ m.final_score?.toFixed(2) }}</td>
            <td class="px-4 py-3">
              <span :class="outcomeBadge(m.outcome)">{{ m.outcome }}</span>
            </td>
            <td class="px-4 py-3 text-gray-500 text-xs max-w-md truncate">{{ m.summary }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { getWeeklyRanking, listICMeetings } from '@/api/client'

const currentWeek = ref(getCurrentWeek())
const rankings = ref<any[]>([])
const meetings = ref<any[]>([])

function getCurrentWeek() {
  const now = new Date()
  const start = new Date(now.getFullYear(), 0, 1)
  const diff = now.getTime() - start.getTime()
  return Math.ceil(diff / (7 * 24 * 60 * 60 * 1000))
}

function scoreColor(score: number) {
  if (score >= 7.5) return 'text-green-600'
  if (score >= 6) return 'text-blue-600'
  if (score >= 5) return 'text-yellow-600'
  if (score >= 4) return 'text-orange-600'
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

function outcomeBadge(outcome: string) {
  const map: Record<string, string> = {
    proceed: 'badge-green',
    abandon: 'badge-red',
    table: 'badge-yellow',
  }
  return `badge ${map[outcome] || 'badge-gray'}`
}

function formatDate(date: string) {
  if (!date) return '-'
  return new Date(date).toLocaleDateString()
}

async function loadRankings() {
  const res = await getWeeklyRanking(currentWeek.value)
  rankings.value = res.data.rankings || []
}

async function loadMeetings() {
  const res = await listICMeetings({ limit: 50 })
  meetings.value = res.data
}

watch(currentWeek, loadRankings)
onMounted(() => {
  loadRankings()
  loadMeetings()
})
</script>
