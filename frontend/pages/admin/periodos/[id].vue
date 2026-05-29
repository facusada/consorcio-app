<template>
  <div class="p-8 max-w-6xl mx-auto">

    <!-- Loading -->
    <div v-if="cargando" class="space-y-6">
      <UiSkeleton height="36px" width="240px" />
      <div class="grid grid-cols-3 gap-4">
        <UiSkeleton v-for="i in 3" :key="i" height="96px" />
      </div>
      <UiSkeleton height="400px" />
    </div>

    <template v-else-if="periodo">

      <!-- Breadcrumb + header -->
      <div class="flex items-center gap-2 text-sm text-slate-400 mb-6">
        <NuxtLink to="/admin/periodos" class="hover:text-slate-700 transition-colors">Periodos</NuxtLink>
        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
        </svg>
        <span class="text-slate-700 font-medium">{{ periodo.etiqueta }}</span>
      </div>

      <div class="flex items-start justify-between mb-6">
        <div class="flex items-center gap-3">
          <h1 class="text-2xl font-bold text-slate-900 tracking-tight">{{ periodo.etiqueta }}</h1>
          <UiBadge :variant="variantEstado(periodo.estado)" dot>{{ periodo.estado }}</UiBadge>
        </div>

        <!-- Acciones -->
        <div class="flex gap-2">
          <template v-if="periodo.estado === 'liquidado'">
            <UiButton variant="secondary" size="sm" :loading="accionando" @click="cambiarEstado('abierto')">
              Reabrir
            </UiButton>
            <UiButton variant="secondary" size="sm" @click="descargarPdf">
              <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
              </svg>
              PDF
            </UiButton>
            <UiButton size="sm" :loading="accionando" @click="cambiarEstado('cerrado')">
              Cerrar periodo
            </UiButton>
          </template>
          <template v-else-if="periodo.estado === 'abierto'">
            <UiButton size="sm" :loading="liquidando" @click="liquidar">
              <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Liquidar
            </UiButton>
          </template>
          <template v-else-if="periodo.estado === 'cerrado'">
            <UiButton variant="secondary" size="sm" @click="descargarPdf">
              <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
              </svg>
              Descargar PDF
            </UiButton>
          </template>
        </div>
      </div>

      <!-- Error bar -->
      <Transition name="error">
        <div v-if="errorAccion" class="flex items-center gap-2.5 px-4 py-3 mb-5 bg-red-50 border border-red-100 rounded-xl">
          <svg class="w-4 h-4 text-red-500 shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-5a.75.75 0 01.75.75v4.5a.75.75 0 01-1.5 0v-4.5A.75.75 0 0110 5zm0 10a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
          </svg>
          <p class="text-sm text-red-700">{{ errorAccion }}</p>
        </div>
      </Transition>

      <!-- Stats cards -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <UiStatCard
          label="Gastos ordinarios"
          :valor="formatMonto(totalOrdinario)"
          icon="📋"
          icon-bg="bg-indigo-50"
        />
        <UiStatCard
          label="Gastos extraordinarios"
          :valor="formatMonto(totalExtraordinario)"
          icon="⚡"
          icon-bg="bg-amber-50"
        />
        <UiStatCard
          label="Total a cobrar"
          :valor="formatMonto(totalLiquidacion)"
          icon="💰"
          icon-bg="bg-emerald-50"
        />
        <UiStatCard
          label="Unidades"
          :valor="liquidacion ? String(liquidacion.detalles.length) : '13'"
          icon="🏢"
          icon-bg="bg-slate-50"
        />
      </div>

      <!-- Grid: gastos + liquidacion -->
      <div class="grid lg:grid-cols-5 gap-6">

        <!-- Gastos (sidebar) -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-2xl border border-slate-100 shadow-card overflow-hidden">
            <div class="flex items-center justify-between px-5 py-4 border-b border-slate-100">
              <h2 class="text-sm font-semibold text-slate-900">Gastos del periodo</h2>
              <UiButton
                v-if="periodo.estado === 'abierto'"
                variant="ghost"
                size="sm"
                @click="abrirModalGasto = true"
              >
                <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                </svg>
                Agregar
              </UiButton>
            </div>

            <div v-if="gastos.length" class="divide-y divide-slate-50">
              <div
                v-for="gasto in gastos"
                :key="gasto.id"
                class="px-5 py-3.5 flex items-start justify-between gap-3 group"
              >
                <div class="min-w-0">
                  <p class="text-sm text-slate-900 font-medium leading-tight truncate">{{ gasto.descripcion }}</p>
                  <div class="flex items-center gap-2 mt-1">
                    <span class="text-xs text-slate-400">{{ gasto.categoria }}</span>
                    <span class="text-slate-200">·</span>
                    <span class="text-xs" :class="gasto.tipo === 'ordinario' ? 'text-indigo-500' : 'text-amber-500'">
                      {{ gasto.tipo }}
                    </span>
                  </div>
                </div>
                <div class="flex items-center gap-2 shrink-0">
                  <span class="text-sm font-semibold tabular text-slate-800">{{ formatMonto(gasto.monto) }}</span>
                  <button
                    v-if="periodo.estado === 'abierto'"
                    @click="eliminarGasto(gasto.id)"
                    class="opacity-0 group-hover:opacity-100 w-6 h-6 flex items-center justify-center rounded-lg text-slate-300 hover:text-red-500 hover:bg-red-50 transition-all"
                  >
                    <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                    </svg>
                  </button>
                </div>
              </div>

              <!-- Total -->
              <div class="px-5 py-3.5 bg-slate-50 flex items-center justify-between">
                <span class="text-xs font-bold text-slate-500 uppercase tracking-wide">Total</span>
                <span class="text-sm font-bold tabular text-slate-900">{{ formatMonto(totalGastos) }}</span>
              </div>
            </div>

            <UiEmptyState
              v-else
              icon="📋"
              titulo="Sin gastos"
              descripcion="Agrega los gastos del periodo para poder liquidar."
            />
          </div>
        </div>

        <!-- Tabla liquidacion -->
        <div class="lg:col-span-3">
          <div v-if="liquidacion" class="bg-white rounded-2xl border border-slate-100 shadow-card overflow-hidden">
            <div class="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
              <h2 class="text-sm font-semibold text-slate-900">Liquidacion por unidad</h2>
              <span class="text-xs text-slate-400">{{ formatFecha(liquidacion.fecha_generacion) }}</span>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-xs">
                <thead>
                  <tr class="bg-slate-50 border-b border-slate-100">
                    <th class="px-4 py-3 text-left font-semibold text-slate-500 uppercase tracking-wide">Unidad</th>
                    <th class="px-4 py-3 text-left font-semibold text-slate-500 uppercase tracking-wide hidden lg:table-cell">Propietario</th>
                    <th class="px-4 py-3 text-right font-semibold text-slate-500 uppercase tracking-wide">Exp. Ord.</th>
                    <th v-if="tieneExtraordinarios" class="px-4 py-3 text-right font-semibold text-slate-500 uppercase tracking-wide">Exp. Ext.</th>
                    <th class="px-4 py-3 text-right font-semibold text-slate-500 uppercase tracking-wide">Deuda</th>
                    <th class="px-4 py-3 text-right font-semibold text-slate-500 uppercase tracking-wide">Total</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-50">
                  <tr
                    v-for="d in liquidacion.detalles"
                    :key="d.id"
                    class="hover:bg-slate-50/60 transition-colors"
                  >
                    <td class="px-4 py-3">
                      <div class="flex items-center gap-2">
                        <span class="w-1.5 h-1.5 rounded-full shrink-0"
                          :class="d.unidad_tipo === 'departamento' ? 'bg-indigo-400' : 'bg-slate-300'" />
                        <span class="font-semibold text-slate-800">{{ d.unidad_codigo }}</span>
                      </div>
                    </td>
                    <td class="px-4 py-3 text-slate-500 hidden lg:table-cell">{{ d.propietario_nombre || "—" }}</td>
                    <td class="px-4 py-3 text-right tabular text-slate-700">{{ formatMonto(d.monto_ordinario) }}</td>
                    <td v-if="tieneExtraordinarios" class="px-4 py-3 text-right tabular text-slate-700">{{ formatMonto(d.monto_extraordinario) }}</td>
                    <td class="px-4 py-3 text-right tabular" :class="parseFloat(d.deuda_ordinaria) > 0 ? 'text-red-600 font-semibold' : 'text-slate-400'">
                      {{ formatMonto(parseFloat(d.deuda_ordinaria) + parseFloat(d.deuda_extraordinaria)) }}
                    </td>
                    <td class="px-4 py-3 text-right tabular font-bold text-slate-900">{{ formatMonto(d.total) }}</td>
                  </tr>
                </tbody>
                <tfoot>
                  <tr class="bg-slate-900">
                    <td class="px-4 py-3 text-xs font-bold text-slate-200 uppercase tracking-wide" colspan="2">Total general</td>
                    <td class="px-4 py-3 text-right tabular font-bold text-white text-xs">{{ formatMonto(liquidacion.gasto_total_ordinario) }}</td>
                    <td v-if="tieneExtraordinarios" class="px-4 py-3 text-right tabular font-bold text-white text-xs">{{ formatMonto(liquidacion.gasto_total_extraordinario) }}</td>
                    <td class="px-4 py-3 text-right tabular font-bold text-red-300 text-xs">{{ formatMonto(totalDeuda) }}</td>
                    <td class="px-4 py-3 text-right tabular font-bold text-white text-xs">{{ formatMonto(totalLiquidacion) }}</td>
                  </tr>
                </tfoot>
              </table>
            </div>
          </div>

          <div v-else-if="periodo.estado === 'abierto'" class="bg-white rounded-2xl border border-slate-100 shadow-card">
            <UiEmptyState
              icon="⚡"
              titulo="Sin liquidacion"
              descripcion="Carga los gastos del periodo y luego presiona Liquidar para calcular las expensas."
            />
          </div>
        </div>
      </div>
    </template>

    <!-- Modal gasto -->
    <UiModal v-model="abrirModalGasto" titulo="Agregar gasto" max-width="max-w-md">
      <form @submit.prevent="agregarGasto" class="space-y-4">
        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-2 uppercase tracking-wide">Descripcion</label>
          <input
            v-model="nuevoGasto.descripcion"
            required
            minlength="3"
            placeholder="Ej: Servicio de limpieza"
            class="w-full px-4 py-2.5 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-semibold text-slate-600 mb-2 uppercase tracking-wide">Monto ($)</label>
            <input
              v-model.number="nuevoGasto.monto"
              type="number"
              step="0.01"
              min="0.01"
              required
              placeholder="0.00"
              class="w-full px-4 py-2.5 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent font-mono"
            />
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-600 mb-2 uppercase tracking-wide">Fecha</label>
            <input
              v-model="nuevoGasto.fecha"
              type="date"
              required
              class="w-full px-4 py-2.5 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-semibold text-slate-600 mb-2 uppercase tracking-wide">Tipo</label>
            <select v-model="nuevoGasto.tipo" class="w-full px-4 py-2.5 text-sm rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <option value="ordinario">Ordinario</option>
              <option value="extraordinario">Extraordinario</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-600 mb-2 uppercase tracking-wide">Categoria</label>
            <select v-model="nuevoGasto.categoria" class="w-full px-4 py-2.5 text-sm rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <option value="servicios">Servicios</option>
              <option value="limpieza">Limpieza</option>
              <option value="mantenimiento">Mantenimiento</option>
              <option value="seguros">Seguros</option>
              <option value="impuestos">Impuestos</option>
              <option value="honorarios">Honorarios</option>
              <option value="extraordinario">Extraordinario</option>
              <option value="otros">Otros</option>
            </select>
          </div>
        </div>

        <Transition name="error">
          <p v-if="errorGasto" class="text-sm text-red-600 bg-red-50 border border-red-100 px-3 py-2.5 rounded-xl">
            {{ errorGasto }}
          </p>
        </Transition>

        <div class="flex gap-3 pt-1">
          <UiButton variant="secondary" class="flex-1" type="button" @click="abrirModalGasto = false">Cancelar</UiButton>
          <UiButton class="flex-1" type="submit" :loading="guardandoGasto">Guardar gasto</UiButton>
        </div>
      </form>
    </UiModal>

  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "admin", middleware: "auth" })

interface Periodo { id: string; mes: number; anio: number; estado: string; etiqueta: string; fecha_cierre: string | null }
interface Gasto { id: string; descripcion: string; monto: string; tipo: string; categoria: string; fecha: string }
interface DetalleExpensa {
  id: string; unidad_codigo: string; unidad_tipo: string; propietario_nombre: string | null
  indice: string; monto_ordinario: string; monto_extraordinario: string
  deuda_ordinaria: string; deuda_extraordinaria: string; total: string; unidad_id: string
}
interface Liquidacion {
  id: string; fecha_generacion: string; gasto_total_ordinario: string
  gasto_total_extraordinario: string; detalles: DetalleExpensa[]
}

const route = useRoute()
const config = useRuntimeConfig()
const auth = useAuthStore()
const api = useApi()

const cargando = ref(true)
const accionando = ref(false)
const liquidando = ref(false)
const periodo = ref<Periodo | null>(null)
const gastos = ref<Gasto[]>([])
const liquidacion = ref<Liquidacion | null>(null)
const abrirModalGasto = ref(false)
const guardandoGasto = ref(false)
const errorGasto = ref("")
const errorAccion = ref("")

const nuevoGasto = ref({ descripcion: "", monto: 0, fecha: "", tipo: "ordinario", categoria: "servicios" })

onMounted(async () => {
  await cargarDatos()
  cargando.value = false
})

async function cargarDatos() {
  const id = route.params.id as string
  ;[periodo.value, gastos.value] = await Promise.all([
    api.get<Periodo>(`/api/v1/periodos/${id}`),
    api.get<Gasto[]>(`/api/v1/periodos/${id}/gastos`),
  ])
  if (periodo.value?.estado !== "abierto") {
    try {
      liquidacion.value = await api.get<Liquidacion>(`/api/v1/periodos/${id}/liquidacion`)
    } catch {}
  }
}

const totalGastos = computed(() => gastos.value.reduce((s, g) => s + parseFloat(g.monto), 0))
const totalOrdinario = computed(() => gastos.value.filter(g => g.tipo === "ordinario").reduce((s, g) => s + parseFloat(g.monto), 0))
const totalExtraordinario = computed(() => gastos.value.filter(g => g.tipo === "extraordinario").reduce((s, g) => s + parseFloat(g.monto), 0))
const tieneExtraordinarios = computed(() => parseFloat(liquidacion.value?.gasto_total_extraordinario ?? "0") > 0)
const totalDeuda = computed(() => liquidacion.value?.detalles.reduce((s, d) => s + parseFloat(d.deuda_ordinaria) + parseFloat(d.deuda_extraordinaria), 0) ?? 0)
const totalLiquidacion = computed(() => liquidacion.value?.detalles.reduce((s, d) => s + parseFloat(d.total), 0) ?? 0)

async function agregarGasto() {
  errorGasto.value = ""
  guardandoGasto.value = true
  try {
    const g = await api.post<Gasto>(`/api/v1/periodos/${route.params.id}/gastos`, nuevoGasto.value)
    gastos.value.push(g)
    abrirModalGasto.value = false
    nuevoGasto.value = { descripcion: "", monto: 0, fecha: "", tipo: "ordinario", categoria: "servicios" }
  } catch {
    errorGasto.value = "No se pudo guardar el gasto"
  } finally {
    guardandoGasto.value = false
  }
}

async function eliminarGasto(id: string) {
  await api.del(`/api/v1/periodos/${route.params.id}/gastos/${id}`)
  gastos.value = gastos.value.filter(g => g.id !== id)
}

async function liquidar() {
  errorAccion.value = ""
  liquidando.value = true
  try {
    liquidacion.value = await api.post<Liquidacion>(`/api/v1/periodos/${route.params.id}/liquidar`, {})
    periodo.value!.estado = "liquidado"
  } catch (e: any) {
    errorAccion.value = e?.data?.detail ?? "Error al liquidar el periodo"
  } finally {
    liquidando.value = false
  }
}

async function cambiarEstado(estado: string) {
  errorAccion.value = ""
  accionando.value = true
  try {
    periodo.value = await api.patch<Periodo>(`/api/v1/periodos/${route.params.id}/estado`, { estado })
    if (estado === "abierto") liquidacion.value = null
  } catch (e: any) {
    errorAccion.value = e?.data?.detail ?? "No se pudo cambiar el estado"
  } finally {
    accionando.value = false
  }
}

function descargarPdf() {
  const url = `${config.public.apiBase}/api/v1/periodos/${route.params.id}/liquidacion/pdf`
  const a = document.createElement("a")
  a.href = url
  a.setAttribute("download", `liquidacion-${periodo.value?.etiqueta?.replace(" ", "-")}.pdf`)
  const headers = new Headers({ Authorization: `Bearer ${auth.token}` })
  fetch(url, { headers }).then(r => r.blob()).then(blob => {
    a.href = URL.createObjectURL(blob)
    a.click()
    URL.revokeObjectURL(a.href)
  })
}

function variantEstado(estado: string) {
  return { abierto: "warning" as const, liquidado: "info" as const, cerrado: "success" as const }[estado] ?? "neutral" as const
}

function formatMonto(v: string | number) {
  return new Intl.NumberFormat("es-AR", { style: "currency", currency: "ARS", minimumFractionDigits: 2 }).format(parseFloat(String(v)))
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
