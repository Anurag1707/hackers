from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import PyPDF2
from env.environment import StudyEnv

app = Flask(__name__)

# Safe model loading (no crash)
def load_models():
    try:
        generator = pipeline(
            "text-generation",
            model="gpt2",
            device=-1
        )
    except:
        generator = None

    try:
        summarizer = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6"
        )
    except:
        summarizer = None

    return generator, summarizer

generator, summarizer = load_models()

env = StudyEnv()
pdf_text = ""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data["message"]

    # Fallback if model not loaded
    if generator:
        res = generator(msg, max_length=80)[0]['generated_text']
    else:
        res = f"AI Response (demo): {msg}"

    step = env.step("answer_question", res)

    return jsonify({
        "response": res,
        "reward": step.reward
    })

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.json
    text = data["text"]

    if summarizer:
        summary = summarizer(text[:1000])[0]['summary_text']
    else:
        summary = "Summary (demo mode)"

    return jsonify({"summary": summary})

@app.route("/upload", methods=["POST"])
def upload():
    global pdf_text

    file = request.files["file"]
    reader = PyPDF2.PdfReader(file)

    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text()

    return jsonify({"msg": "PDF Loaded"})

@app.route("/ask_pdf", methods=["POST"])
def ask_pdf():
    data = request.json
    q = data["question"]

    if generator:
        res = generator(q + " " + pdf_text[:500], max_length=100)[0]['generated_text']
    else:
        res = "PDF answer (demo)"

    return jsonify({"answer": res})

if __name__ == "__main__":
    app.run(debug=True)