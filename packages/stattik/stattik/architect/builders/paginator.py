from .builder import Builder

class Paginator(Builder):
    extension = 'Paginator'
    @property
    def is_deferred(self):
        return True

    async def build(self, job):
        print(job.__dict__)

    async def build_page(self, job):
        #print(job.__dict__)
        builder = self.get_builder(job)
        page = await builder.build(job)

        type = page.type
        repo = self.architect.db[type]

        await repo.add(page)
        return page
