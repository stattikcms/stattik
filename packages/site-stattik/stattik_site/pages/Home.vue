<template>

  <hero-banner>
    <h1>{{v_page.title}}</h1>
    <div>{{v_page.content}}</div>
  </hero-banner>

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
