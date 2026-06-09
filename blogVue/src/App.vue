<script setup>
import Navbar from '@/components/Navbar.vue'
</script>

<template>
  <div id="app">
    <Navbar />
    <main class="container mt-4">
      <router-view />
    </main>
  </div>
</template>
