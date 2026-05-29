<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h1 class="text-2xl font-bold text-gray-800 mb-6">Unidades funcionales</h1>

    <div v-if="cargando" class="text-center py-12 text-gray-400">Cargando...</div>

    <template v-else>
      <!-- Resumen de indices -->
      <div class="bg-blue-50 border border-blue-200 rounded-xl p-4 mb-6 flex items-center justify-between">
        <p class="text-sm text-blue-800">
          <span class="font-semibold">Suma de indices:</span> {{ sumaIndices.toFixed(2) }}%
        </p>
        <span
          :class="Math.abs(sumaIndices - 100) < 0.01 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
          class="text-xs px-2 py-1 rounded-full font-medium"
        >
          {{ Math.abs(sumaIndices - 100) < 0.01 ? "✓ Suma = 100%" : "⚠ Suma ≠ 100%" }}
        </span>
      </div>

      <!-- Tabla departamentos -->
      <div class="bg-white rounded-xl border border-gray-200 mb-6 overflow-hidden">
        <div class="px-4 py-3 border-b bg-gray-50">
          <h2 class="font-semibold text-gray-700 text-sm">Departamentos</h2>
        </div>
        <table class="w-full text-sm">
          <thead>
            <tr class="text-xs text-gray-500 uppercase border-b">
              <th class="px-4 py-3 text-left">Unidad</th>
              <th class="px-4 py-3 text-left">Piso</th>
              <th class="px-4 py-3 text-right">Indice (%)</th>
              <th class="px-4 py-3 text-left">Estado</th>
              <th class="px-4 py-3 text-left">Propietario</th>
            </tr>
          </thead>
          <tbody class="divide-y">
            <tr v-for="u in departamentos" :key="u.id" class="hover:bg-gray-50">
              <td class="px-4 py-3 font-medium">{{ u.codigo }}</td>
              <td class="px-4 py-3 text-gray-500">{{ u.piso || "-" }}</td>
              <td class="px-4 py-3 text-right font-mono">{{ parseFloat(u.indice_prorrateo).toFixed(2) }}</td>
              <td class="px-4 py-3">
                <span :class="u.activa ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-500'"
                  class="text-xs px-2 py-0.5 rounded-full">
                  {{ u.activa ? "Activa" : "Inactiva" }}
                </span>
              </td>
              <td class="px-4 py-3 text-gray-600">-</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Tabla cocheras -->
      <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <div class="px-4 py-3 border-b bg-gray-50">
          <h2 class="font-semibold text-gray-700 text-sm">Cocheras</h2>
        </div>
        <table class="w-full text-sm">
          <thead>
            <tr class="text-xs text-gray-500 uppercase border-b">
              <th class="px-4 py-3 text-left">Unidad</th>
              <th class="px-4 py-3 text-right">Indice (%)</th>
              <th class="px-4 py-3 text-left">Estado</th>
            </tr>
          </thead>
          <tbody class="divide-y">
            <tr v-for="u in cocheras" :key="u.id" class="hover:bg-gray-50">
              <td class="px-4 py-3 font-medium">{{ u.codigo }}</td>
              <td class="px-4 py-3 text-right font-mono">{{ parseFloat(u.indice_prorrateo).toFixed(2) }}</td>
              <td class="px-4 py-3">
                <span :class="u.activa ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-500'"
                  class="text-xs px-2 py-0.5 rounded-full">
                  {{ u.activa ? "Activa" : "Inactiva" }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "admin", middleware: "auth" })

interface Unidad {
  id: string
  tipo: string
  numero: string
  piso: string | null
  indice_prorrateo: string
  activa: boolean
  codigo: string
}

const api = useApi()
const cargando = ref(true)
const unidades = ref<Unidad[]>([])

onMounted(async () => {
  unidades.value = await api.get<Unidad[]>("/api/v1/unidades")
  cargando.value = false
})

const departamentos = computed(() =>
  unidades.value.filter(u => u.tipo === "departamento").sort((a, b) => a.numero.localeCompare(b.numero))
)
const cocheras = computed(() =>
  unidades.value.filter(u => u.tipo === "cochera").sort((a, b) => a.numero.localeCompare(b.numero))
)
const sumaIndices = computed(() =>
  unidades.value.reduce((s, u) => s + parseFloat(u.indice_prorrateo), 0)
)
</script>
