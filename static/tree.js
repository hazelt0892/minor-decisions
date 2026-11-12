let tree = null;
let visited = [];

const question = document.getElementById("question");
const answers = document.getElementById("answers");
const back = document.getElementById("back");
const verdict = document.getElementById("verdict");
const exit = document.getElementById("exit");

async function loadTree() {
    const slug = document.getElementById("question-box").dataset.slug;
    const response = await fetch(`/api/tree/${slug}`);
    tree = await response.json();
    showNode(tree.start);
}

function showNode(nodeId) {
    const node = tree.nodes[nodeId];
    visited.push(nodeId);

    question.textContent = node.text;
    answers.innerHTML = "";

    if (node.is_result) {
        question.classList.add("result");
        verdict.style.display = "inline";
        exit.style.display = "inline";
    }
    else {
        question.classList.remove("result");
        verdict.style.display = "none";
        exit.style.display = "none";
        for (const option of node.options) {
            const button = document.createElement("button");
            button.textContent = option.label;
            button.addEventListener("click", () => showNode(option.next));
            answers.appendChild(button);
        }
    }
    back.hidden = visited.length < 2;
}

back.addEventListener("click", () => {
    visited.pop();
    const previous = visited.pop();
    showNode(previous);
});

loadTree();
