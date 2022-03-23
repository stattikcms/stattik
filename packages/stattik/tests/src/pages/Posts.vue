<component name="Posts">
<template>
  <div>
    <p>{{ v_page.content }}</p>
  </div>
</template>

<script type="text/python">
def data(self):
    return {
      'greeting': 'Hello'
    }
</script>
</component>