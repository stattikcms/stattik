import re

from loguru import logger

from lxml import etree

from .transpiler_base import TranspilerBase, Css
from .elements import void_elements

class Transpiler(TranspilerBase):
    def __init__(self):
        super().__init__()
        self.attrs = {}
        self.module = None
        self.fragments = []
        self.views = []
        self.css = None
        
    def parse(self, root):
        # root = <component name="SomeComponent" ...>
        self.root = root
        for key, value in root.attrib.items():
            self.attrs[key] = value
            #print(f"root: {key}, {value}")

        self.begin(root)

        script_node = root.find('script')
        if script_node is not None:
            script_scope = self.parse_script(script_node)
            self.scope.iadd(script_scope)

        template_node =  root.find('template')
        if template_node is not None:
            template_scope = self.parse_template(template_node)
            self.scope.iadd(template_scope)

        style_node = root.find('style')
        if(style_node is not None):
            self.parse_style(style_node)

        for fragment in self.fragments:
            self.scope.iadd(fragment)

        if(len(self.views)):
            self.scope("views = [")
            self.scope.indent()
            for view in self.views:
                self.scope(f"'{view}',")
            self.scope.dedent()
            self.scope("]")


        
    def parse_node(self, node):
        tag = node.tag
        if tag is etree.Comment:
            return
        elif tag == 'router-view':
            self.parse_view(node)
        elif tag == 'slot':
            self.parse_slot(node)
        elif 'v-if' in node.attrib:
            self.parse_if(node)
        elif 'v-for' in node.attrib:
            self.parse_for(node)
        elif self.iscomponent(tag):
            self.parse_component(node)
        else:
            self.parse_any(node)
            
    def parse_children(self, node):
        for child in node:
            self.parse_node(child)

    def parse_template(self, node):
        self.begin(node)
        self.scope("async def render(self, slots=None):")
        self.scope.indent()
        self.scope('return f"""')
        self.parse_children(node)
        self.scope('"""')
        self.scope.dedent()
        return self.end()
    
    def parse_slot(self, node):
        self.scope("{ self.render_slot(slots) }")

    def parse_view(self, node):
        self.views.append('default')
        self.scope("{ await self.render_view() }")

    def parse_script(self, node):
        self.begin(node)
        self.scope("from stattik.vue import Vue\n")
        self.scope(node.text)
        self.module = self.compile_module(self.src_path, str(self.scope))
        return self.end()

    def parse_if(self, node):
        expr = node.attrib['v-if']
        del node.attrib['v-if']
        self.begin_fragment(node)
        counter = self.scope.counter
        self.scope(f"async def fragment_{counter}(self):")
        self.scope.indent()
        self.scope('lines = []')
        self.scope(f"if {expr}:")
        self.scope.indent()
        self.scope('lines.append(f"""')
        self.parse_node(node)
        self.scope('""")')
        self.scope.dedent()
        self.scope('return "".join(lines)')
        self.scope.dedent()
        self.fragments.append(self.end())
        self.scope(f"{{ await self.fragment_{counter}() }}")

    def parse_for(self, node):
        expr = node.attrib['v-for']
        del node.attrib['v-for']
        self.begin_fragment(node)
        counter = self.scope.counter
        self.scope(f"async def fragment_{counter}(self):")
        self.scope.indent()
        self.scope('lines = []')
        self.scope(f"for {expr}:")
        self.scope.indent()
        self.scope('lines.append(f"""')
        self.parse_node(node)
        self.scope('""")')
        self.scope.dedent()
        self.scope('return "".join(lines)')
        self.scope.dedent()
        self.fragments.append(self.end())
        self.scope(f"{{ await self.fragment_{counter}() }}")

    def parse_component(self, node):
        if len(node): # Means: has children
            self.begin_fragment(node)
            counter = self.scope.counter
            self.scope(f"async def fragment_{counter}(self):")
            self.scope.indent()
            self.scope('return f"""')
            self.parse_children(node)
            self.scope('"""')
            self.scope.dedent()
            self.fragments.append(self.end())
            self.scope(f"{{ await self.render_component('{self.kebab_to_pascal(node.tag)}', {self.parse_props(node)}, slots={{ 'default': await self.fragment_{counter}()}}) }}")
        elif node.text is not None:
            self.scope(f"{{ await self.render_component('{self.kebab_to_pascal(node.tag)}', {self.parse_props(node)}, slots={{ 'default': '{node.text}'}}) }}")
        else:
            self.scope(f"{{ await self.render_component('{self.kebab_to_pascal(node.tag)}', {self.parse_props(node)}) }}")

    def parse_props(self, node):
        if not node.attrib:
            return '{}'
        return self.parse_prop(str(node.attrib))

    def parse_prop(self, text):
        result = []
        tokens = re.split(r"(?s)('{{.*?}}'|'{%.*?%}'|'{#.*?#}')", text)
        #print(tokens)
        for token in tokens:
            if token.startswith("'{{"):
                result.append(token[3:-3].strip())
            else:
                result.append(token)
        return "".join(result)

    def parse_component_attrs(self, node):
        s = "{ "
        for key, value in node.attrib.items():
            s += f" '{key}': {self.parse_component_attr_value(value)}, "
        s += "}"
        return s            

    def parse_component_attr_value(self, text):
        result = []
        tokens = re.split(r"(?s)({{.*?}}|{%.*?%}|{#.*?#})", text)
        #print(tokens)
        for token in tokens:
            if token.startswith('{{'):
                result.append(self._expr_code(token[3:-3].strip()))
            else:
                result.append(token)
        return "".join(result)

    def parse_attrs(self, node):
        s = ""
        for key, value in node.attrib.items():
            s += f' {key}="{self.parse_text(value)}"'
        return s            

    def parse_style(self, node):
        #print(node.text)
        self.css = css = Css(node)
        css(node.text)

    def parse_text(self, text):
        result = []
        tokens = re.split(r"(?s)({{.*?}}|{%.*?%}|{#.*?#})", text)
        #print(tokens)
        for token in tokens:
            if token.startswith('{{'):
                result.append(self._expr_code(token[2:-2].strip()))
            else:
                result.append(token)
        return "".join(result)

    '''
    def parse_any(self, node):
        tag = node.tag            
        self.scope(f"<{tag} {self.parse_attrs(node)}>")
        text = node.text
        if text:
            self.scope.indent()
            self.scope(self.parse_text(text))
            self.scope.dedent()
        self.parse_children(node)
        self.scope(f"</{tag}>")
    '''

    def parse_any(self, node):
        tag = node.tag            
        text = node.text
        if not isinstance(tag, str):
            self.scope(node)
        elif tag not in void_elements:
            self.scope(f"<{tag} {self.parse_attrs(node)}>")
            if text:
                self.scope.indent()
                self.scope(self.parse_text(text))
                self.scope.dedent()
            self.parse_children(node)
            self.scope(f"</{tag}>")
        else:
            self.scope(f"<{tag} {self.parse_attrs(node)} />")
    