<template>
  <header>
    <container>
        <top-nav />
    </container>
  </header>
</template>

<script type="text/python">
Container = Vue.resolve('src/components/Container')
TopNav = Vue.resolve('src/components/TopNav')

components = {
  'Container': Container,
  'TopNav': TopNav
}
</script>
