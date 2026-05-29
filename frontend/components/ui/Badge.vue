<template>
  <span :class="clases" class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold tracking-wide">
    <span v-if="dot" class="w-1.5 h-1.5 rounded-full bg-current opacity-80" />
    <slot />
  </span>
</template>

<script setup lang="ts">
const props = defineProps<{
  variant?: "default" | "success" | "warning" | "danger" | "info" | "neutral"
  dot?: boolean
}>()

const clases = computed(() => ({
  "bg-primary-50 text-primary-700": !props.variant || props.variant === "default",
  "bg-emerald-50 text-emerald-700": props.variant === "success",
  "bg-amber-50 text-amber-700": props.variant === "warning",
  "bg-red-50 text-red-700": props.variant === "danger",
  "bg-blue-50 text-blue-700": props.variant === "info",
  "bg-slate-100 text-slate-600": props.variant === "neutral",
}))
</script>
