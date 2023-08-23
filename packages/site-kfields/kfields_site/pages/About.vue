<template>
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
