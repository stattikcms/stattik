<template>
  <hero-banner><h1>{{v_page.title}}</h1></hero-banner>
  <section>
    {{v_page.content}}
  </section>
</template>

<script type="text/python">
HeroBanner = Vue.resolve('src/components/HeroBanner')

components = {
  'HeroBanner': HeroBanner,
}
</script>
