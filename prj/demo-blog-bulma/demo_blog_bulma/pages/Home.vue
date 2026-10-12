<template>
  <container>
    <hero-banner>
      <h1>{{v_page.title}}</h1>
      <!--<h2>{{v_page.content}}</h2>-->
    </hero-banner>

    <div class="columns">
      <div class="column is-one-fifth">
      </div>
      <div class="column">
        <latest-posts/>
      </div>
      <div class="column is-one-fifth">
      </div>
    </div>
  </container>

</template>

<script type="text/python">
from stattik.core.pagination import Paginator

components = {
  'HeroBanner': Vue.resolve('src/components/HeroBanner'),
  'LatestPosts': Vue.resolve('src/components/LatestPosts'),
}

</script>