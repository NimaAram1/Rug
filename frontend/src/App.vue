<template>
    <section>
      <Header />
      <router-view></router-view>
    </section>
</template>

<script>
import Header from './components/Header.vue';

export default {
  name: "App",
  components: {
    Header
  }
  }
</script>

<style>
@import url('assets/css/style.css');
</style>
