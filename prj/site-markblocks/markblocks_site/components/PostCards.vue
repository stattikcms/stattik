<template>
    <ul class="article-list">
      <li v-for="post in self.posts">
        <post-card post="{{post}}" />
      </li>
    </ul>
</template>

<script type="text/python">

components = {
  'PostCard': Vue.resolve('src/components/PostCard'),
}

async def created(self):
    db = self.v_db
    self.posts = await db['Post'].all()

</script>
