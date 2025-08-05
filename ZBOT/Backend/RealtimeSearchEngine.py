from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
# We are not using dotenv for this test
import os

# --- TEMPORARY TEST: HARDCODE THE API KEY ---
# Replace the placeholder with your actual Groq API key
GroqAPIKey = "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"
Username = "Rohini"  # Or your name
Assistantname = "ZBOT" # Or your bot's name
# --- END OF TEST ---

# Debug print to confirm the key is set
print(f"Using hardcoded Groq API Key: {GroqAPIKey}")

# INITIALIZE THE CLIENT WITH THE HARDCODED KEY
# This is the line that was failing. Let's see if it works now.
client = Groq(api_key=GroqAPIKey)
# -----------------------------------------------------

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***
***Make the answers easy to understand*** """

try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

def GoogleSearch(query):
    results = list(search(query, num=5, stop=5, pause=2))
    Answer = f"The search results for '{query}' are:\n[start]\n"
    for url in results:
        Answer += f"{url}\n"
    Answer += "[end]"
    return Answer

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Heloo, how can i help u disha ?"},
]

def Information():
    data = " "
    current_data_time = datetime.datetime.now()
    day = current_data_time.strftime("%A")
    date = current_data_time.strftime("%d")
    month = current_data_time.strftime("%B")
    year = current_data_time.strftime("%Y")
    hour = current_data_time.strftime("%H")
    minute = current_data_time.strftime("%M")
    second = current_data_time.strftime("%S")
    data += f"Use This Real-Time Informaton if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Hour: {hour} hours, {minute} minutes, {second} seconds \n"
    return data

def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
    messages.append({"role": "user", "content": GoogleSearch(prompt)})
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None
    )
    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content
    Answer = Answer.strip().replace("</s", "")
    messages.append({"role": "assistant", "content": Answer})
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)
    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)

if __name__ == "__main__":
    print("\n--- Initialization Complete. The program should not crash if the API key is valid. ---\n")
    while True:
        prompt = input("Enter your query: ")
        if prompt.lower() in ['exit', 'quit']:
            break
        print(RealtimeSearchEngine(prompt))

