AI-Powered Meeting Summarization System

Project Overview

The AI-Powered Meeting Summarization System is a Python-based application that helps users convert meeting transcripts into organized and easy-to-understand summaries.

It extracts important information from meeting discussions and displays it in a structured format.

Features

- Enter or paste meeting transcripts.
- Generate an overall meeting summary.
- Identify important decisions.
- Extract action items.
- Display unresolved questions.
- Review and approve generated summaries.
- Download meeting summaries.
- Save and search previous meetings.

Technologies Used

- Python
- Streamlit
- Pandas
- spaCy
- SQLite
- python-docx
- pysrt

Installation and Execution

1. Install Python.

2. Install the required packages:
   
   "pip install -r requirements.txt"

3. Run the application:
   
   "streamlit run app.py"

4. Open the local address displayed in the terminal.

Project Structure

- "app.py" – Main application.
- "data/" – Sample meeting transcript and project data.
- "requirements.txt" – Required Python packages.
- ".gitignore" – Files excluded from GitHub.

Current Implementation

This is a working prototype that uses rule-based text processing to identify meeting information. Its results should be reviewed by a human before sharing. It does not yet use an integrated generative AI model.

Future Enhancements

- Integration with a generative AI model.
- Improved topic segmentation.
- Support for more transcript formats.
- Enhanced speaker identification.
- Better summary accuracy and evidence tracking.

Conclusion

This project aims to make meeting documentation easier by organizing discussions, decisions, action items, and unresolved questions in one application.