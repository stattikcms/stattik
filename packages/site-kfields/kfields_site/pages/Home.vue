<component name="Home">

<template>
  <hero-banner>
    <h1>{{v_page.title}}</h1>
    <h2>{{v_page.description}}</h2>
  </hero-banner>
  <section>
    {{v_page.content}}
  </section>
  <callouts />
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