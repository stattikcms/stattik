<component name="Emojize">
<template>
<div>
{{emoji.emojize(slots['default'], language='alias')}}
</div>
</template>

<script type="text/python">
import emoji
</script>

</component>