export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: true },

  modules: ["@pinia/nuxt", "@nuxtjs/tailwindcss"],

  css: ["~/assets/css/main.css"],

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
        { name: "theme-color", content: "#0f172a" },
      ],
      link: [
        { rel: "manifest", href: "/manifest.webmanifest" },
        {
          rel: "preconnect",
          href: "https://fonts.googleapis.com",
        },
        {
          rel: "preconnect",
          href: "https://fonts.gstatic.com",
          crossorigin: "",
        },
        {
          rel: "stylesheet",
          href: "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500&display=swap",
        },
      ],
    },
    pageTransition: { name: "page", mode: "out-in" },
  },

  typescript: {
    strict: true,
  },
})
