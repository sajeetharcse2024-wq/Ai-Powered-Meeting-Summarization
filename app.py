import streamlit as st
import pandas as pd
import sqlite3
import re
from datetime import date
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="AI Meeting Summarizer",
    page_icon="📝",
    layout="wide"
)

# Database setup
conn = sqlite3.connect("meetings.db", check_same_thread=False)
conn.execute("""
CREATE TABLE IF NOT EXISTS meetings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    meeting_date TEXT,
    summary TEXT,
    decisions TEXT,
    actions TEXT,
    questions TEXT
)
""")
conn.commit()

# Text processing
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def generate_summary(text):
    sentences = re.split(r'(?<=[.!?])\s+', clean_text(text))
    sentences = [s for s in sentences if len(s.strip()) > 10]
    return " ".join(sentences[:3]) if sentences else "No summary could be generated."


def extract_decisions(text):
    keywords = ["decided", "agreed", "approved", "selected", "chosen"]
    return [
        line.strip() for line in text.splitlines()
        if any(word in line.lower() for word in keywords)
    ]


def extract_actions(text):
    keywords = ["will", "must", "should", "assigned", "responsible"]
    return [
        line.strip() for line in text.splitlines()
        if any(word in line.lower() for word in keywords)
    ]


def extract_questions(text):
    return [
        line.strip() for line in text.splitlines()
        if "?" in line or "need to decide" in line.lower()
    ]


# Application interface
st.title("AI-Powered Meeting Summarization System")
st.write("Upload meeting transcripts and generate structured meeting summaries.")

st.divider()

st.header("1. Meeting Details")

col1, col2 = st.columns(2)

with col1:
    meeting_title = st.text_input("Meeting Title")

with col2:
    meeting_date = st.date_input("Meeting Date", value=date.today())

st.header("2. Transcript Intake")

uploaded_file = st.file_uploader(
    "Upload meeting transcript",
    type=["txt", "srt"]
)

transcript = ""

if uploaded_file:
    raw = uploaded_file.read().decode("utf-8", errors="replace")
    if uploaded_file.name.endswith(".srt"):
        transcript = re.sub(
            r'\d{2}:\d{2}:\d{2},\d{3} --> .*',
            '',
            raw
        )
        transcript = re.sub(r'^\d+\s*$', '', transcript, flags=re.MULTILINE)
    else:
        transcript = raw

transcript = st.text_area(
    "Or paste your meeting transcript here",
    value=transcript,
    height=200
)

if st.button("Generate Meeting Summary", type="primary"):
    if not meeting_title.strip():
        st.error("Please enter a meeting title.")
    elif not transcript.strip():
        st.error("Please upload or enter a transcript.")
    else:
        cleaned = clean_text(transcript)

        st.session_state["summary"] = generate_summary(cleaned)
        st.session_state["decisions"] = "\n".join(extract_decisions(transcript))
        st.session_state["actions"] = "\n".join(extract_actions(transcript))
        st.session_state["questions"] = "\n".join(extract_questions(transcript))
        st.session_state["generated"] = True
        st.session_state["title"] = meeting_title
        st.session_state["meeting_date"] = str(meeting_date)

        st.success("Meeting analysis completed!")

# Results and human review
if st.session_state.get("generated", False):

    st.divider()
    st.header("3. Generated Meeting Results")

    st.subheader("Overall Meeting Summary")
    st.session_state["summary"] = st.text_area(
        "Review and edit summary",
        value=st.session_state["summary"],
        height=120
    )

    st.subheader("Important Decisions")
    st.session_state["decisions"] = st.text_area(
        "Review decisions",
        value=st.session_state["decisions"],
        height=100
    )

    st.subheader("Action Items")
    st.session_state["actions"] = st.text_area(
        "Review action items",
        value=st.session_state["actions"],
        height=120
    )

    st.subheader("Unresolved Questions")
    st.session_state["questions"] = st.text_area(
        "Review unresolved questions",
        value=st.session_state["questions"],
        height=100
    )

    st.divider()
    st.header("4. Review and Approval")

    approved = st.checkbox(
        "I have reviewed and approved this meeting summary."
    )

    if approved:
        st.success("Summary approved. You can now save and export it.")

        if st.button("Save Approved Summary"):
            conn.execute(
                """INSERT INTO meetings
                (title, meeting_date, summary, decisions, actions, questions)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    st.session_state["title"],
                    st.session_state["meeting_date"],
                    st.session_state["summary"],
                    st.session_state["decisions"],
                    st.session_state["actions"],
                    st.session_state["questions"]
                )
            )
            conn.commit()
            st.success("Meeting summary saved successfully!")

    report = f"""
# Meeting Summary

Title: {st.session_state['title']}
Date: {st.session_state['meeting_date']}

## Overall Summary
{st.session_state['summary']}

## Decisions
{st.session_state['decisions'] or 'Unspecified'}

## Action Items
{st.session_state['actions'] or 'Unspecified'}

## Unresolved Questions
{st.session_state['questions'] or 'None identified'}

## Review Status
Human review required before sharing.
"""

    st.download_button(
        "Download Meeting Summary",
        data=report,
        file_name="meeting_summary.md",
        mime="text/markdown"
    )

st.divider()

st.header("5. Search Previous Meetings")

search = st.text_input("Search approved meeting summaries")

if search:
    results = conn.execute(
        """SELECT title, meeting_date, summary
        FROM meetings WHERE title LIKE ? OR summary LIKE ?""",
        (f"%{search}%", f"%{search}%")
    ).fetchall()

    if results:
        for result in results:
            st.write(f"**{result[0]}** — {result[1]}")
            st.write(result[2])
            st.divider()
    else:
        st.info("No matching approved meetings found.")

st.caption(
    "Responsible AI: Outputs are generated using local text-matching "
    "rules, not a trained AI model. Verify all information before sharing. "
    "Unknown owners and dates should be confirmed manually."
)