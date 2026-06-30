from tools.internet import search_web

results = search_web(
    "latest news about artificial intelligence"
)

for item in results:

    print("\nTITLE:")
    print(item["title"])

    print("\nTEXT:")
    print(item["body"])

    print("\nURL:")
    print(item["url"])

    print("\n" + "=" * 50)