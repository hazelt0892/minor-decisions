let tree = null;
let visited = [];

const question = document.getElementById("question");
const answers = document.getElementById("answers");
const back = document.getElementById("back");

async function loadTree() {
    const slug = document.getElementById("question_box").dataset.slug;
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
    }
    else {
        question.classList.remove("result");
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
