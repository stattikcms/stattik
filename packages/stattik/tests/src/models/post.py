"""
title: "Hello World"
date: 2018-09-14 07:42:34
description: A developer blog is born
cover: "https://i.imgur.com/Uv6nv7k.jpg"
slug: "hello-world"
category: ""
"""
from datetime import datetime

import pydantic

class Post(pydantic.BaseModel):
    id: int
    title: str
    date: datetime
    description: str
    cover: str
    slug: str
    category: str