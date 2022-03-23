<component name="ProjectsLayout">
<template>
  <container>
    <router-view />
  </container>
</template>

<script type="text/python">
Container = Vue.resolve('src/components/Container')

components = {
  'Container': Container,
}
</script>

</component>