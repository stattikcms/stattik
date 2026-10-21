import emoji

class EmojiRendererMixin:
    def Emoji(self, node):
        self(emoji.emojize(f":{node.name}:", language='alias'))
        
