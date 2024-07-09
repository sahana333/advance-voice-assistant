import speech_recognition as sr
import pyttsx3
import nltk
from nltk import pos_tag, ne_chunk
from nltk.tokenize import word_tokenize
from twilio.rest import Client
import spacy
from textblob import TextBlob
import wikipediaapi

# Specify a valid user-agent string for Wikipedia API
wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent="YourApplicationName/1.0 (sahanaganesh501@gmail.com)"
)

# Download NLTK data if not already downloaded
nltk.download('punkt')

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Twilio credentials
TWILIO_ACCOUNT_SID = "AC7264a2292f3a9e16c3439ac8ea955cce"
TWILIO_AUTH_TOKEN = "6bbd0fa6f4939dab81e98d9f8f0f2047"
TWILIO_PHONE_NUMBER = "+13348358396"
TO_PHONE_NUMBER = "+91 8939783181"

# Twilio client initialization
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Initialize spaCy for NLP tasks
nlp = spacy.load("en_core_web_sm")

# Function to perform basic natural language processing
def nlp_processing(query):
    doc = nlp(query)
    response = ""

    # Named Entity Recognition (NER)
    for ent in doc.ents:
        response += f"Entity: {ent.text}, Type: {ent.label_}\n"

    # Sentiment analysis
    sentiment = analyze_sentiment(query)
    response += f"Sentiment: {sentiment}\n"

    # Query Wikipedia for information
    wiki_response = get_wikipedia_summary(query)
    response += f"Wikipedia Summary:\n{wiki_response}"

    return response

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0:
        return "Positive"
    elif sentiment_score < 0:
        return "Negative"
    else:
        return "Neutral"

def get_wikipedia_summary(topic):
    page = wiki.page(topic)
    if page.exists():
        return page.summary[:300]  # Limit summary length to 300 characters
    else:
        return f"Sorry, I couldn't find information about {topic} on Wikipedia."

# Function to listen and recognize speech
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio)
        print(f"You said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        return None

# Function to respond to the user
def respond(query):
    if 'exit' in query.lower():
        print("Exiting the program.")
        engine.say("Goodbye!")
        engine.runAndWait()
        exit()
    elif 'text' in query.lower():
        send_text_message()
    else:
        response = nlp_processing(query)
        engine.say(response)
        engine.runAndWait()
        return response

# Function to send a text message using Twilio
def send_text_message():
    try:
        # Replace with your desired message
        message_body = "Hello, this is a test message from your voice assistant!"

        twilio_client.messages.create(
            to=TO_PHONE_NUMBER,
            from_=TWILIO_PHONE_NUMBER,
            body=message_body
        )

        print("Text message sent successfully.")
        engine.say("Text message sent successfully.")
        engine.runAndWait()
    except Exception as e:
        print(f"Error sending text message: {str(e)}")
        engine.say("Sorry, there was an error sending the text message.")
        engine.runAndWait()

# Main loop
while True:
    query = listen()
    if query:
        respond(query.lower())

