<template>
  <div id="app">
    <header>
      <img alt="Vue logo" src="./assets/vue.svg" />
      <h1>Vue 3 + Vite</h1>
    </header>
    
    <main>
      <HelloWorld msg="안녕하세요! Vue.js 프로젝트입니다." />
    </main>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  components: {
    HelloWorld
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

header {
  margin-bottom: 2rem;
}

header img {
  width: 100px;
  height: 100px;
}
</style>