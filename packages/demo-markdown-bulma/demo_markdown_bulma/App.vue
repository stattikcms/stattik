<component name="App">

<template>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{{v_page.title}}</title>
    <script data-search-pseudo-elements="true" defer="true" src="/js/bundle.js"></script>
    <link rel="icon" href="data:image/svg+xml,&lt;svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22>&lt;text y=%22.9em%22 font-size=%2290%22>⚡&lt;/text>&lt;/svg>" />
    <link v-for="stylesheet in self.v_site.stylesheets" rel="stylesheet" href="{{stylesheet}}" />
  </head>
  <body>
    <router-view />
  </body>
</html>
</template>

<script type="text/python">

components = {
  'Container': Vue.resolve('src/components/Container'),
  'Emojize': Vue.resolve('src/components/Emojize'),
}

</script>

</component>