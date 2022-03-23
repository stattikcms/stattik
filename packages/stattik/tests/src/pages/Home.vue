<component name="Home">

<template>
  <div>
      <div class="columns is-gapless">
        <div class="column">
        </div>
        <div class="column is-four-fifths">
          <div>{{ v_page.content }}</div>
        </div>
      </div>

      <div class="columns is-gapless">
        <div class="column">
          <div class="landing-heading">
            <div class="landing-title">Latest Posts</div>
          </div>
        </div>
        <div class="column is-four-fifths">
          <div>Post Here</div>
        </div>
      </div>

  </div>
</template>

<script type="text/python">
HeroBanner = Vue.resolve('src/components/HeroBanner')

components = {
  'HeroBanner': HeroBanner,
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
    font-size: 3em;
    transform: rotate(-90deg);
    //position: absolute;
    position: relative;
    top: 256px;

    // transform-origin: 0 0;
    // padding-top: 3em;
    // padding-left: 1em;
  }
}
/* Smartphones (portrait) ----------- */
@media only screen and (max-width : 1223px) {
  .landing-heading {
    padding-left: 1em;
    transform: none;
  }
  .landing-title {
    transform: none;
  }
}

</style>

</component>