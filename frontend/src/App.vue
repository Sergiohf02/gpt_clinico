<script setup>
import { ref, onMounted } from 'vue'

const message = ref("Cargando...")

onMounted(async () => {
  const res = await fetch("http://localhost:8000/api/health")
  const data = await res.json()
  message.value = data.status
})
</script>

<template>
  <h1>Frontend funcionando</h1>
  <p>Backend responde: {{ message }}</p>
</template>