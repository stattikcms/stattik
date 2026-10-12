from math import remainder


class Page:
    def __init__(self, objects, number, src_url, url, path, paginator) -> None:
        self.objects = objects
        self.number = number
        self.src_url = src_url
        self.url = url
        self.path = path
        self.paginator = paginator

    def has_next(self):
        #print(self.paginator.count)
        return self.number < self.paginator.num_pages

    def has_previous(self):
        return self.number > 1

class Paginator:
    def __init__(self, objects, per_page, count, src_url, url, path):
        self.objects = objects
        self.per_page = per_page
        self.count = count
        self.src_url = src_url
        self.url = url
        self.path = path
        self.pages = []
        self.num_pages = 0

    @classmethod
    async def produce(cls, objects, per_page, src_url, url, path):
        count = await objects.count()
        paginator = cls(objects, per_page, count, src_url, url, path)
        slices = int(count / per_page)
        if not slices:
            slices = 1

        for i in range(0, slices):
            start = i * per_page
            stop = start + per_page
            page_objects = await objects.slice(start, stop)
            page_src_url = src_url if not i else src_url / 'page' / str(i+1)
            page_url = url if not i else url / 'page' / str(i+1)
            page_path = path if not i else path.parent / 'page' / str(i+1) / "index.html"
            paginator.add_page(Page(page_objects, i+1, page_src_url, page_url, page_path, paginator))

        remainder = int(count % per_page)
        if remainder and slices != 1:
            i += 1
            start = slices
            stop = slices + remainder
            page_objects = await objects.slice(start, stop)
            page_src_url = src_url if not i else src_url / 'page' / str(i+1)
            page_url = url if not i else url / 'page' / str(i+1)
            page_path = path if not i else path.parent / 'page' / str(i+1) / "index.html"
            paginator.add_page(Page(page_objects, i+1, page_src_url, page_url, page_path, paginator))

        '''
        for page in paginator.pages:
            print(page.__dict__)
        exit()
        '''
        return paginator

    def add_page(self, page):
        self.pages.append(page)
        self.num_pages = len(self.pages)

    def page_range(self):
        return range(1, self.count)
  
    def page(self, i):
        return self.pages[i-1]
