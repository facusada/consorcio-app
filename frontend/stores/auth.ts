import { defineStore } from "pinia"

interface UsuarioActual {
  id: string
  email: string
  rol: string
  nombre_completo: string
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: null as string | null,
    usuario: null as UsuarioActual | null,
  }),

  getters: {
    autenticado: (state) => !!state.token,
    esAdmin: (state) => state.usuario?.rol === "admin",
  },

  actions: {
    async login(email: string, contrasena: string) {
      const config = useRuntimeConfig()
      const { data, error } = await useFetch<{ access_token: string }>(
        `${config.public.apiBase}/api/v1/auth/login`,
        {
          method: "POST",
          body: { email, contrasena },
        }
      )
      if (error.value || !data.value) {
        throw new Error("Credenciales incorrectas")
      }
      this.token = data.value.access_token
      await this.cargarUsuario()
    },

    async cargarUsuario() {
      if (!this.token) return
      const config = useRuntimeConfig()
      const { data } = await useFetch<UsuarioActual>(
        `${config.public.apiBase}/api/v1/auth/me`,
        {
          headers: { Authorization: `Bearer ${this.token}` },
        }
      )
      if (data.value) this.usuario = data.value
    },

    cerrarSesion() {
      this.token = null
      this.usuario = null
      navigateTo("/login")
    },
  },

  persist: true,
})
