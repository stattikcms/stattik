from loguru import logger

import stattik.renderer

def create_renderer():
    return stattik.renderer.create_renderer()
