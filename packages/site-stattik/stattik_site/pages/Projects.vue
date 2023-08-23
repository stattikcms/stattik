<template>
  <section>
      <div class="columns">
        <div class="column">
          <div class="landing-heading">
            <div class="landing-title">Projects</div>
          </div>
        </div>
        <div class="column is-four-fifths">
          <projects />
        </div>
      </div>

  </section>
</template>

<script type="text/python">
HeroBanner = Vue.resolve('src/components/HeroBanner')
ProjectCards = Vue.resolve('src/components/ProjectCards')

components = {
  'HeroBanner': HeroBanner,
  'ProjectCards': ProjectCards,
}
</script>

<style>

.landing-title {
  font-size: 2em;
  white-space: nowrap;
  opacity: .5;
}
@media only screen  and (min-width : 1224px) {
  .landing-title {
    font-size: 4em;
    transform: rotate(-90deg);
    //position: absolute;
    position: relative;
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
