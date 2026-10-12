from loguru import logger

import stattik.baker


def create_baker():
    return stattik.baker.create_baker()
