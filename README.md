# Multilingual Voice Translator with Sentiment Analysis

## Project Overview

This project facilitates real-time communication across over 20 Indian languages by integrating voice recognition and sentiment analysis. Users can translate their spoken input into various languages with a latency of under 3 seconds, enhancing communication across linguistic barriers.

## Key Features

- **Voice Recognition**: Captures spoken input in real-time.
- **Multilingual Support**: Translates speech into languages such as Hindi, Tamil, Telugu, Kannada, and Bengali.
- **Sentiment Analysis**: Utilizes the VADER model to classify sentiment, achieving 80% accuracy.
- **Conversation Logging**: Maintains a log of interactions, including timestamps, source and target languages, input texts, translated texts, and sentiment scores.
- **User-Friendly Interface**: Easily interact through voice commands to choose target languages.

## Technologies Used

- Python
- Pygame
- SpeechRecognition
- Google Translate API
- NLTK (Natural Language Toolkit)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/karthikram-p/SentimentSpeak.git
   cd SentimentSpeak

2. **Install required packages**: Make sure you have Python installed. Then, use pip to install the necessary libraries:
   ```bash
   pip install pygame SpeechRecognition googletrans==4.0.0-rc1 nltk

3. **Download NLTK resources**: Open a Python shell and run:
   ```bash
   import nltk
   nltk.download('punkt')
   nltk.download('vader_lexicon')

## Usage
 1. **Run the application**:
    ```bash
    python nlp.py
 2. **Speak your input**: The application will recognize your speech and prompt you to choose a target language.

 3. **Review translations and sentiment analysis**: The application will log your conversation and display sentiment scores.
