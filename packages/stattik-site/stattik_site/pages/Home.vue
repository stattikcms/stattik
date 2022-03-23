<component name="Home">

<template>
  <hero-banner><h1>{{v_page.title}}</h1></hero-banner>
  <callouts />
  <section>
    {{v_page.content}}
  </section>
</template>

<script type="text/python">
HeroBanner = Vue.resolve('src/components/HeroBanner')
Callouts = Vue.resolve('src/components/Callouts')

components = {
  'HeroBanner': HeroBanner,
  'Callouts': Callouts,
}
</script>

</component>