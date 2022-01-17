<template>
    <section>
        <nav class="bg-gray-100 p-1 text-black">
            <div><h1 class="text-2xl text-cyan-700 text-center">Rug</h1></div>
        </nav>
        <h2>{{ counter }}</h2>
        <button @click="addOne" class="bg-sky-400 p-2 text-center rounded-md transiton duration-300 hover:bg-sky-300">add</button>
    </section>
</template>
<script>
export default {
  name: "Header",
  data() {
    return {};
  },
  methods: {
    addOne(){
      this.$store.state.counter++;
    }
  },
  computed: {
    counter(){
      return this.$store.state.counter;
    }
  }
};
</script>
<style></style>
