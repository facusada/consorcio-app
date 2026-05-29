<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- Sidebar -->
    <aside class="w-56 bg-blue-900 text-white flex flex-col shrink-0">
      <div class="p-5 border-b border-blue-800">
        <h1 class="text-lg font-bold">Consorcio App</h1>
        <p class="text-blue-300 text-xs mt-0.5">Panel de administracion</p>
      </div>

      <nav class="flex-1 p-3 space-y-1">
        <NuxtLink
          v-for="item in menu"
          :key="item.ruta"
          :to="item.ruta"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition"
          :class="estaActivo(item.ruta)
            ? 'bg-blue-700 text-white'
            : 'text-blue-200 hover:bg-blue-800 hover:text-white'"
        >
          <span class="text-base">{{ item.icono }}</span>
          {{ item.etiqueta }}
        </NuxtLink>
      </nav>

      <div class="p-4 border-t border-blue-800">
        <p class="text-blue-300 text-xs mb-2">{{ auth.usuario?.nombre_completo }}</p>
        <button
          @click="auth.cerrarSesion()"
          class="text-xs text-blue-400 hover:text-white transition"
        >
          Cerrar sesion
        </button>
      </div>
    </aside>

    <!-- Contenido -->
    <main class="flex-1 overflow-auto">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: "auth" })

const auth = useAuthStore()
const route = useRoute()

const menu = [
  { ruta: "/admin/periodos", etiqueta: "Periodos", icono: "📅" },
  { ruta: "/admin/unidades", etiqueta: "Unidades", icono: "🏢" },
  { ruta: "/admin/propietarios", etiqueta: "Propietarios", icono: "👥" },
]

function estaActivo(ruta: string) {
  return route.path.startsWith(ruta)
}
</script>
