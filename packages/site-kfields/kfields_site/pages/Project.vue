<template>
  <article>
    <img class="hero-image" alt="{{v_page.title}}" src="{{v_page.cover}}" />
    <section>
      <!-- <h1>{{ v_page.title }}</h1> -->
      <!-- <div>{{ v_page.description }}</div> -->
      <div class="content">{{ v_page.content }}</div>
    </section>
  </article>
</template>

<script type="text/python">
def data(self):
    return {
      'greeting': 'Hello'
    }
</script>
