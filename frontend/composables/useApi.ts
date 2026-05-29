export function useApi() {
  const config = useRuntimeConfig()
  const auth = useAuthStore()

  const headers = () =>
    auth.token ? { Authorization: `Bearer ${auth.token}` } : {}

  async function get<T>(ruta: string): Promise<T> {
    return $fetch<T>(`${config.public.apiBase}${ruta}`, { headers: headers() })
  }

  async function post<T>(ruta: string, cuerpo: unknown): Promise<T> {
    return $fetch<T>(`${config.public.apiBase}${ruta}`, {
      method: "POST",
      headers: headers(),
      body: cuerpo,
    })
  }

  async function put<T>(ruta: string, cuerpo: unknown): Promise<T> {
    return $fetch<T>(`${config.public.apiBase}${ruta}`, {
      method: "PUT",
      headers: headers(),
      body: cuerpo,
    })
  }

  async function patch<T>(ruta: string, cuerpo: unknown): Promise<T> {
    return $fetch<T>(`${config.public.apiBase}${ruta}`, {
      method: "PATCH",
      headers: headers(),
      body: cuerpo,
    })
  }

  async function del(ruta: string): Promise<void> {
    await $fetch(`${config.public.apiBase}${ruta}`, {
      method: "DELETE",
      headers: headers(),
    })
  }

  return { get, post, put, patch, del }
}
