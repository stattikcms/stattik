<component name="ProjectCard">

<template>
<div class="card my-3">
  <header class="card-header">
    <a href="{{project.url}}" class="card-header-title" >
    <p class="previewTitle">
      {{project.title}}
    </p>
    </a>
    <div class="card-header-icon">
      <span class="icon is-medium">
        <i class="far fa-star"></i>
      </span>
      <div> {{project.stars}} </div>
    </div>
  </header>
  <div class="card-content">
    <div class="content">
      {{project.description}}
    </div>
  </div>
</div>
</template>

<script>
props = ['project']
</script>

<style>
.previewTitle {
  font-size: 1.5rem;
  margin-top: .5rem;
  margin-bottom: .5rem;
  // line-height: 1rem;
}
.previewSummary {
  color:#A0A0A0
}
.previewImage {
  max-height: 200px;
  overflow: hidden;
  height: 100%;
  width: 100%;
  object-fit: cover;
  /*
  border-radius: 5%;
  border-width: 1px;
  border-style: solid;
  border-color: #eeeeee;
  */
}

.previewDate {
  text-align: right;
}

.tag {
  color: #A0A0A0;
  text-decoration: none;
  display: inline-block;
  padding: .33333rem .5rem;
  line-height: 1;
  border-radius: 2px;
  border: 1px solid #A0A0A0;
  margin-right: .5em;
}
</style>

</component>