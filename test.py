def slugify(title):
    slug = title.lower()
    for c in slug:
        if not c.isalnum() and c != "-":
            slug = slug.replace(c, "-")
            slug = slug.strip("-")
    return slug

print(slugify("Is it too early to decorate for Christmas?"))