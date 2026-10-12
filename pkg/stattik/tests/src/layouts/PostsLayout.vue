<template>
  <container>
    <div>
      <h1>Posts</h1>
      <router-view />
    </div>
  </container>
</template>

<script type="text/python">
Container = Vue.resolve('src/components/Container')

components = {
  'Container': Container,
}
</script>
