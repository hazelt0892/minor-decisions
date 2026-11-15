def slugify(title):
    slug = title.lower()
    for c in slug:
        if not c.isalnum() and c != "-":
            slug = slug.replace(c, "-")
            slug = slug.strip("-")
    return slug

print(slugify("Is it too early to decorate for Christmas?"))

saves = document.querySelectorAll(".save");
    console.log(saves[0].tagName);
    for (let save of saves) {
        save.addEventListener("click", async function() {
            console.log("Bookmark clicked!");
            const treeId = this.dataset.treeId;
            const response = await fetch(`/save/${treeId}`, {
                method: "POST"
            });
            save.classList.toggle("fa-solid");
            save.classList.toggle("fa-regular");
        })
    }