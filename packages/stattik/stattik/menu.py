import json

class Menu:
    def __init__(self, data):
        self.children = []
        self.cls = ''
        self.inject(data)

    def inject(self, data):
        for key in data:
            setattr(self, key, data[key])

    def add_child(self, child):
        self.children.append(child)

    def dumps(self):
        #return json.dumps(self.__dict__, sort_keys=True, indent=4)
        return self.__dict__

def print_menu(menu):
    print(menu.__dict__)
    for child in menu.children:
        print_menu(child)

def build_bottom_up(page, stop_url='/'):
    matched = build_matched(page, stop_url)
    #print(matched)
    menu = build_menu(matched)
    #print_menu(menu)
    return menu

def build_menu(matched):
    page = matched[0]
    cls = 'is-active' if len(matched) == 1 else ''
    menu = Menu({ 'title': page.title, 'url': page.url, 'cls': cls })
    if page.menu:
        for item in page.menu:
            if len(matched) > 1 and item['url'] == str(matched[1].url):
            #if len(matched) > 1 :
                menu.add_child(build_menu(matched[1:]))
            else:    
                menu.add_child(Menu(item))
    return menu

def build_matched(page, stop_url='/'):
    if not page.parent or not page.parent.menu or page.url == stop_url:
        return [page]
    result = build_matched(page.parent, stop_url)
    result.append(page)
    return result
