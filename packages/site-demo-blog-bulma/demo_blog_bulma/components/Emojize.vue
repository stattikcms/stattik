<component name="Emojize">

<template>
  <div>
    {{emoji.emojize(slots['default'], use_aliases=True)}}
  </div>
</template>

<script type="text/python">
import emoji
</script>

</component>