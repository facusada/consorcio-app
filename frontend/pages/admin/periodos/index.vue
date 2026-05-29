<template>
  <div class="p-8 max-w-5xl mx-auto">

    <!-- Header -->
    <div class="flex items-start justify-between mb-8">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Periodos</h1>
        <p class="text-slate-500 text-sm mt-1">Gestion mensual de gastos y liquidaciones</p>
      </div>
      <UiButton @click="abrirModal = true">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
        </svg>
        Nuevo periodo
      </UiButton>
    </div>

    <!-- Stats -->
    <div v-if="!cargando && periodos.length" class="grid grid-cols-3 gap-4 mb-8">
      <UiStatCard
        label="Total periodos"
        :valor="String(periodos.length)"
        icon="📅"
        icon-bg="bg-indigo-50 text-indigo-600"
      />
      <UiStatCard
        label="Liquidados"
        :valor="String(periodos.filter(p => p.estado === 'liquidado').length)"
        icon="✅"
        icon-bg="bg-emerald-50 text-emerald-600"
      />
      <UiStatCard
        label="Cerrados"
        :valor="String(periodos.filter(p => p.estado === 'cerrado').length)"
        icon="🔒"
        icon-bg="bg-slate-100 text-slate-500"
      />
    </div>

    <!-- Loading skeleton -->
    <div v-if="cargando" class="space-y-3">
      <UiSkeleton v-for="i in 4" :key="i" height="64px" />
    </div>

    <!-- Lista -->
    <div v-else-if="periodos.length" class="bg-white rounded-2xl border border-slate-100 shadow-card overflow-hidden stagger">
      <div
        v-for="(periodo, i) in periodos"
        :key="periodo.id"
        class="flex items-center justify-between px-5 py-4 hover:bg-slate-50/60 transition-colors cursor-pointer"
        :class="i !== 0 ? 'border-t border-slate-100' : ''"
        @click="navigateTo(`/admin/periodos/${periodo.id}`)"
      >
        <div class="flex items-center gap-4">
          <!-- Month icon -->
          <div class="w-10 h-10 rounded-xl flex items-center justify-center text-xs font-bold shrink-0"
            :class="colorMes(periodo.estado)">
            {{ periodo.mes }}
          </div>
          <div>
            <p class="text-sm font-semibold text-slate-900">{{ periodo.etiqueta }}</p>
            <p v-if="periodo.fecha_cierre" class="text-xs text-slate-400 mt-0.5">
              Cerrado el {{ formatFecha(periodo.fecha_cierre) }}
            </p>
            <p v-else-if="periodo.estado === 'liquidado'" class="text-xs text-slate-400 mt-0.5">
              Pendiente de cierre
            </p>
            <p v-else class="text-xs text-slate-400 mt-0.5">En progreso</p>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <UiBadge :variant="variantEstado(periodo.estado)" dot>
            {{ periodo.estado }}
          </UiBadge>
          <svg class="w-4 h-4 text-slate-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
          </svg>
        </div>
      </div>
    </div>

    <!-- Empty state -->
    <div v-else class="bg-white rounded-2xl border border-slate-100 shadow-card">
      <UiEmptyState
        icon="📅"
        titulo="Sin periodos todavia"
        descripcion="Crea el primer periodo para empezar a cargar gastos y liquidar expensas."
      >
        <UiButton class="mt-4" @click="abrirModal = true">
          Crear primer periodo
        </UiButton>
      </UiEmptyState>
    </div>

    <!-- Modal nuevo periodo -->
    <UiModal v-model="abrirModal" titulo="Nuevo periodo" max-width="max-w-sm">
      <form @submit.prevent="crearPeriodo" class="space-y-5">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-semibold text-slate-600 mb-2 uppercase tracking-wide">Mes</label>
            <select
              v-model="nuevoMes"
              class="w-full px-3 py-2.5 text-sm rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            >
              <option v-for="m in 12" :key="m" :value="m">{{ nombreMes(m) }}</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-600 mb-2 uppercase tracking-wide">Año</label>
            <input
              v-model.number="nuevoAnio"
              type="number"
              min="2020"
              max="2099"
              class="w-full px-3 py-2.5 text-sm rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
          </div>
        </div>

        <Transition name="error">
          <p v-if="errorCrear" class="text-sm text-red-600 bg-red-50 border border-red-100 px-3 py-2.5 rounded-xl">
            {{ errorCrear }}
          </p>
        </Transition>

        <div class="flex gap-3 pt-1">
          <UiButton variant="secondary" size="md" class="flex-1" type="button" @click="abrirModal = false">
            Cancelar
          </UiButton>
          <UiButton size="md" class="flex-1" type="submit" :loading="creando">
            Crear periodo
          </UiButton>
        </div>
      </form>
    </UiModal>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "admin", middleware: "auth" })

interface Periodo {
  id: string; mes: number; anio: number; estado: string; etiqueta: string; fecha_cierre: string | null
}

const api = useApi()
const periodos = ref<Periodo[]>([])
const cargando = ref(true)
const abrirModal = ref(false)
const nuevoMes = ref(new Date().getMonth() + 1)
const nuevoAnio = ref(new Date().getFullYear())
const creando = ref(false)
const errorCrear = ref("")

onMounted(async () => {
  try {
    periodos.value = await api.get<Periodo[]>("/api/v1/periodos")
  } catch {}
  cargando.value = false
})

async function crearPeriodo() {
  errorCrear.value = ""
  creando.value = true
  try {
    const nuevo = await api.post<Periodo>("/api/v1/periodos", { mes: nuevoMes.value, anio: nuevoAnio.value })
    periodos.value.unshift(nuevo)
    abrirModal.value = false
  } catch {
    errorCrear.value = "Ya existe un periodo para ese mes y año"
  } finally {
    creando.value = false
  }
}

function variantEstado(estado: string) {
  return { abierto: "warning" as const, liquidado: "info" as const, cerrado: "success" as const }[estado] ?? "neutral" as const
}

function colorMes(estado: string) {
  return {
    abierto: "bg-amber-50 text-amber-600",
    liquidado: "bg-indigo-50 text-indigo-600",
    cerrado: "bg-emerald-50 text-emerald-700",
  }[estado] ?? "bg-slate-100 text-slate-500"
}

function nombreMes(m: number) {
  return ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"][m]
}

function formatFecha(f: string) {
  return new Date(f).toLocaleDateString("es-AR", { day: "numeric", month: "short", year: "numeric" })
}
</script>

<style scoped>
.error-enter-active { transition: all 200ms ease; }
.error-leave-active { transition: all 150ms ease; }
.error-enter-from, .error-leave-to { opacity: 0; transform: translateY(-4px); }
</style>
