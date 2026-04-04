function showTab(tab) {
    document.querySelectorAll(".tab").forEach(t => t.classList.add("hidden"));
    document.getElementById(tab).classList.remove("hidden");
}

async function send() {
    let msg = document.getElementById("msg").value;

    let res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({message: msg})
    });

    let data = await res.json();

    document.getElementById("chat-box").innerHTML += `
        <div>🧑 ${msg}</div>
        <div>🤖 ${data.response}</div>
        <div>⭐ Reward: ${data.reward}</div>
    `;
}

async function summarize() {
    let text = document.getElementById("text").value;

    let res = await fetch("/summarize", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({text})
    });

    let data = await res.json();
    document.getElementById("sum").innerText = data.summary;
}

async function uploadPDF() {
    let file = document.getElementById("pdfFile").files[0];
    let form = new FormData();
    form.append("file", file);

    await fetch("/upload", {method:"POST", body: form});
    alert("PDF Uploaded");
}

async function askPDF() {
    let q = document.getElementById("pdfQ").value;

    let res = await fetch("/ask_pdf", {
        method:"POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({question: q})
    });

    let data = await res.json();
    document.getElementById("pdfAns").innerText = data.answer;
}