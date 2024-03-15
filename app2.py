import pyttsx3

def text_to_speech(text):
    # Initialize the text-to-speech engine
 

    # Convert the text to speech
    engine.say(text)

    # Wait for the speech to finish
    engine.runAndWait()

# Example usage
text = "Hello, how are you?"
text_to_speech(text)
