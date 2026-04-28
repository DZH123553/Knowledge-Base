<template>
  <div class="min-h-screen flex">
    <!-- Sidebar -->
    <aside class="w-64 bg-gray-900 text-white flex-shrink-0">
      <div class="p-6">
        <h1 class="text-xl font-bold tracking-tight">AI Sourcing</h1>
        <p class="text-xs text-gray-400 mt-1">Agentic VC Intelligence</p>
      </div>
      
      <nav class="mt-4 px-3 space-y-1">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          :class="[
            'flex items-center px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
            $route.path === item.path
              ? 'bg-blue-600 text-white'
              : 'text-gray-300 hover:bg-gray-800 hover:text-white'
          ]"
        >
          <span class="mr-3 text-lg">{{ item.icon }}</span>
          {{ item.name }}
        </router-link>
      </nav>
      
      <div class="absolute bottom-0 left-0 right-0 p-4">
        <div class="bg-gray-800 rounded-lg p-3">
          <p class="text-xs text-gray-400">System Status</p>
          <div class="flex items-center mt-1">
            <span class="w-2 h-2 rounded-full bg-green-400 mr-2"></span>
            <span class="text-xs font-medium">Operational</span>
          </div>
        </div>
      </div>
    </aside>
    
    <!-- Main Content -->
    <main class="flex-1 overflow-auto">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
const navItems = [
  { path: '/', name: 'Dashboard', icon: '📊' },
  { path: '/signals', name: 'Signals', icon: '📡' },
  { path: '/companies', name: 'Companies', icon: '🏢' },
  { path: '/ic-meetings', name: 'IC Meetings', icon: '⚖️' },
  { path: '/reports', name: 'Reports', icon: '📄' },
  { path: '/agent-console', name: 'Agent Console', icon: '🤖' },
]
</script>
