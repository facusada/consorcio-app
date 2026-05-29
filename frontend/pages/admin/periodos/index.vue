<template>
  <div class="p-6 max-w-4xl mx-auto">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Periodos</h1>
      <button
        @click="mostrarModalNuevo = true"
        class="bg-blue-700 text-white px-4 py-2 rounded-lg hover:bg-blue-800 text-sm font-medium"
      >
        + Nuevo periodo
      </button>
    </div>

    <div v-if="cargando" class="text-center py-12 text-gray-400">Cargando...</div>

    <div v-else class="space-y-3">
      <div
        v-for="periodo in periodos"
        :key="periodo.id"
        class="bg-white rounded-xl border border-gray-200 p-4 flex items-center justify-between hover:shadow-sm transition"
      >
        <div>
          <p class="font-semibold text-gray-800">{{ periodo.etiqueta }}</p>
          <span :class="claseEstado(periodo.estado)" class="text-xs px-2 py-0.5 rounded-full font-medium">
            {{ periodo.estado }}
          </span>
        </div>
        <NuxtLink
          :to="`/admin/periodos/${periodo.id}`"
          class="text-blue-700 text-sm hover:underline"
        >
          Ver detalle →
        </NuxtLink>
      </div>

      <p v-if="!periodos.length" class="text-center text-gray-400 py-12">
        No hay periodos creados aun
      </p>
    </div>

    <!-- Modal nuevo periodo -->
    <div v-if="mostrarModalNuevo" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 px-4">
      <div class="bg-white rounded-2xl p-6 w-full max-w-sm shadow-xl">
        <h2 class="text-lg font-semibold mb-4">Nuevo periodo</h2>
        <form @submit.prevent="crearPeriodo" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Mes</label>
              <select v-model="nuevoMes" class="w-full border rounded-lg px-3 py-2 text-sm">
                <option v-for="m in 12" :key="m" :value="m">{{ nombreMes(m) }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Ano</label>
              <input v-model.number="nuevoAnio" type="number" min="2020" class="w-full border rounded-lg px-3 py-2 text-sm" />
            </div>
          </div>
          <p v-if="errorCrear" class="text-red-600 text-sm">{{ errorCrear }}</p>
          <div class="flex gap-3">
            <button type="button" @click="mostrarModalNuevo = false" class="flex-1 border border-gray-300 rounded-lg py-2 text-sm">
              Cancelar
            </button>
            <button type="submit" :disabled="creando" class="flex-1 bg-blue-700 text-white rounded-lg py-2 text-sm disabled:opacity-50">
              {{ creando ? "Creando..." : "Crear" }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: "auth" })

interface Periodo {
  id: string
  mes: number
  anio: number
  estado: string
  etiqueta: string
  fecha_cierre: string | null
}

const api = useApi()
const periodos = ref<Periodo[]>([])
const cargando = ref(true)
const mostrarModalNuevo = ref(false)
const nuevoMes = ref(new Date().getMonth() + 1)
const nuevoAnio = ref(new Date().getFullYear())
const creando = ref(false)
const errorCrear = ref("")

onMounted(async () => {
  periodos.value = await api.get<Periodo[]>("/api/v1/periodos")
  cargando.value = false
})

async function crearPeriodo() {
  errorCrear.value = ""
  creando.value = true
  try {
    const nuevo = await api.post<Periodo>("/api/v1/periodos", {
      mes: nuevoMes.value,
      anio: nuevoAnio.value,
    })
    periodos.value.unshift(nuevo)
    mostrarModalNuevo.value = false
  } catch {
    errorCrear.value = "No se pudo crear el periodo"
  } finally {
    creando.value = false
  }
}

function claseEstado(estado: string) {
  return {
    abierto: "bg-yellow-100 text-yellow-800",
    liquidado: "bg-blue-100 text-blue-800",
    cerrado: "bg-green-100 text-green-800",
  }[estado] || "bg-gray-100 text-gray-600"
}

function nombreMes(m: number) {
  return ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"][m]
}
</script>
