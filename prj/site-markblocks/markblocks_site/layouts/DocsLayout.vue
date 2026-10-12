<template>
  <container>
  <section>
      <div class="columns">
        <div class="column">
          <div class="landing-heading">
            <side-nav />
          </div>
        </div>
        <div class="column is-four-fifths">
          <router-view />
        </div>
      </div>

  </section>

  </container>
</template>

<script type="text/python">
SideNav = Vue.resolve('src/components/SideNav')

components = {
  'SideNav': SideNav,
}
</script>
