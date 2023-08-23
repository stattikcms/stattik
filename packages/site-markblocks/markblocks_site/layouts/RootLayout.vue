<template>
<div class="layout">
  <site-header />
    <main>
      <container>
          <router-view />
      </container>
    </main>
</div>
</template>

<script type="text/python">
Container = Vue.resolve('src/components/Container')
SiteHeader = Vue.resolve('src/components/SiteHeader')

components = {
  'Container': Container,
  'SiteHeader': SiteHeader
}
</script>
