<template>
  <div class="p-8 max-w-5xl mx-auto">

    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Unidades funcionales</h1>
      <p class="text-slate-500 text-sm mt-1">13 unidades · 7 departamentos + 6 cocheras</p>
    </div>

    <!-- Loading -->
    <div v-if="cargando" class="space-y-4">
      <UiSkeleton height="72px" />
      <UiSkeleton height="320px" />
      <UiSkeleton height="240px" />
    </div>

    <template v-else>
      <!-- Indice summary -->
      <div class="flex items-center justify-between bg-white rounded-2xl border border-slate-100 shadow-card px-6 py-4 mb-6">
        <div class="flex items-center gap-4">
          <div class="w-10 h-10 rounded-xl flex items-center justify-center"
            :class="Math.abs(sumaIndices - 100) < 0.01 ? 'bg-emerald-50' : 'bg-red-50'">
            <svg v-if="Math.abs(sumaIndices - 100) < 0.01" class="w-5 h-5 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <svg v-else class="w-5 h-5 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
            </svg>
          </div>
          <div>
            <p class="text-sm font-semibold text-slate-900">
              Suma de indices: <span class="tabular font-bold">{{ sumaIndices.toFixed(2) }}%</span>
            </p>
            <p class="text-xs" :class="Math.abs(sumaIndices - 100) < 0.01 ? 'text-emerald-600' : 'text-red-500'">
              {{ Math.abs(sumaIndices - 100) < 0.01 ? "Los indices suman exactamente 100%" : "Los indices no suman 100% — revisar reglamento" }}
            </p>
          </div>
        </div>

        <!-- Bar visualizacion -->
        <div class="hidden lg:flex items-center gap-1">
          <div v-for="u in unidades" :key="u.id"
            class="h-8 rounded-sm transition-all hover:opacity-80"
            :class="u.tipo === 'departamento' ? 'bg-indigo-400' : 'bg-slate-300'"
            :style="{ width: `${parseFloat(u.indice_prorrateo) * 3}px` }"
            :title="`${u.codigo}: ${u.indice_prorrateo}%`"
          />
        </div>
      </div>

      <!-- Departamentos -->
      <div class="bg-white rounded-2xl border border-slate-100 shadow-card overflow-hidden mb-4">
        <div class="flex items-center gap-3 px-5 py-4 border-b border-slate-100">
          <div class="w-2 h-2 rounded-full bg-indigo-400" />
          <h2 class="text-sm font-semibold text-slate-900">Departamentos</h2>
          <span class="text-xs text-slate-400 tabular">{{ departamentos.length }} unidades</span>
        </div>
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-slate-50/60 border-b border-slate-100">
              <th class="px-5 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wide">Unidad</th>
              <th class="px-5 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wide">Piso</th>
              <th class="px-5 py-3 text-right text-xs font-semibold text-slate-400 uppercase tracking-wide">Indice</th>
              <th class="px-5 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wide">Estado</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50">
            <tr v-for="u in departamentos" :key="u.id" class="hover:bg-slate-50/40 transition-colors">
              <td class="px-5 py-3.5">
                <div class="flex items-center gap-2.5">
                  <div class="w-7 h-7 rounded-lg bg-indigo-50 flex items-center justify-center text-xs font-bold text-indigo-600">
                    {{ u.numero }}
                  </div>
                  <span class="font-semibold text-slate-900">{{ u.codigo }}</span>
                </div>
              </td>
              <td class="px-5 py-3.5 text-slate-500">Piso {{ u.piso || "—" }}</td>
              <td class="px-5 py-3.5 text-right">
                <div class="flex items-center justify-end gap-2">
                  <div class="h-1.5 rounded-full bg-indigo-100 w-16 overflow-hidden">
                    <div class="h-full rounded-full bg-indigo-400" :style="{ width: `${parseFloat(u.indice_prorrateo) * 6}%` }" />
                  </div>
                  <span class="tabular font-semibold text-slate-700 w-12 text-right">{{ parseFloat(u.indice_prorrateo).toFixed(2) }}%</span>
                </div>
              </td>
              <td class="px-5 py-3.5">
                <UiBadge :variant="u.activa ? 'success' : 'neutral'">
                  {{ u.activa ? "Activa" : "Inactiva" }}
                </UiBadge>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Cocheras -->
      <div class="bg-white rounded-2xl border border-slate-100 shadow-card overflow-hidden">
        <div class="flex items-center gap-3 px-5 py-4 border-b border-slate-100">
          <div class="w-2 h-2 rounded-full bg-slate-300" />
          <h2 class="text-sm font-semibold text-slate-900">Cocheras</h2>
          <span class="text-xs text-slate-400 tabular">{{ cocheras.length }} unidades</span>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-0 divide-x divide-y divide-slate-50">
          <div
            v-for="u in cocheras"
            :key="u.id"
            class="p-4 hover:bg-slate-50/40 transition-colors text-center"
          >
            <div class="w-10 h-10 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-center text-sm font-bold text-slate-600 mx-auto mb-2">
              {{ u.numero }}
            </div>
            <p class="text-xs font-semibold text-slate-700">{{ u.codigo }}</p>
            <p class="text-xs tabular text-slate-400 mt-0.5">{{ parseFloat(u.indice_prorrateo).toFixed(2) }}%</p>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "admin", middleware: "auth" })

interface Unidad {
  id: string; tipo: string; numero: string; piso: string | null
  indice_prorrateo: string; activa: boolean; codigo: string
}

const api = useApi()
const cargando = ref(true)
const unidades = ref<Unidad[]>([])

onMounted(async () => {
  unidades.value = await api.get<Unidad[]>("/api/v1/unidades")
  cargando.value = false
})

const departamentos = computed(() =>
  unidades.value.filter(u => u.tipo === "departamento").sort((a, b) => +a.numero - +b.numero)
)
const cocheras = computed(() =>
  unidades.value.filter(u => u.tipo === "cochera").sort((a, b) => a.numero.localeCompare(b.numero))
)
const sumaIndices = computed(() =>
  unidades.value.reduce((s, u) => s + parseFloat(u.indice_prorrateo), 0)
)
</script>
