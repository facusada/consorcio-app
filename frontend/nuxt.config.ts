export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: true },

  modules: ["@pinia/nuxt", "@nuxtjs/tailwindcss"],

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000",
    },
  },

  app: {
    head: {
      title: "Consorcio App",
      meta: [
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { name: "description", content: "Gestion del consorcio residencial" },
        { name: "theme-color", content: "#1e40af" },
      ],
      link: [
        { rel: "manifest", href: "/manifest.webmanifest" },
      ],
    },
  },

  typescript: {
    strict: true,
  },
})
