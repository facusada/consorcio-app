<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-blue-800">Consorcio App</h1>
        <p class="text-gray-500 mt-2">Gestion del consorcio residencial</p>
      </div>

      <form @submit.prevent="iniciarSesion" class="bg-white rounded-2xl shadow p-8 space-y-6">
        <h2 class="text-xl font-semibold text-gray-800">Iniciar sesion</h2>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            v-model="email"
            type="email"
            required
            class="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="admin@consorcio.local"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Contrasena</label>
          <input
            v-model="contrasena"
            type="password"
            required
            class="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <p v-if="error" class="text-red-600 text-sm">{{ error }}</p>

        <button
          type="submit"
          :disabled="cargando"
          class="w-full bg-blue-700 hover:bg-blue-800 disabled:opacity-50 text-white font-medium py-2.5 rounded-lg transition"
        >
          {{ cargando ? "Ingresando..." : "Ingresar" }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
const auth = useAuthStore()
const email = ref("")
const contrasena = ref("")
const error = ref("")
const cargando = ref(false)

async function iniciarSesion() {
  error.value = ""
  cargando.value = true
  try {
    await auth.login(email.value, contrasena.value)
    await navigateTo("/admin/periodos")
  } catch {
    error.value = "Email o contrasena incorrectos"
  } finally {
    cargando.value = false
  }
}
</script>
