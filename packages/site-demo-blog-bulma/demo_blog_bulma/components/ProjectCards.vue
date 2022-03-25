<component name="ProjectCards">

<template>
  <ul class="article-list">
    <li v-for="project in self.projects">
      <project-card project="{{project}}" />
    </li>
  </ul>
</template>

<script type="text/python">

ProjectCard = Vue.resolve('src/components/ProjectCard')

props = ['projects']

components = {
  'ProjectCard': ProjectCard,
}

</script>

</component>