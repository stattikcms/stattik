<component name="PostCards">

<template>
    <ul class="article-list">
      <li v-for="post in self.posts">
        <post-card post="{{post}}" />
      </li>
    </ul>
</template>

<script type="text/python">

props = ['posts']

components = {
  'PostCard': Vue.resolve('src/components/PostCard'),
}

</script>

</component>