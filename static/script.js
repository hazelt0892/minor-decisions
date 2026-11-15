function hamburger(x) {
    x.classList.toggle("change");
    }

document.addEventListener("DOMContentLoaded", function() {

    ham = document.querySelector("#hamburger");
    navLinks = document.querySelectorAll("nav li");
    menu = document.getElementById("menu");
    active = false;
    ham.addEventListener("click", function() {
        if (active == false) {
            navLinks.forEach(function(link) {
                link.classList.toggle("active");
            });
            menu.style.width = "100vw";
            menu.style.position = "fixed";
            ham.style.position = "static";
            active = true;
        }
        else {
            navLinks.forEach(function(link) {
                link.classList.remove("active");
            });
            menu.style.width = "0";
            menu.style.position = "absolute";
            ham.style.position = "absolute";
            active = false;
        }
    })

    const password = document.getElementById("password")
    const confirmation = document.getElementById("confirmation")

    function checkPassword() {
        if (confirmation.value === "") {
            confirmation.setCustomValidity("");
        }
        else if (password.value != confirmation.value) {
            confirmation.setCustomValidity("Passwords do not match");
        }
        else {
            confirmation.setCustomValidity("");
        }
    }

    if (password && confirmation){
        password.addEventListener("input", checkPassword);
        confirmation.addEventListener("input", checkPassword);
    }

    document.addEventListener("click", async function(event) {
        const save = event.target.closest(".save");
        if (!save) {
            return;
        }
        const treeId = save.dataset.treeId;
        const response = await fetch(`/save/${treeId}`, {
            method: "POST"
        });

        if (response.status === 401) {
            window.location.href = "/login";
            return;
        }

        if (response.ok) {
            const data = response.json();
            save.classList.toggle("fa-solid", data.saved);
            save.classList.toggle("fa-regular", !data.saved);
        }
    })

})






