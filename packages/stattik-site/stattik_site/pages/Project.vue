<component name="Project">
<template>
  <article>
    <!-- <g-image class="heroImage" :alt="$page.project.title" :src="$page.project.cover"/> -->
    <img class="heroImage" alt="{{v_page.title}}" src="{{v_page.cover}}" />
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
</component>