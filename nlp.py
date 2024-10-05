import pygame
import speech_recognition as sr
from googletrans import Translator
from datetime import datetime
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import textwrap

# Download NLTK VADER lexicon if not available
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

# Initialize SentimentIntensityAnalyzer
sent_analyzer = SentimentIntensityAnalyzer()

# Indian Languages
indian_languages = {
    'hindi': 'hi', 'telugu': 'te', 'tamil': 'ta', 'kannada': 'kn',
    'bengali': 'bn', 'gujarati': 'gu', 'marathi': 'mr', 'punjabi': 'pa',
    'malayalam': 'ml', 'urdu': 'ur', 'assamese': 'as', 'oriya': 'or',
    'maithili': 'mai', 'sanskrit': 'sa', 'konkani': 'kok', 'sindhi': 'sd',
    'nepali': 'ne', 'bhili': 'bhi', 'santali': 'sat', 'kashmiri': 'ks',
    'dogri': 'doi', 'tulu': 'tcy', 'bodo': 'brx', 'kanauji': 'bjj',
    'english': 'en'
}

# Initialize pygame mixer
pygame.mixer.init()

# Create an empty DataFrame to store translations
conversation_df = pd.DataFrame(columns=['Timestamp', 'Source Language', 'Target Language', 'Input Text', 'Translated Text', 'English Translation', 'Sentiment'])

# Create a translator instance
translator = Translator()

# Function to capture speech input
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        print(f"You: {query}\n")
    except sr.UnknownValueError:
        print("Could not understand the audio. Please speak again.")
        return "None"
    except sr.RequestError:
        print("Speech Recognition service failed. Please try again.")
        return "None"
    return query

# Function to choose destination language
def destination_language():
    print("Please choose a target language from the following list:")
    print(", ".join(indian_languages.keys()))  # Show available languages
    to_lang = takecommand().lower()
    while to_lang not in indian_languages:
        print(f"Language '{to_lang}' not supported. Please choose from Indian languages.")
        print(", ".join(indian_languages.keys()))  # Show available languages again
        to_lang = takecommand().lower()
    return to_lang

# Function to print wrapped text
def print_wrapped(text, width=80):
    wrapped_text = textwrap.wrap(text, width=width)
    for line in wrapped_text:
        print(line)

while True:
    print("Speak...")

    # Capture user input
    query = takecommand()
    if query == "None":
        continue  # Retry if no input is recognized
    if query.lower() == "exit":
        print("Exiting the program.")
        break

    # Choose destination language
    to_lang = destination_language()

    # Detect the source language
    try:
        detected_language = translator.detect(query).lang
        print(f"Detected Source Language: {detected_language}")
    except Exception as e:
        print(f"Error detecting language: {e}")
        detected_language = 'en'  # Fallback to English

    # Translate the text to the target language
    try:
        translated_text = translator.translate(query, src=detected_language, dest=indian_languages[to_lang]).text
        print(f"\nTranslated Text ({to_lang}):")
        print_wrapped(translated_text)
        print()  # Add a newline for better readability
    except Exception as e:
        print(f"Error translating text to {to_lang}: {e}")
        translated_text = query  # Fallback to original text if translation fails

    # Translate to English if the target language is not English
    if to_lang.lower() != 'english':
        try:
            english_translation = translator.translate(translated_text, src=indian_languages[to_lang], dest='en').text
            print("English Translation:")
            print_wrapped(english_translation)
            print()  # Add a newline for better readability
        except Exception as e:
            print(f"Error translating text to English: {e}")
            english_translation = translated_text  # Fallback to target language translation if English translation fails
    else:
        english_translation = translated_text  # If target is English, no need for separate English translation

    # Sentiment Analysis
    try:
        sentiment_scores = sent_analyzer.polarity_scores(english_translation)
        compound_score = sentiment_scores['compound']
        print(f"Sentiment Score: {compound_score:.2f}")
        if compound_score >= 0.05:
            print("Sentiment: Positive")
        elif compound_score <= -0.05:
            print("Sentiment: Negative")
        else:
            print("Sentiment: Neutral")
    except Exception as e:
        print(f"Error performing sentiment analysis: {e}")
        compound_score = 0

    # Generate a timestamp for logging
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Store the translation in DataFrame
    conversation_df = conversation_df._append({
        'Timestamp': timestamp,
        'Source Language': detected_language,
        'Target Language': to_lang,
        'Input Text': query,
        'Translated Text': translated_text,
        'English Translation': english_translation,
        'Sentiment': compound_score
    }, ignore_index=True)

    # Output conversation history
    print("\nConversation History:")
    pd.set_option('display.max_colwidth', None)  # Show full content of each column
    print(conversation_df.to_string(index=False))
    print("\n" + "="*80 + "\n")  # Add a separator for better readability

    # Wait for audio to finish playing if any sound is played (optional)
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)