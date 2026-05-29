<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="clases"
    class="inline-flex items-center justify-center gap-2 font-semibold transition-all duration-150 focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
  >
    <span v-if="loading" class="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
    <slot />
  </button>
</template>

<script setup lang="ts">
const props = defineProps<{
  variant?: "primary" | "secondary" | "ghost" | "danger"
  size?: "sm" | "md" | "lg"
  loading?: boolean
  disabled?: boolean
  type?: "button" | "submit" | "reset"
}>()

const clases = computed(() => {
  const v = props.variant ?? "primary"
  const s = props.size ?? "md"

  const variants = {
    primary: "bg-primary-600 text-white hover:bg-primary-700 shadow-sm active:scale-[0.98]",
    secondary: "bg-white text-slate-700 border border-slate-200 hover:bg-slate-50 shadow-sm active:scale-[0.98]",
    ghost: "text-slate-600 hover:text-slate-900 hover:bg-slate-100",
    danger: "bg-red-600 text-white hover:bg-red-700 shadow-sm active:scale-[0.98]",
  }

  const sizes = {
    sm: "text-xs px-3 py-1.5 rounded-lg",
    md: "text-sm px-4 py-2.5 rounded-xl",
    lg: "text-sm px-5 py-3 rounded-xl",
  }

  return `${variants[v]} ${sizes[s]}`
})
</script>
