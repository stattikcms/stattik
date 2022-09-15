<component name="Home">

<template>
    <div class="columns">
      <div class="column is-one-fifth">
        <div class="landing-heading">
          <div class="landing-title">Kurtis Fields</div>
        </div>
      </div>
      <div class="column">
        {{v_page.content}}
        <latest-posts/>
      </div>
      <div class="column is-one-fifth">
      </div>
    </div>

</template>

<script type="text/python">
HeroBanner = Vue.resolve('src/components/HeroBanner')

components = {
  'HeroBanner': HeroBanner,
  'LatestPosts': Vue.resolve('src/components/LatestPosts'),
}
</script>

</component>