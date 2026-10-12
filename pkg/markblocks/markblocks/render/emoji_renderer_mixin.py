import emoji

class EmojiRendererMixin:
    def Emoji(self, node):
        #print(node.name)
        self(emoji.emojize(f":{node.name}:", language='alias'))
        
