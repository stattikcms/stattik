<component name="HeroBanner">
<template>
  <div class="hero-banner hero">
    <slot/>
  </div>
</template>

<style>
.hero-banner {
  padding-top: 1em;
  padding-bottom: 1em;
  margin-bottom: 1em;
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