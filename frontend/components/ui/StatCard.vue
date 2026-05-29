<template>
  <div class="bg-white rounded-2xl border border-slate-100 shadow-card p-5 flex flex-col gap-3">
    <div class="flex items-center justify-between">
      <span class="text-xs font-semibold uppercase tracking-widest text-slate-400">{{ label }}</span>
      <div
        v-if="icon"
        class="w-8 h-8 rounded-xl flex items-center justify-center text-sm"
        :class="iconBg"
      >
        {{ icon }}
      </div>
    </div>
    <div>
      <p class="text-2xl font-bold text-slate-900 tracking-tight tabular">{{ valor }}</p>
      <p v-if="sub" class="text-xs text-slate-400 mt-0.5">{{ sub }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  label: string
  valor: string
  sub?: string
  icon?: string
  iconBg?: string
}>()
</script>
