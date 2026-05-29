<template>
  <div class="p-8 max-w-5xl mx-auto">

    <div class="mb-8">
      <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Propietarios</h1>
      <p class="text-slate-500 text-sm mt-1">7 propietarios · 13 unidades asignadas</p>
    </div>

    <div v-if="cargando" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <UiSkeleton v-for="i in 7" :key="i" height="120px" />
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 stagger">
      <div
        v-for="p in propietarios"
        :key="p.id"
        class="bg-white rounded-2xl border border-slate-100 shadow-card hover:shadow-card-hover hover:-translate-y-0.5 transition-all duration-200 cursor-pointer p-5"
        @click="navigateTo(`/admin/propietarios/${p.id}`)"
      >
        <div class="flex items-start gap-4">
          <!-- Avatar -->
          <div class="w-11 h-11 rounded-xl shrink-0 flex items-center justify-center text-sm font-bold"
            :style="{ background: colorAvatar(p.apellido).bg, color: colorAvatar(p.apellido).text }">
            {{ iniciales(p.nombre, p.apellido) }}
          </div>

          <div class="flex-1 min-w-0">
            <p class="text-sm font-semibold text-slate-900 truncate">{{ p.apellido }}, {{ p.nombre }}</p>
            <p v-if="p.email" class="text-xs text-slate-400 truncate mt-0.5">{{ p.email }}</p>
            <p v-else class="text-xs text-slate-300 mt-0.5">Sin email registrado</p>
          </div>

          <svg class="w-4 h-4 text-slate-300 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
          </svg>
        </div>
      </div>

      <div v-if="!propietarios.length" class="col-span-full">
        <div class="bg-white rounded-2xl border border-slate-100 shadow-card">
          <UiEmptyState icon="👥" titulo="Sin propietarios" descripcion="No hay propietarios registrados." />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "admin", middleware: "auth" })

interface Propietario {
  id: string; nombre: string; apellido: string; email: string | null
}

const api = useApi()
const cargando = ref(true)
const propietarios = ref<Propietario[]>([])

onMounted(async () => {
  propietarios.value = await api.get<Propietario[]>("/api/v1/propietarios")
  cargando.value = false
})

function iniciales(nombre: string, apellido: string) {
  return `${nombre[0]}${apellido[0]}`.toUpperCase()
}

const PALETA = [
  { bg: "#eef2ff", text: "#4338ca" },
  { bg: "#d1fae5", text: "#065f46" },
  { bg: "#fef3c7", text: "#92400e" },
  { bg: "#fee2e2", text: "#991b1b" },
  { bg: "#ede9fe", text: "#5b21b6" },
  { bg: "#dbeafe", text: "#1e40af" },
  { bg: "#fce7f3", text: "#9d174d" },
]

function colorAvatar(apellido: string) {
  const idx = apellido.charCodeAt(0) % PALETA.length
  return PALETA[idx]
}
</script>
