# from AppOpener import close , open as appopen #to open and close app 
# from webbrowser import open as webopen 
# from pywhatkit import search, playonyt #yt and google 
# from dotenv import dotenv_values 
# from bs4 import BeautifulSoup #for parsing html content 
# from rich import print  #for styled consoled op
# from groq import Groq #for Ai chat functionalities 
# import webbrowser 
# import os
# import requests # for making https requests 
# import keyboard
# import subprocess 
# import asyncio # fir asynchronus functionalities

# env_vars = dotenv_values(".env") 
# GroqAPIKey = env_vars.get("GroqAPIKey")

# #define CSS class for parsing specific ele.

# classes =["zCubwf","hgKElc","LTKOO sY7ric","Z0LcW","grst vk_bk FzvWSb YwPhnf","pclqee",
#           "tw-Data-text tw-text-small tw-ta",
#           "IZ6rdc","O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe",  
#           "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]
# useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# #initialize with Groq key 
# client = Groq (api_key=GroqAPIKey)

# #predefined responses 
# professional_responses =[
#     "Your satisfaction is my top priority ; feel free to reach out if there is anything else i can help with disha .",
#     "i'm at your service, anything else you need help with."
#     "you do not thank me, i am your BOT, that is my duty, why else would you create me ? if there isanything go on."
#     ]

# #list to store bot messages 
# messages = []
# #System message to provide context to chatbot 
# SystemChatBot=[{"role":"system" ,"content":f"Hello, I am{os.environ['Username']}You're a content writer.You have to write content like letter "}]
# #function to perform like google search 

# def GoogleSearch(Topic):
#     search(Topic)
#     return True 

# def Content (Topic):
#     def OpenNotepad(File):
#         default_text_editor = 'notepad.exe'
#         subprocess.Popen([default_text_editor,File])
        
#     def ContentWriterAI(prompt):
#         messages.append({"role":"user","content": f"{prompt}"})
#         completion = client.chat.completions.create(
#             model ="mixtral-8x7b-32768", #Ai model to be used 
#             messages = SystemChatBot+messages,
#             max_tokens= 2048,
#             temperature=0.7,
#             top_p=1, 
#             stream =True,
#             stop =None
#         )
#         Answer =""     #initialize string for response 
#         for chunk in completion :
#             if chunk.choices[0].delta.content:
#                 Answer += chunk.choices[0].delta.content 
#         Answer =Answer.replace("</s>","")  
#         messages.append({"role":"assistant", "content":Answer})
#         return Answer
#     Topic : str = Topic.replace("Content","")
#     ContentByAI = ContentWriterAI(Topic)
    
#     #save the generated content in the form of a text file 
#     with open(rf"Data\{Topic.lower().replace(' ','')}.txt", "w", encoding ="utf-8") as file:
#         file.write(ContentByAI)
#         file.close()
#     OpenNotepad(rf"Data\{Topic.lower().replace(' ', '')}.txt")
#     return True

# def YouTubeSearch(Topic):
#     Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
#     webbrowser.open(Url4Search)
#     return True
# # YouTubeSearch("hum dil de chuke sanam ")     TEST EXAMPLE 
# def PlayYouTube (query):
#     playonyt(query)
#     return True 
# def OpenApp(app, sess =requests.session()):
#     try:
#         appopen(app,match_closest=True,output=True,throw_error=True)
#         return True
#     except:
# def extract_links(html):
#     if html is None:
#         return []
#     soup = BeautifulSoup(html, 'html.parser')
#     links = soup.find_all('a')  # Updated to find all anchor tags
#     valid_links = [link.get('href') for link in links if link.get('href') is not None]  # Ensure href is not None
#     return valid_links

        
#         def search_google(query):
#             url= f"https://www.google.com/search?q={query}"
#             headers ={"User-Agent": useragent}
#             response = sess.get(url, headers=headers)
            
#             if response.status_code==200:
#                 return response.text
#             else:
#                 print("Failed to retrive search results , i am so sorry")
#             return None 
        
#         html= search_google(app) 
        
#         if html:
#         #     link = extract_links(html)[0]
#         #     webopen(link)
#         # return True
#             link = extract_links(html)
#             if link:
#                 webbrowser.open(link[0])
#                 return True
#             else:
#                 print("No valid links found.")
    
#     return False
# # OpenApp("spotify")  TEST EXAMPLE

# def CloseApp(app):
#         if "chrome" in app:
#             pass
#         else :
#             try:
#                 close (app,match_closest=True,output=True,throw_error=True)
#                 return True
#             except:
#                 return False
# # CloseApp("settings")     TEST SAMPLE 
# def System(command ):
#         def mute():
#             keyboard.press_and_release("volume mute ")
#         def unmute():
#             keyboard.press_and_release("volume mute ")
#         def volume_up():
#             keyboard.press_and_release("volume up ")
#         def volume_down():
#             keyboard.press_and_release("volume down ")
#         if command == "mute":
#             mute()
#         elif command == "unmute":
#             unmute()
#         elif command == "volume_up":
#             volume_up()
#         elif command == "volume_down":
#             volume_down()
#         return True
# async def TranslateAndExecute(commands:list[str]):
#     funcs=[]
#     for command in commands:
#         command = command.strip()  # Remove leading/trailing spaces
#         if command.startswith("open"):
#             # if "open it " in command :
#             #     pass 
#             # if "open file" == command:
#             #     pass
#             # else:
#                 fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
#                 funcs.append(fun)
#         elif command.startswith("general "):
#             pass 
#         elif command.startswith("realtime "):
#             pass
#         elif command.startswith("close"):
#             fun = asyncio.to_thread(CloseApp,command.removeprefix("close "))
#             funcs.append(fun)
#         elif command.startswith("play "):
#             fun = asyncio.to_thread(PlayYouTube,command.removeprefix("play "))
#             funcs.append(fun)
#         elif command.startswith("content "):
#             fun = asyncio.to_thread(Content,command.removeprefix("content "))
#             funcs.append(fun)
#         elif command.startswith("google search "):
#             fun = asyncio.to_thread(GoogleSearch,command.removeprefix("google search "))
#             funcs.append(fun)
#         elif command.startswith("youtube search "):
#             fun = asyncio.to_thread(System,command.removeprefix("youtube search "))
#             funcs.append(fun)
#         elif command.startswith("system "):
#             fun = asyncio.to_thread(System,command.removeprefix("system "))
#             funcs.append(fun)
#         else:
#             print(f"No function found for {command}")
#     results = await asyncio.gather(*funcs)
    
#     for result in results:
#         if isinstance(result,str):
#             yield result
#         else:
#             yield result
# async def Automation (commands: list[str]):
#     async for result in TranslateAndExecute(commands):
#         pass 
#     return True 
# if __name__ =="__main__":
#     asyncio.run(Automation([ " play ekshanam swayamvaram ","open files explorer"]))
    
    
#     # THE PROBLEM IS THIS CODE IS NOT ABLE TO OPEN YOUTUBE OR ANY OTHER APP THAT REQUIRES EXTRACT LINK FUNC. IT JUST SHOWS NO VALID LINK FOUND






from AppOpener import close, open as appopen  # to open and close apps
from webbrowser import open as webopen
from pywhatkit import search, playonyt  # Google & YouTube search
from dotenv import dotenv_values
from bs4 import BeautifulSoup  # For parsing HTML content
from rich import print  # Styled console output
from groq import Groq  # AI chat functionalities
import webbrowser
import os
import requests  # For making HTTP requests
import keyboard
import subprocess
import asyncio  # For async functions

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Define CSS classes for parsing specific elements.
classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "grst vk_bk FzvWSb YwPhnf",
           "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "O5uR6d LTKOO", 
           "vlzY6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", 
           "sXLaOe", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize AI client
client = Groq(api_key=GroqAPIKey)

# System message for chatbot
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}. You're a content writer."}]

# Google search function
def GoogleSearch(Topic):
    search(Topic)
    return True

# YouTube search function
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic.replace(' ', '+')}"
    webbrowser.open(Url4Search)
    return True

# Play video on YouTube
def PlayYouTube(query):
    playonyt(query)
    return True

# Extract valid links from search results
def extract_links(html):
    if html is None:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', href=True)

    valid_links = [link['href'] for link in links if link['href'].startswith('/url?q=')]
    valid_links = [link.split('/url?q=')[1].split('&')[0] for link in valid_links]

    return valid_links

# Function to open applications
def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        print(f"Trying Google search for {app}...")
        
        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": useragent}
            response = sess.get(url, headers=headers)

            if response.status_code == 200:
                return response.text
            else:
                print("Failed to retrieve search results.")
                return None

        html = search_google(app)
        if html:
            links = extract_links(html)
            if links:
                webbrowser.open(links[0])
                return True
            else:
                print("No valid links found.")
                return False

    return False

# Function to close apps
def CloseApp(app):
    if "chrome" in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False

# System volume controls
def System(command):
    if command == "mute":
        keyboard.press_and_release("volume mute")
    elif command == "unmute":
        keyboard.press_and_release("volume mute")
    elif command == "volume_up":
        keyboard.press_and_release("volume up")
    elif command == "volume_down":
        keyboard.press_and_release("volume down")
    return True

# Async function to execute commands
async def TranslateAndExecute(commands: list[str]):
    funcs = []
    for command in commands:
        command = command.strip()

        if command.startswith("open "):
            fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
            funcs.append(fun)
        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)
        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYouTube, command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)
        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)
        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)
        else:
            print(f"No function found for {command}")

    results = await asyncio.gather(*funcs)
    
    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True

# Run script
if __name__ == "__main__":
    asyncio.run(Automation(["open file explorer", "play tmkoc"]))
