"""
Milestone 5 — Gradio web interface.

Run:
    python app.py
Then open http://localhost:7860
"""

import gradio as gr

from rag import ask


def handle_query(question: str) -> tuple[str, str]:
    if not question.strip():
        return "", ""
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks(title="DACA Unofficial Guide 2026") as demo:
    gr.Markdown(
        "## DACA Unofficial Guide 2026\n"
        "Ask questions about DACA renewals, delays, and 2026 policy changes. "
        "Answers are grounded in curated sources — not general AI knowledge."
    )
    inp = gr.Textbox(
        label="Your question",
        placeholder="e.g. When should I submit my DACA renewal?",
    )
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()
