<template>
    <ul class="article-list">
      <li v-for="project in self.projects">
        <project-card project="{{project}}" />
      </li>
    </ul>
</template>

<script type="text/python">

ProjectCard = Vue.resolve('src/components/ProjectCard')

components = {
  'ProjectCard': ProjectCard,
}

async def created(self):
    db = self.v_db
    self.projects = await db['Project'].all()

</script>
