<template>
    <ul class="article-list">
      <li v-for="(result, index) in results" :key="index">
        <result-card :result="result" />
      </li>
    </ul>
</template>

<script setup>
import { ref, markRaw, onMounted } from 'vue'

import ResultCard from './ResultCard.vue'

defineProps({
  results: Array
})

const name="ResultCards"

const components = {
  ResultCard,
}

</script>