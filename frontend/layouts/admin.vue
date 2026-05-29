<template>
  <div class="flex h-screen overflow-hidden bg-slate-50">

    <!-- Sidebar -->
    <aside class="w-60 flex flex-col shrink-0 overflow-y-auto" style="background: var(--sidebar-bg); border-right: 1px solid var(--sidebar-border);">

      <!-- Logo -->
      <div class="px-5 pt-6 pb-5">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center shadow-lg">
            <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-.75 4.5H21m-3.75 3.75h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008z" />
            </svg>
          </div>
          <div>
            <p class="text-sm font-bold text-white leading-tight">Consorcio</p>
            <p class="text-xs" style="color: var(--sidebar-text)">Administracion</p>
          </div>
        </div>
      </div>

      <!-- Divider -->
      <div class="mx-4 mb-3" style="height: 1px; background: var(--sidebar-border)" />

      <!-- Nav -->
      <nav class="px-3 flex-1 space-y-0.5">
        <template v-for="item in menu" :key="item.ruta">
          <NuxtLink
            :to="item.ruta"
            class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-150"
            :class="estaActivo(item.ruta)
              ? 'text-white'
              : 'hover:text-white'"
            :style="estaActivo(item.ruta)
              ? { background: 'var(--sidebar-active)', color: 'white' }
              : { color: 'var(--sidebar-text)' }"
          >
            <span class="w-5 h-5 flex items-center justify-center shrink-0" v-html="item.icono" />
            {{ item.etiqueta }}
          </NuxtLink>
        </template>
      </nav>

      <!-- User -->
      <div class="p-4 mt-auto">
        <div class="mx-0 mb-3" style="height: 1px; background: var(--sidebar-border)" />
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center text-indigo-300 text-xs font-bold">
            {{ iniciales }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-white truncate leading-tight">{{ auth.usuario?.nombre_completo }}</p>
            <p class="text-xs truncate" style="color: var(--sidebar-text)">Administrador</p>
          </div>
          <button
            @click="auth.cerrarSesion()"
            title="Cerrar sesion"
            class="w-7 h-7 flex items-center justify-center rounded-lg transition-colors hover:bg-white/10"
            style="color: var(--sidebar-text)"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
            </svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- Main -->
    <main class="flex-1 overflow-y-auto">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: "auth" })

const auth = useAuthStore()
const route = useRoute()

const menu = [
  {
    ruta: "/admin/periodos",
    etiqueta: "Periodos",
    icono: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 9v7.5m-9-6h.008v.008H12v-.008zM12 15h.008v.008H12V15zm0 2.25h.008v.008H12v-.008zM9.75 15h.008v.008H9.75V15zm0 2.25h.008v.008H9.75v-.008zM7.5 15h.008v.008H7.5V15zm0 2.25h.008v.008H7.5v-.008zm6.75-4.5h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008V15zm0 2.25h.008v.008h-.008v-.008zm2.25-4.5h.008v.008H16.5v-.008zm0 2.25h.008v.008H16.5V15z"/></svg>`,
  },
  {
    ruta: "/admin/unidades",
    etiqueta: "Unidades",
    icono: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 21h16.5M4.5 3h15M5.25 3v18m13.5-18v18M9 6.75h1.5m-1.5 3h1.5m-1.5 3h1.5m3-6H15m-1.5 3H15m-1.5 3H15M9 21v-3.375c0-.621.504-1.125 1.125-1.125h3.75c.621 0 1.125.504 1.125 1.125V21"/></svg>`,
  },
  {
    ruta: "/admin/propietarios",
    etiqueta: "Propietarios",
    icono: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z"/></svg>`,
  },
]

const estaActivo = (ruta: string) => useRoute().path.startsWith(ruta)

const iniciales = computed(() => {
  const n = auth.usuario?.nombre_completo ?? ""
  return n.split(" ").slice(0, 2).map(w => w[0]).join("").toUpperCase()
})
</script>
