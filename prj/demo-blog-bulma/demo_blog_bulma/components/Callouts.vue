<template>
    <div class="columns">
      <div class="column" v-for="callout in self.v_page.data['callouts']">
        <callout callout="{{callout}}" />
      </div>
    </div>
</template>

<script type="text/python">

Callout = Vue.resolve('src/components/Callout')

components = {
  'Callout': Callout,
}

</script>
