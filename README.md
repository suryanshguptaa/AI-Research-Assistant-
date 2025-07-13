# 🔬 AI Research Assistant

A local, privacy-first research assistant that analyzes PDF, TXT, or DOCX documents using LLaMA (GGUF) and modern retrieval-augmented generation (RAG) techniques.  
Features include instant summarization, contextual Q&A, and comprehension challenges—all in a user-friendly web interface.

---
> 🎬 **Demo Video:** [Watch on YouTube](https://youtu.be/gL2ZytDPNec)
**![Demo Screenshot](https://drive.google.com/file/d/1rmle4LsvJ4i5Id4upXSpo6SzJ-22lglW/view?usp=sharing)**


---

## 🎯 Features

- **Ask Anything Mode:**  
  Intelligent Q&A with document citations, context-aware responses, and conversation history.
- **Challenge Me Mode:**  
  AI-generated comprehension questions, automated answer evaluation, and feedback.
- **Auto-Summarization:**  
  Instant document summaries (≤150 words) for quick insights.
- **Privacy-First:**  
  100% local processing, no data leaves your machine, offline capable.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+ (3.11 recommended)
- 8GB+ RAM (16GB recommended)
- LLaMA GGUF model (see below)

### Installation

```
git clone https://github.com/yourusername/AI-Research-Assistant-.git
cd AI-Research-Assistant-
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
```

### Model Setup

1. **Download a LLaMA GGUF model** (e.g., LLaMA-2-7B-Chat) and place it in a folder like `C:\model\`.
2. **If you have a GGML model, convert it to GGUF:**  
   ```
   git clone https://github.com/ggerganov/llama.cpp.git
   python llama.cpp/convert-llama-ggmlv3-to-gguf.py \
     --input "path/to/your/model.ggmlv3.bin" \
     --output "path/to/your/model.gguf"
   ```
3. **Update `config/settings.py`:**
   ```
   MODEL_PATH = r"C:\model\llama-2-7b-chat.gguf"
   ```

### Run the App

```
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🏗️ Architecture

```
User (Browser)
    │
    ▼
Streamlit UI  ──►  Document Processor  ──►  Text Chunker  ──►  Embedding Generator
    │                                                           │
    │                                                           ▼
    └──────────── Q&A / Challenge ──►  Vector Search (ChromaDB) ──►  LLaMA Model
```

- **Frontend:** Streamlit + Custom CSS
- **Document Processing:** PyPDF2, pdfplumber, python-docx
- **Embeddings:** SentenceTransformers (all-MiniLM-L6-v2)
- **Vector Store:** ChromaDB
- **LLM Engine:** LangChain + LLaMA GGUF (local)
- **RAG Pipeline:** Retrieval-augmented generation for grounded answers

---

## 📚 Example Workflow

1. **Upload a document** (PDF, TXT, or DOCX).
2. **Automatic summary** is generated.
3. **Ask questions** like:  
   *"What are the main findings?"*  
   *"Summarize the methodology."*
4. **Challenge Me:**  
   Get AI-generated questions, answer them, and receive instant feedback.

---

## ⚙️ Configuration

Edit `config/settings.py` to adjust:
- Model path, context length, temperature
- Chunk size and overlap
- UI settings

---

## 🛠️ Project Structure

```
AI-Research-Assistant-/
├── app.py
├── requirements.txt
├── config/
│   ├── settings.py
│   └── prompts.py
├── src/
│   ├── document_processor.py
│   └── vector_store.py
├── helpers/
│   ├── langchain_helper.py
│   └── ui_helper.py
├── data/
│   ├── documents/
│   ├── embeddings/
│   └── vectorstore/
└── README.md
```

---

## 🐞 Troubleshooting

- **Model not loading:** Use GGUF format and correct path.
- **No results:** Make sure a document is processed and selected before asking questions.
- **Add text paste:** Add a `st.text_area` in the sidebar if you want manual text input.

---

## 📄 License

MIT License

---

## 🙏 Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain)
- [Meta AI](https://ai.meta.com/)
- [ChromaDB](https://www.trychroma.com/)
- [Streamlit](https://streamlit.io/)
- [Open Source Community](https://github.com/)

---

**How to use:**
- Replace `yourusername` in the GitHub URLs with your actual GitHub username.
- Replace `image.jpg` with the actual path/filename of your screenshot in the repo.
- Add/adjust sections as needed for your project.

**This README is now ready to copy-paste into your GitHub repo!**
