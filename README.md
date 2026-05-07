# Markdown → PDF (Streamlit)

Turn any **Markdown** file—especially **`README.md`**—into a **print-ready PDF** from your browser. Upload a `.md` file or paste content, pick **A4** or **Letter** and margins, then download.

**Keywords:** markdown to pdf, readme to pdf, streamlit converter, printable documentation, GitHub readme pdf, python pdf generator.

---

## Features

- **Upload** `.md`, `.markdown`, or `.txt`, **or paste** Markdown in the app.
- **Print-oriented styling**: headings, tables, fenced code blocks, blockquotes, lists.
- **Layout controls**: page size (**A4** / **Letter**) and margin presets (**Comfortable** / **Tight** / **Wide**).
- **Local-first**: runs on your machine; no account required.

---

## Quick start

Requires **Python 3.10+** (3.11 recommended).

```bash
git clone https://github.com/YOUR_USERNAME/md-readme-to-pdf.git
cd md-readme-to-pdf

python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

streamlit run app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`), add your Markdown, click **Generate PDF**, then **Download PDF**.

### Documentation (GitHub Pages)

The full **usage guide** lives in [`docs/index.html`](docs/index.html). To host it: **Settings → Pages → Build and deployment → Branch: main, Folder: `/docs`**. Your site will be at `https://YOUR_USERNAME.github.io/REPO_NAME/` (replace with your username and repo).

---

## Stack

| Piece | Role |
| --- | --- |
| [Streamlit](https://streamlit.io/) | Web UI |
| [Python-Markdown](https://python-markdown.github.io/) | Markdown → HTML (tables, fenced code, extras) |
| [xhtml2pdf](https://github.com/xhtml2pdf/xhtml2pdf) | HTML/CSS → PDF |

---

## Limitations

- **Remote images** (badges, diagrams hosted on URLs) only appear if the PDF engine can fetch them; corporate proxies or SSL issues may block downloads.
- **Relative image paths** (for example `./assets/diagram.png`) are not resolved from a repo on disk when you only paste or upload a single file—use **absolute URLs** for images if you need them in the PDF.

---

## Suggested GitHub topics (tags)

Add these under **Settings → General → Topics** so others can discover the repo:

`streamlit` · `markdown` · `pdf` · `readme` · `converter` · `documentation` · `python` · `xhtml2pdf` · `python-markdown` · `printable` · `export-pdf` · `markdown-to-pdf` · `readme-to-pdf` · `static-site` · `devtools`

---

## License

Specify your license here (for example MIT). If you omit a license, default copyright applies and others may be unsure whether they can reuse the code.
