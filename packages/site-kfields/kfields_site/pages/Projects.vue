<template>
  <project-cards projects="{{self.projects}}"/>
  <pagination paginator="{{self.paginator}}" number="{{self.number}}"/>
</template>

<script type="text/python">
from stattik.core.pagination import Paginator

props = ['number']

components = {
  'ProjectCards': Vue.resolve('src/components/ProjectCards'),
  'Pagination': Vue.resolve('src/components/Pagination'),
}

async def created(self):
    if hasattr(self, 'number'):
        number = self.number
    else:
        self.number = number = 1

    self.projects = self.paginator.page(number).objects

async def paginate(self):
    db = self.v_db
    per_page = 5
    paginator = await Paginator.produce(db['Project'], per_page, self.v_page.src_url, self.v_page.url, self.v_page.path)
    return await super(self.__class__, self).paginate(paginator)

</script>
