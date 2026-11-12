function hamburger(x) {
    x.classList.toggle("change");
    };

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
    });
});


