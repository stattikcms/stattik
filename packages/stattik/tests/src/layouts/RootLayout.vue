<component name="RootLayout">
<template>
<div class="layout">
  <container>
    <div>
      <navbar />
      <main class="darkdown-body">
        <router-view />
      </main>
    </div>
  </container>
</div>
</template>

<script type="text/python">
Container = Vue.resolve('src/components/Container')
Navbar = Vue.resolve('src/components/Navbar')

components = {
  'Container': Container,
  'Navbar': Navbar
}
</script>

</component>