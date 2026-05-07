"""
Streamlit app: Markdown (e.g. README.md) → printable PDF.
Uses HTML as an intermediate format and xhtml2pdf for raster-free PDF output.
"""

from __future__ import annotations

from io import BytesIO
from string import Template

import markdown
import streamlit as st
from xhtml2pdf import pisa

# string.Template avoids brace clashes with CSS `{ ... }`.
PRINT_CSS = Template(
    """
@page {
  size: $page_size;
  margin: $margin_top $margin_side $margin_bottom $margin_side;
}

html {
  font-size: 11pt;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  line-height: 1.5;
  color: #24292f;
  word-wrap: break-word;
}

article {
  max-width: none;
}

h1, h2, h3, h4, h5, h6 {
  margin-top: 1.2em;
  margin-bottom: 0.35em;
  font-weight: 600;
  line-height: 1.25;
  page-break-after: avoid;
}

h1 {
  font-size: 1.75em;
  border-bottom: 1px solid #d0d7de;
  padding-bottom: 0.2em;
}

h2 {
  font-size: 1.4em;
  border-bottom: 1px solid #eaeef2;
  padding-bottom: 0.15em;
}

p {
  margin: 0.5em 0;
}

pre, code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 0.9em;
}

pre {
  padding: 0.75rem 1rem;
  background: #f6f8fa;
  border: 1px solid #d0d7de;
  border-radius: 6px;
  overflow-wrap: anywhere;
  white-space: pre-wrap;
  page-break-inside: avoid;
}

code {
  background: rgba(175,184,193,0.2);
  padding: 0.15em 0.35em;
  border-radius: 4px;
}

pre code {
  background: transparent;
  padding: 0;
}

blockquote {
  margin: 1em 0;
  padding: 0 1em;
  color: #57606a;
  border-left: 0.25em solid #d0d7de;
}

ul, ol {
  padding-left: 1.75em;
  margin: 0.5em 0;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0;
  font-size: 0.95em;
  page-break-inside: avoid;
}

th, td {
  border: 1px solid #d0d7de;
  padding: 6px 10px;
}

th {
  background: #f6f8fa;
  font-weight: 600;
}

tr:nth-child(even) td {
  background: #fafbfc;
}

img {
  max-width: 100%;
  height: auto;
}

a {
  color: #0969da;
  text-decoration: none;
}

hr {
  margin: 1.5rem 0;
  border: 0;
  border-top: 1px solid #d0d7de;
}

/* Avoid orphaned headings across pages where the engine respects it */
h1 + *, h2 + *, h3 + * {
  page-break-before: avoid;
}
"""
)


def _page_size_slug(choice: str) -> str:
    return {"A4": "a4", "Letter": "letter"}.get(choice, "a4")


def _margin_css(preset: str) -> tuple[str, str, str]:
    presets = {
        "Comfortable": ("2cm", "1.75cm", "2cm"),
        "Tight": ("1.25cm", "1.25cm", "1.25cm"),
        "Wide": ("2.5cm", "2cm", "2.5cm"),
    }
    return presets.get(preset, presets["Comfortable"])


def markdown_to_html(md_text: str) -> str:
    return markdown.markdown(
        md_text,
        extensions=[
            "extra",
            "tables",
            "fenced_code",
            "nl2br",
            "sane_lists",
        ],
    )


def render_pdf(html_body: str, page_size_key: str, margin_preset: str) -> tuple[bytes, int]:
    mt, ms, mb = _margin_css(margin_preset)
    css = PRINT_CSS.substitute(
        page_size=_page_size_slug(page_size_key),
        margin_top=mt,
        margin_bottom=mb,
        margin_side=ms,
    )
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>Document</title>
  <style>{css}</style>
</head>
<body>
  <article>{html_body}</article>
</body>
</html>"""
    buffer = BytesIO()
    status = pisa.CreatePDF(
        src=full_html,
        dest=buffer,
        encoding="utf-8",
    )
    return buffer.getvalue(), int(status.err)


def default_output_name(upload_name: str | None) -> str:
    if not upload_name:
        return "README.pdf"
    base = upload_name.rsplit(".", 1)[0].strip()
    return f"{base}.pdf" if base else "README.pdf"


def main() -> None:
    st.set_page_config(
        page_title="Markdown → PDF",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("README / Markdown → PDF")
    st.caption(
        "Upload a `.md` file or paste Markdown, then download a printable PDF. "
        "Tables, headings, fenced code blocks, and blockquotes are styled for printing."
    )

    with st.sidebar:
        st.header("Print layout")
        page_size = st.selectbox("Page size", ["A4", "Letter"], index=0)
        margins = st.selectbox("Margins", ["Comfortable", "Tight", "Wide"], index=0)
        st.divider()
        st.markdown(
            "**Notes**\n\n"
            "- Remote images may not render if fetching fails offline.\n"
            "- Paths like `./img.png` in Markdown are relative to the server "
            "(uploaded text only)—use absolute image URLs when possible."
        )

    uploaded = st.file_uploader(
        "Upload a Markdown file",
        type=["md", "markdown", "txt"],
        help="Typical: README.md",
    )
    paste = st.text_area(
        "Or paste Markdown here",
        height=220,
        placeholder="# Title\n\nYour content…",
    )

    md_source: str | None = None
    source_label: str | None = None
    if uploaded is not None:
        md_source = uploaded.getvalue().decode("utf-8", errors="replace")
        source_label = uploaded.name
    elif paste.strip():
        md_source = paste
        source_label = None

    col_a, col_b = st.columns([1, 1])
    with col_a:
        generate = st.button("Generate PDF", type="primary", disabled=not md_source)
    with col_b:
        if md_source:
            st.caption(f"Input: **{len(md_source):,}** characters")

    if generate and md_source:
        with st.spinner("Building PDF…"):
            html_body = markdown_to_html(md_source)
            pdf_bytes, err_count = render_pdf(html_body, page_size, margins)
        if err_count:
            st.warning(
                f"PDF was created with {err_count} layout warning(s). "
                "Check the output; complex HTML can sometimes trip the PDF engine."
            )
        else:
            st.success("PDF ready — use the download button below.")
        out_name = default_output_name(source_label)
        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name=out_name,
            mime="application/pdf",
        )


if __name__ == "__main__":
    main()
