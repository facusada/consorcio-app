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
    esInvitado: (state) => state.usuario?.rol === "invitado",
    puedeModificar: (state) => state.usuario?.rol === "admin",
  },

  actions: {
    async login(email: string, contrasena: string) {
      const config = useRuntimeConfig()
      const data = await $fetch<{ access_token: string }>(
        `${config.public.apiBase}/api/v1/auth/login`,
        {
          method: "POST",
          body: { email, contrasena },
        }
      )
      this.token = data.access_token
      await this.cargarUsuario()
    },

    async cargarUsuario() {
      if (!this.token) return
      const config = useRuntimeConfig()
      const data = await $fetch<UsuarioActual>(
        `${config.public.apiBase}/api/v1/auth/me`,
        {
          headers: { Authorization: `Bearer ${this.token}` },
        }
      )
      this.usuario = data
    },

    async entrarComoInvitado() {
      const config = useRuntimeConfig()
      const data = await $fetch<{ access_token: string }>(
        `${config.public.apiBase}/api/v1/auth/invitado`,
        { method: "POST" }
      )
      this.token = data.access_token
      this.usuario = {
        id: "invitado",
        email: "invitado@consorcio.local",
        rol: "invitado",
        nombre_completo: "Invitado",
      }
    },

    cerrarSesion() {
      this.token = null
      this.usuario = null
      navigateTo("/login")
    },
  },
})
