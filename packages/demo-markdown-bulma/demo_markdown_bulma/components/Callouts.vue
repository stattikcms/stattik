<component name="Callouts">

<template>
  <section>
    <div class="columns is-multiline">
      <div class="column is-one-third" v-for="callout in self.v_page.data['callouts']">
        <callout callout="{{callout}}" />
      </div>
    </div>
  </section>
</template>

<script type="text/python">

Callout = Vue.resolve('src/components/Callout')

components = {
  'Callout': Callout,
}

</script>

</component>