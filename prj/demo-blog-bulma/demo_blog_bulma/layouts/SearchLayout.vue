<template>
  <container>
    <div class="columns">
      <div class="column is-one-fifth">
        <div class="landing-heading">
          <div class="landing-title">Search</div>
        </div>
      </div>
      <div class="column">
        <router-view />
      </div>
      <div class="column is-one-fifth">
      </div>
    </div>
  </container>
</template>

<script type="text/python">
components = {
  'Container': Vue.resolve('src/components/Container'),
}
</script>
