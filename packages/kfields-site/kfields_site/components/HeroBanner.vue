<component name="HeroBanner">
<template>
  <div class="hero-banner my-3">
    <slot/>
  </div>
</template>

<style>
.hero-banner {
  text-align: center;
  font-size: 1.2em;
}
.hero-banner h1 {
  font-size: 2.4em;
}
.hero-banner div {
  display: inline-block
}
</style>
</component>