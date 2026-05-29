<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h1 class="text-2xl font-bold text-gray-800 mb-6">Propietarios</h1>

    <div v-if="cargando" class="text-center py-12 text-gray-400">Cargando...</div>

    <div v-else class="space-y-3">
      <div
        v-for="p in propietarios"
        :key="p.id"
        class="bg-white rounded-xl border border-gray-200 p-4 flex items-center justify-between hover:shadow-sm transition"
      >
        <div>
          <p class="font-semibold text-gray-800">{{ p.nombre }} {{ p.apellido }}</p>
          <p v-if="p.email" class="text-xs text-gray-500 mt-0.5">{{ p.email }}</p>
        </div>
        <NuxtLink
          :to="`/admin/propietarios/${p.id}`"
          class="text-blue-700 text-sm hover:underline"
        >
          Ver unidades →
        </NuxtLink>
      </div>

      <p v-if="!propietarios.length" class="text-center text-gray-400 py-12">
        No hay propietarios registrados
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "admin", middleware: "auth" })

interface Propietario {
  id: string
  nombre: string
  apellido: string
  email: string | null
}

const api = useApi()
const cargando = ref(true)
const propietarios = ref<Propietario[]>([])

onMounted(async () => {
  const personas = await api.get<Propietario[]>("/api/v1/propietarios")
  propietarios.value = personas
  cargando.value = false
})
</script>
