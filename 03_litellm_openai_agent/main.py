from litellm import completion
import os

# Set Gemini API key
os.environ["GEMINI_API_KEY"] = "AIzaSyCLe6Bq0fqOUI9WPjL5WRE95P8VFT6omPM"

def gemini():
    response = completion(
        model="gemini/gemini-1.5-flash",
        messages=[{"content": "Hello, how are you?", "role": "user"}]
    )
    print(response['choices'][0]['message']['content'])

def gemini2():
    response = completion(
        model="gemini/gemini-2.0-flash-exp",
        messages=[{"content": "Hello, how are you?", "role": "user"}]
    )
    print(response['choices'][0]['message']['content'])

# Call the function you want
gemini()
gemini2()
