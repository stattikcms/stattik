<component name="Post">
<template>
  <div>
    <h1>{{ v_page.title }}</h1>
    <div>{{ v_page.content }}</div>
  </div>
</template>

<script type="text/python">
def data(self):
    return {
      'greeting': 'Hello'
    }
</script>
</component>