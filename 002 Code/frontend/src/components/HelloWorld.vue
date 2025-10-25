<template>
  <div class="hello">
    <h2>{{ msg }}</h2>
    <p>
      Vue.js 프로젝트가 성공적으로 설정되었습니다!
    </p>
    
    <div class="counter">
      <button @click="count++">카운트: {{ count }}</button>
    </div>
    
    <p>
      <a href="https://vuejs.org/" target="_blank" rel="noopener">Vue 3 문서</a> |
      <a href="https://vitejs.dev/" target="_blank" rel="noopener">Vite 문서</a>
    </p>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  setup() {
    const count = ref(0)
    
    return {
      count
    }
  }
}
</script>

<style scoped>
.hello {
  padding: 2rem;
}

.counter button {
  background-color: #42b883;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  margin: 1rem 0;
}

.counter button:hover {
  background-color: #369870;
}

a {
  color: #42b883;
  text-decoration: none;
  margin: 0 0.5rem;
}

a:hover {
  text-decoration: underline;
}
</style>