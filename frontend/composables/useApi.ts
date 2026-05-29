export function useApi() {
  const config = useRuntimeConfig()
  const auth = useAuthStore()

  async function get<T>(ruta: string): Promise<T> {
    const { data, error } = await useFetch<T>(`${config.public.apiBase}${ruta}`, {
      headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : {},
    })
    if (error.value) throw error.value
    return data.value as T
  }

  async function post<T>(ruta: string, cuerpo: unknown): Promise<T> {
    const { data, error } = await useFetch<T>(`${config.public.apiBase}${ruta}`, {
      method: "POST",
      headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : {},
      body: cuerpo,
    })
    if (error.value) throw error.value
    return data.value as T
  }

  async function put<T>(ruta: string, cuerpo: unknown): Promise<T> {
    const { data, error } = await useFetch<T>(`${config.public.apiBase}${ruta}`, {
      method: "PUT",
      headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : {},
      body: cuerpo,
    })
    if (error.value) throw error.value
    return data.value as T
  }

  async function patch<T>(ruta: string, cuerpo: unknown): Promise<T> {
    const { data, error } = await useFetch<T>(`${config.public.apiBase}${ruta}`, {
      method: "PATCH",
      headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : {},
      body: cuerpo,
    })
    if (error.value) throw error.value
    return data.value as T
  }

  async function del(ruta: string): Promise<void> {
    const { error } = await useFetch(`${config.public.apiBase}${ruta}`, {
      method: "DELETE",
      headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : {},
    })
    if (error.value) throw error.value
  }

  return { get, post, put, patch, del }
}
