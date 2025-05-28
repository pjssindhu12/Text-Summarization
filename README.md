# Text Summarizer Tool

This project is a simple web-based Text Summarization Tool built with Python, Flask, and spaCy. It allows users to paste or upload text and get a concise summary. The application is containerized using Docker.

## Core Features

-   GUI to paste text.
-   Summarization using spaCy (extractive method).
-   Display of original text and generated summary.
-   Editable summary output.
-   Configurable number of sentences for the summary.

## How it Works

The text summarization is performed using an extractive method based on word frequencies:

1.  **Text Preprocessing**: The input text is processed using the spaCy library.
2.  **Tokenization**: The text is broken down into individual words (tokens) and sentences.
3.  **Stop Word and Punctuation Removal**: Common words (like "the", "is", "in") and punctuation marks that don't contribute much to the meaning are removed.
4.  **Word Frequency Calculation**: The frequency of each significant word (using its base form/lemma) is calculated.
5.  **Frequency Normalization**: Word frequencies are normalized (scaled usually between 0 and 1) to provide a relative measure of importance.
6.  **Sentence Scoring**: Each sentence is scored based on the sum of the normalized frequencies of the words it contains.
7.  **Summary Generation**: The sentences with the highest scores are selected to form the summary, up to the user-specified number of sentences.

## Technologies Used

-   **Python**: Core programming language.
-   **Flask**: Micro web framework for the backend and serving the HTML interface.
-   **spaCy**: NLP library used for text processing and summarization logic (specifically the `en_core_web_sm` model).
-   **HTML/CSS**: For the frontend user interface.
-   **Docker**: For containerizing the application, ensuring consistent deployment and execution.

## Prerequisites

-   [Docker](https://www.docker.com/get-started) installed on your system.

## Getting Started

Follow these instructions to build and run the application using Docker.

### 1. Clone the Repository (or use your local files)

If this project were on a Git repository, you would clone it. Since you have the files locally, ensure all project files (`app.py`, `Dockerfile`, `requirements.txt`, `README.md`, and the `templates` directory with `index.html`) are in a single directory (e.g., `text_summarizer`).

### 2. Build the Docker Image

Open a terminal or command prompt, navigate to the project's root directory (where the `Dockerfile` is located), and run the following command:

```bash
docker build -t text-summarizer-app .