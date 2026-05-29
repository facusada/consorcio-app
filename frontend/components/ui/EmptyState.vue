<template>
  <div class="flex flex-col items-center justify-center py-16 px-8 text-center">
    <div class="w-16 h-16 rounded-2xl bg-slate-50 flex items-center justify-center text-2xl mb-4">
      {{ icon }}
    </div>
    <h3 class="text-sm font-semibold text-slate-700 mb-1">{{ titulo }}</h3>
    <p class="text-sm text-slate-400 max-w-xs">{{ descripcion }}</p>
    <slot />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  icon?: string
  titulo: string
  descripcion: string
}>()
</script>
