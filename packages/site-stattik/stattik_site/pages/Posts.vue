<component name="Posts">

<template>
  <section>
      <div class="columns">
        <div class="column">
          <div class="landing-heading">
            <div class="landing-title">{{v_page.title}}</div>
          </div>
        </div>
        <div class="column is-four-fifths">
          <post-cards />
        </div>
      </div>

  </section>
</template>

<script type="text/python">
HeroBanner = Vue.resolve('src/components/HeroBanner')
PostCards = Vue.resolve('src/components/PostCards')

components = {
  'HeroBanner': HeroBanner,
  'PostCards': PostCards,
}

</script>

<style>

.landing-outer {
  position: relative
}

.landing-title {
  font-size: 2em;
  white-space: nowrap;
  opacity: .5;
}

@media only screen  and (min-width : 1224px) {
  .landing-title {
    font-size: 4em;
    transform: rotate(-90deg);
    position: absolute;
    top: 256px;

    // transform-origin: 0 0;
    // padding-top: 3em;
    // padding-left: 1em;
  }
}

@media only screen and (max-width : 1223px) {
  .landing-heading {
    //padding-left: 1em;
    transform: none;
  }
  .landing-title {
    transform: none;
  }
}

</style>

</component>