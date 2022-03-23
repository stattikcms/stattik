from post import Post

external_data = {
    "id": 1,
    "title": "Hello World",
    "date": "2018-09-14 07:42:34",
    "description": "A developer blog is born",
    "cover": "https://i.imgur.com/Uv6nv7k.jpg",
    "slug": "hello-world",
    "category": "",
}

def main():
    post = Post(**external_data)
    print(post.id)
    print(post.date)
    print(post.dict())
    print(Post.schema_json(indent=2))




if __name__ == "__main__":
    main()