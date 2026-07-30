"""
Healthcare Security Code Review – Streamlit Web Application
Author : Vijay Sharma
Course : DSC670-T301 Advanced Uses of Generative AI
Date   : May 2026

Uses the fine-tuned OpenAI model produced in Milestone 2 to generate
HIPAA-aware security review comments for healthcare data-pipeline code diffs.

Run:
    streamlit run app.py

Required environment variables:
    OPENAI_API_KEY        – your OpenAI API key
    FINE_TUNED_MODEL      – fine-tuned model name (e.g. ft:gpt-4o-mini-2024-07-18:...)
                            Falls back to BASE_MODEL if not set.
"""

import os
import time
import textwrap

import streamlit as st
from openai import OpenAI

# ── Constants ────────────────────────────────────────────────────────────────
BASE_MODEL = "gpt-4o-mini-2024-07-18"
FINE_TUNED_MODEL = os.environ.get("FINE_TUNED_MODEL", BASE_MODEL)

SYSTEM_PROMPT = (
    "You are a healthcare security code reviewer specializing in HIPAA-compliant data pipelines. "
    "Review code diffs and produce structured security comments that identify PHI exposure risks, "
    "unsafe logging, missing validation, and error handling gaps. "
    "Format each finding as:\n"
    "  SECURITY RISK [SEVERITY]: <issue>\n"
    "  FIX: <concrete code-level recommendation>\n"
    "Cite relevant HIPAA rules where applicable."
)

SAMPLE_DIFFS = {
    "PHI in logs + eval()": """\
diff --git a/parser.py b/parser.py
--- a/parser.py
+++ b/parser.py
@@ -0,0 +1,9 @@
+import requests
+
+def fetch_and_parse_record(url, token):
+    headers = {'Authorization': token}
+    response = requests.get(url, headers=headers, verify=False)
+    record = eval(response.text)
+    patient_ssn = record['ssn']
+    print(f'Processing SSN: {patient_ssn}')
+    return record
""",
    "Hardcoded credentials": """\
diff --git a/db_connect.py b/db_connect.py
--- a/db_connect.py
+++ b/db_connect.py
@@ -0,0 +1,8 @@
+import psycopg2
+
+def get_connection():
+    return psycopg2.connect(
+        host='prod-db.hospital.internal',
+        user='phi_admin',
+        password='S3cr3tP@ss!',
+        dbname='patient_records'
+    )
""",
    "Unencrypted PHI export": """\
diff --git a/export.py b/export.py
--- a/export.py
+++ b/export.py
@@ -0,0 +1,10 @@
+import csv
+
+def export_patients(records, filepath):
+    with open(filepath, 'w', newline='') as f:
+        writer = csv.DictWriter(f, fieldnames=['name','dob','ssn','diagnosis'])
+        writer.writeheader()
+        for r in records:
+            writer.writerow(r)
+    print(f'Exported {len(records)} records to {filepath}')
""",
    "SQL injection in patient lookup": """\
diff --git a/lookup.py b/lookup.py
--- a/lookup.py
+++ b/lookup.py
@@ -0,0 +1,8 @@
+import sqlite3
+
+def find_patient(conn, patient_id):
+    cursor = conn.cursor()
+    query = f"SELECT * FROM patients WHERE id = {patient_id}"
+    cursor.execute(query)
+    return cursor.fetchone()
""",
}

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Healthcare Security Code Reviewer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .risk-box {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem 1.2rem;
        border-radius: 4px;
        font-family: monospace;
        white-space: pre-wrap;
        font-size: 0.9rem;
    }
    .ft-box {
        background: #d1ecf1;
        border-left: 5px solid #17a2b8;
        padding: 1rem 1.2rem;
        border-radius: 4px;
        font-family: monospace;
        white-space: pre-wrap;
        font-size: 0.9rem;
    }
    .model-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .badge-base { background:#e2e3e5; color:#383d41; }
    .badge-ft   { background:#cce5ff; color:#004085; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image(
        "https://img.icons8.com/color/96/hospital.png",
        width=64,
    )
    st.title("⚙️ Settings")

    api_key_input = st.text_input(
        "OpenAI API Key",
        value=os.environ.get("OPENAI_API_KEY", ""),
        type="password",
        help="Set OPENAI_API_KEY env var or enter here. Never committed to source control.",
    )

    ft_model_input = st.text_input(
        "Fine-Tuned Model Name",
        value=FINE_TUNED_MODEL,
        help="The ft:gpt-4o-mini-... model name produced by Milestone 2.",
    )

    st.divider()
    compare_mode = st.toggle(
        "Compare vs. Base Model",
        value=True,
        help="Run the same diff through both the fine-tuned and base model side-by-side.",
    )

    temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.05)
    max_tokens = st.slider("Max tokens", 200, 1200, 700, 50)

    st.divider()
    st.markdown("**About**")
    st.caption(
        "DSC670 · Milestone 2 · Vijay Sharma\n\n"
        "Fine-tuned `gpt-4o-mini-2024-07-18` on 10 curated healthcare "
        "pipeline diffs to produce structured, HIPAA-aware security review comments."
    )

# ── Header ───────────────────────────────────────────────────────────────────
st.title("🏥 Healthcare Security Code Reviewer")
st.markdown(
    "Paste a **git diff** below (or choose a sample) and the fine-tuned model will "
    "generate structured, HIPAA-aware security review comments."
)

# ── Sample selector ───────────────────────────────────────────────────────────
sample_choice = st.selectbox(
    "Load a sample diff",
    options=["— paste your own —"] + list(SAMPLE_DIFFS.keys()),
)

# ── Diff input ────────────────────────────────────────────────────────────────
placeholder_diff = (
    SAMPLE_DIFFS[sample_choice]
    if sample_choice != "— paste your own —"
    else "Paste your git diff here…"
)

diff_input = st.text_area(
    "Code Diff",
    value=placeholder_diff,
    height=280,
    placeholder="Paste your git diff here…",
)

run_btn = st.button("🔍 Run Security Review", type="primary", use_container_width=True)

# ── Helpers ───────────────────────────────────────────────────────────────────

def get_client(key: str) -> OpenAI:
    if not key:
        st.error("Please provide an OpenAI API key in the sidebar.")
        st.stop()
    return OpenAI(api_key=key)


def stream_review(client: OpenAI, model: str, diff: str, temperature: float, max_tokens: int):
    """Yield streamed text chunks from the chat completions API."""
    stream = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Review this code diff for security issues:\n\n{diff}",
            },
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


# ── Main output ───────────────────────────────────────────────────────────────
if run_btn:
    if not diff_input.strip() or diff_input.strip() == "Paste your git diff here…":
        st.warning("Please enter or select a code diff before running.")
        st.stop()

    client = get_client(api_key_input)
    effective_ft_model = ft_model_input.strip() or BASE_MODEL

    if compare_mode:
        col_ft, col_base = st.columns(2)

        with col_ft:
            st.markdown(
                f'<span class="model-badge badge-ft">Fine-Tuned Model</span>',
                unsafe_allow_html=True,
            )
            st.caption(f"`{effective_ft_model}`")
            ft_placeholder = st.empty()
            ft_text = ""
            t0 = time.time()
            for chunk in stream_review(client, effective_ft_model, diff_input, temperature, max_tokens):
                ft_text += chunk
                ft_placeholder.markdown(
                    f'<div class="ft-box">{ft_text}▌</div>', unsafe_allow_html=True
                )
            latency_ft = time.time() - t0
            ft_placeholder.markdown(
                f'<div class="ft-box">{ft_text}</div>', unsafe_allow_html=True
            )
            st.caption(f"⏱ {latency_ft:.2f}s")

        with col_base:
            st.markdown(
                '<span class="model-badge badge-base">Base Model</span>',
                unsafe_allow_html=True,
            )
            st.caption(f"`{BASE_MODEL}`")
            base_placeholder = st.empty()
            base_text = ""
            t0 = time.time()
            for chunk in stream_review(client, BASE_MODEL, diff_input, temperature, max_tokens):
                base_text += chunk
                base_placeholder.markdown(
                    f'<div class="risk-box">{base_text}▌</div>', unsafe_allow_html=True
                )
            latency_base = time.time() - t0
            base_placeholder.markdown(
                f'<div class="risk-box">{base_text}</div>', unsafe_allow_html=True
            )
            st.caption(f"⏱ {latency_base:.2f}s")

    else:
        st.markdown(
            f'<span class="model-badge badge-ft">Fine-Tuned Model</span>',
            unsafe_allow_html=True,
        )
        st.caption(f"`{effective_ft_model}`")
        placeholder = st.empty()
        result_text = ""
        t0 = time.time()
        for chunk in stream_review(client, effective_ft_model, diff_input, temperature, max_tokens):
            result_text += chunk
            placeholder.markdown(
                f'<div class="ft-box">{result_text}▌</div>', unsafe_allow_html=True
            )
        latency = time.time() - t0
        placeholder.markdown(
            f'<div class="ft-box">{result_text}</div>', unsafe_allow_html=True
        )
        st.caption(f"⏱ {latency:.2f}s")

    # ── Download button ──────────────────────────────────────────────────────
    report_lines = [
        "Healthcare Security Code Review Report",
        "=" * 50,
        f"Model: {effective_ft_model}",
        "",
        "CODE DIFF",
        "-" * 40,
        diff_input,
        "",
        "FINE-TUNED MODEL REVIEW",
        "-" * 40,
        ft_text if compare_mode else result_text,
    ]
    if compare_mode:
        report_lines += ["", "BASE MODEL REVIEW", "-" * 40, base_text]

    st.download_button(
        "⬇️ Download Report (.txt)",
        data="\n".join(report_lines),
        file_name="security_review_report.txt",
        mime="text/plain",
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "DSC670 · Milestone 2 · Vijay Sharma · Bellevue University · May 2026  "
    "| Fine-tuned on 10 curated HIPAA-focused security review examples."
)
