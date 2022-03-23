# https://developer.mozilla.org/en-US/docs/Web/HTML/Element

element_list = [
    # Main root
    'html',
    # Document metadata
    'base',
    'head',
    'link',
    'meta',
    'style',
    'title',
    # Sectioning root
    'body',
    # Content sectioning
    'address',
    'article',
    'aside',
    'footer',
    'header',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'main',
    'nav',
    'section',
    # Text content
    'blockquote',
    'dd',
    'div',
    'dl',
    'dt',
    'figcaption',
    'figure',
    'hr',
    'li',
    'ol',
    'p',
    'pre',
    'ul',
    # Inline text semantics
    'a',
    'abbr',
    'b',
    'bdi',
    'bdo',
    'br',
    'cite',
    'code',
    'data',
    'dfn',
    'em',
    'i',
    'kbd',
    'mark',
    'q',
    'rp',
    'rt',
    'ruby',
    's',
    'samp',
    'small',
    'span',
    'strong',
    'sub',
    'sup',
    'time',
    'u',
    'var',
    'wbr',
    # Image and multimedia
    'area',
    'audio',
    'img',
    'map',
    'track',
    'video',
    # Embedded content
    'embed',
    'iframe',
    'object',
    'param',
    'picture',
    'portal',
    'source',
    # SVG and MathML
    'svg',
    'math',
    # Scripting
    'canvas',
    'noscript',
    'script',
    # Demarcating edits
    'del',
    'ins',
    # Table content
    'caption',
    'col',
    'colgroup',
    'table',
    'tbody',
    'td',
    'tfoot',
    'th',
    'thead',
    'tr',
    # Forms
    'button',
    'datalist',
    'fieldset',
    'form',
    'input',
    'label',
    'legend',
    'meter',
    'optgroup',
    'option',
    'output',
    'progress',
    'select',
    'textarea',
    # Interactive elements
    'details',
    'dialog',
    # 'menu', # Experimental
    'summary',
    # Web Components
    'slot',
    'template',    
]

elements = {}

for element in element_list:
    elements[element] = element

void_element_list = [
    'area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input', 'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr'
]

void_elements = {}

for element in void_element_list:
    void_elements[element] = element
