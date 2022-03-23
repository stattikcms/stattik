from pathlib import Path
from lxml import etree
from lxml.html import XHTMLParser

from loguru import logger

from stattik.site import Site
from .transpiler import Transpiler

class Compiler(Transpiler):
    def __init__(self, src_path, dst_path):
        super().__init__()
        self.src_path = src_path
        self.dst_path = dst_path
        self.code = None

    def compile(self):
        src_path = self.src_path
        dst_path = self.dst_path

        #logger.info(f"compiling:  {src_path}")
        text = '''
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        '''
        with open(str(src_path)) as f:
            #text = f.read()
            text += f.read()

        try:
            code = self.compile_fromstring(text)
        except etree.XMLSyntaxError as exc:
            print(f"Exception compiling:  {src_path}")
            print(exc)
            raise exc

        # TODO: This is triggering a reload when serving
        
        with open(dst_path, "w") as text_file:
            text_file.write(code)
        
        self.code = code

    def compile_fromstring(self, text):
        root = etree.fromstring(text, parser=XHTMLParser(resolve_entities=False))
        self.parse(root)
        if self.css:
            Site.instance.add_css(self.css)
                
        return str(self)