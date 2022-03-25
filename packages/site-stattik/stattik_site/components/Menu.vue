<component name="Menu">

<template>
<li>
<a href="{{menu.url}}" class="{{menu.cls}}"> {{menu.title}} </a>

<ul class="menu-list">
    <menu v-for="child in self.menu.children" menu="{{child}}" />
</ul>
</li>
</template>

<script type="text/python">
props = ['menu']

</script>

</component>
