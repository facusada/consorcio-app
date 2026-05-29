<script setup lang="ts">
const auth = useAuthStore()
if (auth.autenticado) {
  await navigateTo("/admin/periodos")
} else {
  await navigateTo("/login")
}
</script>
