import spacy
from collections import Counter
import string
from flask import Flask, request, render_template

app = Flask(__name__)

# Load spaCy English model once when the app starts
# This might take a moment, and it's better to do it outside request handling
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading 'en_core_web_sm' model...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def summarize_text_spacy(text, num_sentences=3):
    if not text.strip():
        return "" # Return empty if input text is empty or just whitespace
    doc = nlp(text)

    # Create a list of stop words and punctuation
    stop_words = spacy.lang.en.stop_words.STOP_WORDS
    punctuation = string.punctuation + "\n" # Add newline to punctuation

    # Build word frequency dictionary
    word_frequencies = {}
    for token in doc:
        if token.text.lower() not in stop_words and token.text.lower() not in punctuation:
            if token.lemma_.lower() not in word_frequencies: # Use lemma for better grouping
                word_frequencies[token.lemma_.lower()] = 1
            else:
                word_frequencies[token.lemma_.lower()] += 1
    
    if not word_frequencies: # Handle cases where text is all stop words/punctuation
        # Return first few sentences or a message
        sentences = [sent.text.strip() for sent in doc.sents]
        return ' '.join(sentences[:num_sentences]) if sentences else "Could not generate summary from the provided text."


    # Normalize word frequencies
    max_freq = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] /= max_freq

    # Score sentences based on word frequency
    sentence_scores = {}
    for sent in doc.sents:
        for token in sent:
            if token.lemma_.lower() in word_frequencies: # Check lemma in frequencies
                if sent not in sentence_scores:
                    sentence_scores[sent] = word_frequencies[token.lemma_.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[token.lemma_.lower()]

    if not sentence_scores: # If no sentences could be scored
        sentences = [sent.text.strip() for sent in doc.sents]
        return ' '.join(sentences[:num_sentences]) if sentences else "Could not generate summary from the provided text."

    # Select top N sentences
    summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    
    # Ensure we don't request more sentences than available
    num_to_select = min(num_sentences, len(summarized_sentences))
    
    summary = ' '.join([str(sent).strip() for sent in summarized_sentences[:num_to_select]])

    return summary

@app.route('/', methods=['GET', 'POST'])
def index():
    original_text = ""
    summary = ""
    num_sentences = 2 # Default number of sentences for summary

    if request.method == 'POST':
        original_text = request.form.get('text_input', '')
        num_sentences_str = request.form.get('num_sentences', '2')
        try:
            num_sentences = int(num_sentences_str)
            if num_sentences <= 0:
                num_sentences = 2 # Default to 2 if invalid input
        except ValueError:
            num_sentences = 2 # Default if conversion fails

        if original_text:
            summary = summarize_text_spacy(original_text, num_sentences)
        else:
            summary = "Please enter some text to summarize."

    return render_template('index.html', original_text=original_text, summary=summary, num_sentences=num_sentences)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)