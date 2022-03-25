<script setup>
import { reactive, ref, markRaw, onMounted, onUpdated } from 'vue'
import Fuse from 'fuse.js'

import ResultCards from './ResultCards.vue'

defineProps({
  msg: String
})

const components = {
  ResultCards,
}

const data = reactive({
  results: []
})

let name = ''

let fuse = null
const fuseOptions = {
  useExtendedSearch: true,
  includeMatches: true,
  includeScore: true,
  threshold: 0.3,
  keys: ['title', 'description', 'content']
}

let fuseIndex = null
//let results = ref([])

onMounted(async () => {
  const response = await fetch('/search/index.json')
  console.log(response)
  const resources = await response.json()
  console.log(resources)
  fuse = markRaw(new Fuse(resources, fuseOptions, fuseIndex))
})

onUpdated(() => {
  // text content should be the same as current `count.value`
  // console.log(document.getElementById('count').textContent)
})

let onInput = (event) => {
  console.log(event)
  const value = event.srcElement.value
  console.log('value', value)
  data.results = fuse.search(value)
  console.log('fuse', data.results)

}

</script>

<template>
<section>
  <o-field class="my-4">
    <o-input rounded v-model="name" @input="onInput"></o-input>
  </o-field>

  <result-cards :results="data.results"/>
</section>
</template>

<style scoped>
a {
  color: #42b983;
}
</style>
