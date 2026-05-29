<template>
  <div class="p-6 max-w-5xl mx-auto">
    <div v-if="cargando" class="text-center py-12 text-gray-400">Cargando...</div>

    <template v-else-if="periodo">
      <!-- Encabezado -->
      <div class="flex items-center gap-4 mb-6">
        <NuxtLink to="/admin/periodos" class="text-blue-700 text-sm hover:underline">← Periodos</NuxtLink>
        <div class="flex-1">
          <h1 class="text-2xl font-bold text-gray-800">{{ periodo.etiqueta }}</h1>
          <span :class="claseEstado(periodo.estado)" class="text-xs px-2 py-0.5 rounded-full font-medium">
            {{ periodo.estado }}
          </span>
        </div>
        <div class="flex gap-2">
          <button
            v-if="periodo.estado === 'abierto'"
            @click="liquidar"
            :disabled="accionando"
            class="bg-blue-700 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-800 disabled:opacity-50"
          >
            Liquidar
          </button>
          <button
            v-if="periodo.estado === 'liquidado'"
            @click="cambiarEstado('cerrado')"
            :disabled="accionando"
            class="bg-green-700 text-white px-4 py-2 rounded-lg text-sm hover:bg-green-800 disabled:opacity-50"
          >
            Cerrar periodo
          </button>
          <button
            v-if="periodo.estado === 'liquidado'"
            @click="cambiarEstado('abierto')"
            :disabled="accionando"
            class="border border-gray-300 px-4 py-2 rounded-lg text-sm hover:bg-gray-50 disabled:opacity-50"
          >
            Reabrir
          </button>
        </div>
      </div>

      <!-- Gastos -->
      <div class="bg-white rounded-xl border border-gray-200 mb-6">
        <div class="flex items-center justify-between p-4 border-b">
          <h2 class="font-semibold text-gray-800">Gastos del periodo</h2>
          <button
            v-if="periodo.estado === 'abierto'"
            @click="mostrarModalGasto = true"
            class="text-blue-700 text-sm hover:underline"
          >
            + Agregar gasto
          </button>
        </div>
        <div class="divide-y">
          <div v-for="gasto in gastos" :key="gasto.id" class="flex items-center justify-between px-4 py-3">
            <div>
              <p class="text-sm font-medium text-gray-800">{{ gasto.descripcion }}</p>
              <p class="text-xs text-gray-500">{{ gasto.categoria }} · {{ gasto.tipo }}</p>
            </div>
            <div class="flex items-center gap-3">
              <span class="font-medium text-gray-800">{{ formatearMonto(gasto.monto) }}</span>
              <button
                v-if="periodo.estado === 'abierto'"
                @click="eliminarGasto(gasto.id)"
                class="text-red-500 text-xs hover:underline"
              >
                Eliminar
              </button>
            </div>
          </div>
          <p v-if="!gastos.length" class="text-center text-gray-400 py-6 text-sm">
            No hay gastos registrados
          </p>
        </div>
        <div v-if="gastos.length" class="p-4 border-t bg-gray-50 flex justify-between text-sm">
          <span class="font-medium">Total</span>
          <span class="font-semibold">{{ formatearMonto(totalGastos) }}</span>
        </div>
      </div>

      <!-- Liquidacion -->
      <div v-if="liquidacion" class="bg-white rounded-xl border border-gray-200">
        <div class="p-4 border-b flex items-center justify-between">
          <h2 class="font-semibold text-gray-800">Liquidacion</h2>
          <span class="text-xs text-gray-500">Generada {{ formatearFecha(liquidacion.fecha_generacion) }}</span>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-gray-50 text-gray-600 text-xs uppercase">
              <tr>
                <th class="px-4 py-3 text-left">Unidad</th>
                <th class="px-4 py-3 text-left">Propietario</th>
                <th class="px-4 py-3 text-right">Indice</th>
                <th class="px-4 py-3 text-right">Exp. Ord.</th>
                <th class="px-4 py-3 text-right">Exp. Ext.</th>
                <th class="px-4 py-3 text-right">Deuda Ord.</th>
                <th class="px-4 py-3 text-right">Deuda Ext.</th>
                <th class="px-4 py-3 text-right font-bold">Total</th>
              </tr>
            </thead>
            <tbody class="divide-y">
              <tr v-for="d in liquidacion.detalles" :key="d.id" class="hover:bg-gray-50">
                <td class="px-4 py-3 font-medium">{{ d.unidad_codigo }}</td>
                <td class="px-4 py-3 text-gray-600">{{ d.propietario_nombre || "-" }}</td>
                <td class="px-4 py-3 text-right text-gray-500">{{ d.indice }}%</td>
                <td class="px-4 py-3 text-right">{{ formatearMonto(d.monto_ordinario) }}</td>
                <td class="px-4 py-3 text-right">{{ formatearMonto(d.monto_extraordinario) }}</td>
                <td class="px-4 py-3 text-right" :class="{ 'text-red-600': parseFloat(d.deuda_ordinaria) > 0 }">
                  {{ formatearMonto(d.deuda_ordinaria) }}
                </td>
                <td class="px-4 py-3 text-right" :class="{ 'text-red-600': parseFloat(d.deuda_extraordinaria) > 0 }">
                  {{ formatearMonto(d.deuda_extraordinaria) }}
                </td>
                <td class="px-4 py-3 text-right font-semibold">{{ formatearMonto(d.total) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

    <!-- Modal nuevo gasto -->
    <div v-if="mostrarModalGasto" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 px-4">
      <div class="bg-white rounded-2xl p-6 w-full max-w-md shadow-xl">
        <h2 class="text-lg font-semibold mb-4">Agregar gasto</h2>
        <form @submit.prevent="agregarGasto" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Descripcion</label>
            <input v-model="nuevoGasto.descripcion" required class="w-full border rounded-lg px-3 py-2 text-sm" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Monto ($)</label>
              <input v-model.number="nuevoGasto.monto" type="number" step="0.01" min="0.01" required class="w-full border rounded-lg px-3 py-2 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Fecha</label>
              <input v-model="nuevoGasto.fecha" type="date" required class="w-full border rounded-lg px-3 py-2 text-sm" />
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Tipo</label>
              <select v-model="nuevoGasto.tipo" class="w-full border rounded-lg px-3 py-2 text-sm">
                <option value="ordinario">Ordinario</option>
                <option value="extraordinario">Extraordinario</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Categoria</label>
              <select v-model="nuevoGasto.categoria" class="w-full border rounded-lg px-3 py-2 text-sm">
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
          <p v-if="errorGasto" class="text-red-600 text-sm">{{ errorGasto }}</p>
          <div class="flex gap-3">
            <button type="button" @click="mostrarModalGasto = false" class="flex-1 border border-gray-300 rounded-lg py-2 text-sm">
              Cancelar
            </button>
            <button type="submit" :disabled="guardandoGasto" class="flex-1 bg-blue-700 text-white rounded-lg py-2 text-sm disabled:opacity-50">
              {{ guardandoGasto ? "Guardando..." : "Guardar" }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "admin", middleware: "auth" })

interface Periodo {
  id: string; mes: number; anio: number; estado: string; etiqueta: string; fecha_cierre: string | null
}
interface Gasto {
  id: string; descripcion: string; monto: string; tipo: string; categoria: string; fecha: string
}
interface DetalleExpensa {
  id: string; unidad_codigo: string; propietario_nombre: string | null; indice: string
  monto_ordinario: string; monto_extraordinario: string; deuda_ordinaria: string
  deuda_extraordinaria: string; total: string; unidad_id: string
}
interface Liquidacion {
  id: string; fecha_generacion: string; gasto_total_ordinario: string
  gasto_total_extraordinario: string; detalles: DetalleExpensa[]
}

const route = useRoute()
const api = useApi()
const cargando = ref(true)
const accionando = ref(false)
const periodo = ref<Periodo | null>(null)
const gastos = ref<Gasto[]>([])
const liquidacion = ref<Liquidacion | null>(null)
const mostrarModalGasto = ref(false)
const guardandoGasto = ref(false)
const errorGasto = ref("")
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

async function agregarGasto() {
  errorGasto.value = ""
  guardandoGasto.value = true
  try {
    const g = await api.post<Gasto>(`/api/v1/periodos/${route.params.id}/gastos`, nuevoGasto.value)
    gastos.value.push(g)
    mostrarModalGasto.value = false
    nuevoGasto.value = { descripcion: "", monto: 0, fecha: "", tipo: "ordinario", categoria: "servicios" }
  } catch {
    errorGasto.value = "No se pudo agregar el gasto"
  } finally {
    guardandoGasto.value = false
  }
}

async function eliminarGasto(id: string) {
  await api.del(`/api/v1/periodos/${route.params.id}/gastos/${id}`)
  gastos.value = gastos.value.filter(g => g.id !== id)
}

async function liquidar() {
  accionando.value = true
  try {
    liquidacion.value = await api.post<Liquidacion>(`/api/v1/periodos/${route.params.id}/liquidar`, {})
    periodo.value!.estado = "liquidado"
  } catch (e: any) {
    alert(e?.data?.detail || "Error al liquidar")
  } finally {
    accionando.value = false
  }
}

async function cambiarEstado(estado: string) {
  accionando.value = true
  try {
    periodo.value = await api.patch<Periodo>(`/api/v1/periodos/${route.params.id}/estado`, { estado })
    if (estado === "abierto") liquidacion.value = null
  } finally {
    accionando.value = false
  }
}

function claseEstado(estado: string) {
  return { abierto: "bg-yellow-100 text-yellow-800", liquidado: "bg-blue-100 text-blue-800", cerrado: "bg-green-100 text-green-800" }[estado] || ""
}

function formatearMonto(v: string | number) {
  return new Intl.NumberFormat("es-AR", { style: "currency", currency: "ARS" }).format(parseFloat(String(v)))
}

function formatearFecha(f: string) {
  return new Date(f).toLocaleDateString("es-AR")
}
</script>
