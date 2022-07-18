<component name="Contact">

<template>
  <section>
    <form name="contact" method="POST" data-netlify="true">
      <div class="field">
        <label class="label">Your Name:</label>
        <div class="control">
          <input class="input" type="text" name="name" />
        </div>
      </div>
      <div class="field">
        <label class="label">Your Email:</label>
        <div class="control">
          <input class="input" type="email" name="email" />
        </div>
      </div>
      <div class="field">
        <label class="label">Message:</label>
        <div class="control">
          <textarea class="textarea" name="message"></textarea>
        </div>
      </div>
      <div class="field">
          <button class="button is-link" type="submit">Send</button>
      </div>
    </form>
  </section>
</template>

<script type="text/python">
HeroBanner = Vue.resolve('src/components/HeroBanner')

components = {
  'HeroBanner': HeroBanner,
}
</script>

</component>