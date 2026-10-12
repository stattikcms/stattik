<template>
  <article>
    <section>
      <h1>{{ v_page.title }}</h1>
      <div>{{ v_page.content }}</div>
    </section>
  </article>
</template>

<script type="text/python">
def data(self):
    return {
      'greeting': 'Hello'
    }
</script>
