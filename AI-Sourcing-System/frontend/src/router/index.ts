import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'
import Signals from '@/views/Signals.vue'
import Companies from '@/views/Companies.vue'
import ICMeetings from '@/views/ICMeetings.vue'
import Reports from '@/views/Reports.vue'
import AgentConsole from '@/views/AgentConsole.vue'

const routes = [
  { path: '/', name: 'Dashboard', component: Dashboard },
  { path: '/signals', name: 'Signals', component: Signals },
  { path: '/companies', name: 'Companies', component: Companies },
  { path: '/ic-meetings', name: 'ICMeetings', component: ICMeetings },
  { path: '/reports', name: 'Reports', component: Reports },
  { path: '/agent-console', name: 'AgentConsole', component: AgentConsole },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
