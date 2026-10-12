<template>
  <h2>Latest Posts</h2>
  <post-cards posts="{{self.posts}}"/>
  <a href="/blog">
  <button class="button">
  <span class="icon-text">
    <span>All Posts</span>
    <span class="icon">
      <i class="fas fa-arrow-right"></i>
    </span>
  </span>
  </button>
  </a>
</template>

<script type="text/python">

components = {
  'PostCards': Vue.resolve('src/components/PostCards'),
}

async def created(self):
    db = self.v_db
    self.posts = await db['Post'].latest(0, 5)

</script>

<style>
</style>
