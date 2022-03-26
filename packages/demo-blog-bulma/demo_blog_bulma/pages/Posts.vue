<component name="Posts">

<template>
  <post-cards posts="{{self.posts}}"/>
  <pagination paginator="{{self.paginator}}" number="{{self.number}}"/>
</template>

<script type="text/python">
from stattik.core.pagination import Paginator

components = {
  'PostCards': Vue.resolve('src/components/PostCards'),
  'Pagination': Vue.resolve('src/components/Pagination'),
}

async def created(self):
    if hasattr(self, 'number'):
        number = self.number
    else:
        self.number = number = 1

    self.posts = self.paginator.page(number).objects

async def paginate(self):
    db = self.v_db
    per_page = 5
    paginator = await Paginator.produce(db['Post'], per_page, self.v_page.url, self.v_page.path)
    return await super(self.__class__, self).paginate(paginator)

</script>

<style>

.landing-title {
  font-size: 2em;
  white-space: nowrap;
  opacity: .5;
}
@media only screen  and (min-width : 1224px) {
  .landing-title {
    font-size: 4em;
    transform: rotate(-90deg);
    //position: absolute;
    position: relative;
    top: 256px;

    // transform-origin: 0 0;
    // padding-top: 3em;
    // padding-left: 1em;
  }
}
@media only screen and (max-width : 1223px) {
  .landing-heading {
    //padding-left: 1em;
    transform: none;
  }
  .landing-title {
    transform: none;
  }
}

</style>

</component>