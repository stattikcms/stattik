<template>
  <!--<div class="preview">
    <a href="{{post.url}}" >
      <div class="previewTitle">
        {{post.title}}
      </div>
      <p class="previewSummary">
        {{post.description}}
      </p>
    </a>
  </div>-->
<div class="card preview">
  <header class="card-header">
    <a href="{{project.url}}" >
    <p class="card-header-title previewTitle">
      {{project.title}}
    </p>
    </a>
  </header>
  <div class="card-content">
    <div class="content">
      {{project.description}}
    </div>
  </div>
</div>
</template>

<script>
name = 'ProjectPreview'
props = ['project']
</script>

<style>
.preview {
  padding-bottom: 1rem;
}
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
