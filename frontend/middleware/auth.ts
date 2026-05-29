export default defineNuxtRouteMiddleware(() => {
  const auth = useAuthStore()
  if (!auth.autenticado) {
    return navigateTo("/login")
  }
})
