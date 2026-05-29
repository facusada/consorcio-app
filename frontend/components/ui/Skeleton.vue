<template>
  <div
    class="animate-pulse rounded-lg bg-slate-100"
    :style="{ height, width }"
  />
</template>

<script setup lang="ts">
defineProps<{
  height?: string
  width?: string
}>()
</script>
