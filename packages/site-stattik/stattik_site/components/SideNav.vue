<template>
  <aside class="menu">
    <ul class="menu-list">
    <menu menu="{{self.menu}}" />
    </ul>
  </aside>
</template>

<script type="text/python">
from stattik.menu import build_bottom_up

Menu = Vue.resolve('src/components/Menu')

components = {
  'Menu': Menu,
}

async def created(self):
  self.menu = build_bottom_up(self.v_page)
</script>
