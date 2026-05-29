<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="modelValue"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        @click.self="$emit('update:modelValue', false)"
      >
        <!-- Overlay -->
        <div class="absolute inset-0 bg-slate-900/40 backdrop-blur-sm" />

        <!-- Panel -->
        <div
          class="relative z-10 w-full bg-white rounded-2xl shadow-modal overflow-hidden"
          :class="maxWidth"
        >
          <!-- Header -->
          <div v-if="titulo" class="flex items-center justify-between px-6 pt-5 pb-4 border-b border-slate-100">
            <h2 class="text-base font-semibold text-slate-900">{{ titulo }}</h2>
            <button
              @click="$emit('update:modelValue', false)"
              class="w-8 h-8 flex items-center justify-center rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
            >
              ✕
            </button>
          </div>

          <!-- Content -->
          <div class="px-6 py-5">
            <slot />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: boolean
  titulo?: string
  maxWidth?: string
}>()

defineEmits<{
  "update:modelValue": [value: boolean]
}>()
</script>

<style scoped>
.modal-enter-active { transition: all 200ms cubic-bezier(0.16, 1, 0.3, 1); }
.modal-leave-active { transition: all 150ms ease; }
.modal-enter-from { opacity: 0; }
.modal-leave-to   { opacity: 0; }
.modal-enter-from .relative { transform: scale(0.96) translateY(8px); }
.modal-leave-to   .relative { transform: scale(0.96) translateY(4px); }
</style>
