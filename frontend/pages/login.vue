<template>
  <div class="min-h-screen grid lg:grid-cols-2">

    <!-- Panel izquierdo — decorativo -->
    <div class="hidden lg:flex flex-col justify-between p-12 relative overflow-hidden"
      style="background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);">

      <!-- Noise texture overlay -->
      <div class="absolute inset-0 opacity-30"
        style="background-image: url(&quot;data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.08'/%3E%3C/svg%3E&quot;); background-size: 256px;" />

      <!-- Grid lines -->
      <div class="absolute inset-0 opacity-5"
        style="background-image: linear-gradient(#fff 1px, transparent 1px), linear-gradient(90deg, #fff 1px, transparent 1px); background-size: 48px 48px;" />

      <!-- Orbs -->
      <div class="absolute top-1/4 left-1/3 w-72 h-72 rounded-full opacity-20 blur-3xl"
        style="background: radial-gradient(circle, #6366f1, transparent)" />
      <div class="absolute bottom-1/4 right-1/4 w-56 h-56 rounded-full opacity-15 blur-3xl"
        style="background: radial-gradient(circle, #8b5cf6, transparent)" />

      <!-- Top -->
      <div class="relative z-10">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-indigo-500 flex items-center justify-center shadow-lg shadow-indigo-500/40">
            <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21" />
            </svg>
          </div>
          <span class="text-white font-bold text-lg">Consorcio App</span>
        </div>
      </div>

      <!-- Center copy -->
      <div class="relative z-10 space-y-6">
        <h1 class="text-4xl font-bold text-white leading-tight">
          Gestion integral<br />
          <span style="color: #818cf8">sin papeles</span><br />
          ni hojas de calculo
        </h1>
        <p class="text-slate-400 text-base leading-relaxed max-w-sm">
          Liquidaciones, cobranzas y comunicados de tu consorcio en un solo lugar.
        </p>

        <!-- Feature pills -->
        <div class="flex flex-wrap gap-2 pt-2">
          <span v-for="f in features" :key="f"
            class="text-xs px-3 py-1.5 rounded-full font-medium border"
            style="background: rgba(99,102,241,0.1); border-color: rgba(99,102,241,0.25); color: #a5b4fc;">
            {{ f }}
          </span>
        </div>
      </div>

      <!-- Bottom -->
      <p class="relative z-10 text-xs text-slate-600">
        Consorcio App · 13 unidades · 7 propietarios
      </p>
    </div>

    <!-- Panel derecho — login -->
    <div class="flex items-center justify-center p-8 bg-white">
      <div class="w-full max-w-sm animate-slide-up">

        <!-- Mobile logo -->
        <div class="flex items-center gap-2 mb-8 lg:hidden">
          <div class="w-8 h-8 rounded-xl bg-indigo-600 flex items-center justify-center">
            <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21" />
            </svg>
          </div>
          <span class="font-bold text-slate-900">Consorcio App</span>
        </div>

        <div class="mb-8">
          <h2 class="text-2xl font-bold text-slate-900">Bienvenido</h2>
          <p class="text-slate-500 text-sm mt-1">Ingresa con tus credenciales para continuar</p>
        </div>

        <form @submit.prevent="iniciarSesion" class="space-y-4">
          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-1.5">Email</label>
            <input
              v-model="email"
              type="text"
              autocomplete="email"
              required
              placeholder="admin@consorcio.local"
              class="w-full px-4 py-3 text-sm rounded-xl border border-slate-200 bg-slate-50 text-slate-900 placeholder-slate-400 transition-all duration-150 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent focus:bg-white"
            />
          </div>

          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-1.5">Contrasena</label>
            <div class="relative">
              <input
                v-model="contrasena"
                :type="mostrarPass ? 'text' : 'password'"
                autocomplete="current-password"
                required
                class="w-full px-4 py-3 text-sm rounded-xl border border-slate-200 bg-slate-50 text-slate-900 transition-all duration-150 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent focus:bg-white pr-11"
              />
              <button
                type="button"
                @click="mostrarPass = !mostrarPass"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors"
              >
                <svg v-if="!mostrarPass" class="w-4.5 h-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <svg v-else class="w-4.5 h-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                </svg>
              </button>
            </div>
          </div>

          <Transition name="error">
            <div v-if="error" class="flex items-center gap-2.5 px-4 py-3 bg-red-50 border border-red-100 rounded-xl">
              <svg class="w-4 h-4 text-red-500 shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-5a.75.75 0 01.75.75v4.5a.75.75 0 01-1.5 0v-4.5A.75.75 0 0110 5zm0 10a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
              </svg>
              <p class="text-sm text-red-700 font-medium">{{ error }}</p>
            </div>
          </Transition>

          <UiButton type="submit" :loading="cargando" size="lg" class="w-full mt-2">
            Ingresar
          </UiButton>

          <div class="relative my-1">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-slate-100" />
            </div>
            <div class="relative flex justify-center">
              <span class="bg-white px-3 text-xs text-slate-400">o</span>
            </div>
          </div>

          <button
            type="button"
            :disabled="cargandoInvitado"
            @click="entrarComoInvitado"
            class="w-full flex items-center justify-center gap-2 py-2.5 text-sm text-slate-500 hover:text-slate-700 border border-slate-200 rounded-xl hover:bg-slate-50 transition-colors disabled:opacity-50"
          >
            <span v-if="cargandoInvitado" class="w-3.5 h-3.5 border-2 border-slate-400 border-t-transparent rounded-full animate-spin" />
            <svg v-else class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Ver como invitado (solo lectura)
          </button>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
const auth = useAuthStore()
const email = ref("")
const contrasena = ref("")
const error = ref("")
const cargando = ref(false)
const cargandoInvitado = ref(false)
const mostrarPass = ref(false)

const features = ["Liquidacion automatica", "Exportacion PDF", "Historial de periodos", "PWA offline"]

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

async function entrarComoInvitado() {
  cargandoInvitado.value = true
  try {
    await auth.entrarComoInvitado()
    await navigateTo("/admin/periodos")
  } catch {
    error.value = "No se pudo iniciar como invitado"
  } finally {
    cargandoInvitado.value = false
  }
}
</script>

<style scoped>
.error-enter-active { transition: all 200ms ease; }
.error-leave-active { transition: all 150ms ease; }
.error-enter-from, .error-leave-to { opacity: 0; transform: translateY(-4px); }
</style>
