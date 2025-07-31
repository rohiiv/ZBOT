# from Frontend.GUI import (
#     GraphicalUserInterface,
#     SetAssistantStatus,
#     ShowTextToScreen,
#     TempDirectoryPath,
#     SetMicrophoneStatus,
#     AnswerModifier,
#     QueryModifier,
#     GetMicrophoneStatus,
#     GetAssistantStatus)
# from Backend.Model import FirstLayerDMM
# from Backend.RealtimeSearchEngine import RealtimeSearchEngine
# from Backend.Automation import Automation
# from Backend.SpeechToText import SpeechRecognition 
# from Backend.TextToSpeech import TextToSpeech
# from Backend.Chatbot import ChatBot
# from dotenv import dotenv_values
# from asyncio import run 
# from time import sleep 
# import subprocess 
# import threading
# import json 
# import os 
# import webbrowser

# env_vars = dotenv_values(r"ZBOT\Backend\key.env")
# Username = env_vars.get("Username")
# Assistantname =env_vars.get("Assistantname") 
# DefaultMessage = f'''{Username}: Hello {Assistantname},How are you?
# {Assistantname}: Welcome {Username}. I am doing well.How may I help you?'''
# subprocess =[]
# Functions = ["open","close","play","system","content","google search","youtbe search"]


# def ShowDefaultChatIfNoChats():
#     File = open(r'Data\ChatLog.json',"r", encoding ='utf-8')
#     chat_log_content= File.read()
#     print(f"Chatlog.json content:{chat_log_content}")
#     if len(File.read())<5:
#         with open(TempDirectoryPath('Database.data'),'w', encoding= 'utf-8') as file :
#             file.write("")
#             print ("database wa scleared due to insufficient storage issue")
            
#         with open(TempDirectoryPath('Responses.data'),'w', encoding= 'utf-8') as file :
#             file.write(DefaultMessage)

            
# def ReadChatLogJson():
#     with open(r'Data\ChatLog.json','r', encoding ='utf-8') as file:
#         chatlog_data = json.load(file)
#     return chatlog_data 

# def ChatLogIntegration():
#     json_data = ReadChatLogJson()
#     formatted_chatlog = ""
#     for entry in json_data :
#         if entry["role"] == "user":
#             formatted_chatlog += f"User:{entry['content']}\n"
#         elif entry["role"] == "assistant":
#             formatted_chatlog += f"Assistantname:{entry['content']}\n"
#     formatted_chatlog = formatted_chatlog.replace("User", Username + " ")
#     formatted_chatlog = formatted_chatlog.replace("Assistantname", Assistantname + " ")
    
#     with open(TempDirectoryPath('Database.data'),'w', encoding ='utf-8') as file :
#         file.write(AnswerModifier(formatted_chatlog))

# def ShowChatsOnGUI():
#     File= open(TempDirectoryPath('Database.data'),"r", encoding = 'utf-8')
#     Data = File.read()
#     if len(str(Data))>0:
#         lines = Data.split('\n')
#         result = '\n'.join(lines)
#         File.close() 
#         File = open(TempDirectoryPath('Responses.data'),"w", encoding = 'utf-8')
#         File.write(result)
#         File.close()
        
# def InitialExecution():
#     SetMicrophoneStatus("False")
#     ShowTextToScreen("")
#     ShowDefaultChatIfNoChats()
#     ChatLogIntegration()
#     ShowChatsOnGUI()
    
# InitialExecution()

# def MainExecution():
    
    
#     TaskExecution = False 
#     ImageExecution = False 
#     ImageGenerationQuery =""
    
#     SetAssistantStatus("Listening...")
#     Query = SpeechRecognition()
#     ShowTextToScreen(f"{Username}:{Query}")
#     SetAssistantStatus("Thinking...")
#     Decision = FirstLayerDMM(Query)
    
#     print("")
#     print(f"Decision: {Decision}")
#     print("")
    
#     G= any ([ i for i in Decision if i.startswith("general")])
#     R = any ([i for i in Decision if i.startswith("realtime")])
    
#     Mearged_query = " and". join (
#         [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")] 
#     )
    
#     for queries in Decision:
#         if "generate" in queries :
#             ImageGenerationQuery= str(queries)
#             ImageExecution=True
    
#     for queries in Decision:
#         if TaskExecution== False:
#             if any (queries.startswith(func) for func in Functions):
#                 run(Automation(list(Decision)))
#                 TaskExecution = True
    
#     if ImageExecution== True:
        
#         with open(r"Frontend\Files\ImageGeneration.data", "w") as file :
#             file.write(f"{ImageGenerationQuery}, True")
        
#         try:
#             p1 = subprocess.Popen(['python', r'Backend\ImageGeneration.py'],
#                                   stdout= subprocess.PIPE, stderr = subprocess.PIPE,
#                                   stdin= subprocess.PIPE, shell = False,
#                                   start_new_session=True
#                                   )
#             subprocess.append(p1)
            
#         except Exception as e:
#             print(f"Error starting ImageGeneration.py: {e}")
            
#     if G and R or R:
        
#                 SetAssistantStatus("Searching.....")
#                 Answer = RealtimeSearchEngine(QueryModifier(Mearged_query))
#                 ShowTextToScreen(f"{Assistantname}: {Answer}")
#                 SetAssistantStatus("Answering...")
#                 TextToSpeech(Answer)
#                 return True 
            
#     else:
#             for Queries in Decision:
                
#                 if "general" in Queries:
#                     SetAssistantStatus("Thinking.....")
#                     QueryFinal = Queries.replace("general ","")
#                     Answer = ChatBot(QueryModifier(QueryFinal))
#                     ShowTextToScreen(f"{Assistantname} : {Answer}")
#                     SetAssistantStatus("Answering.....")
#                     TextToSpeech(Answer)
#                     return True 
                
#                 elif "realtime" in Queries :
#                     SetAssistantStatus("SEARCHING.....")
#                     QueryFinal = Queries.replace("realtime ","")
#                     Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
#                     ShowTextToScreen(f"{Assistantname}: {Answer}")
#                     SetAssistantStatus("ANSWERING.....")
#                     TextToSpeech(Answer)
#                     return True
                
#                 elif "exit" in Queries :
#                     QueryFinal = "Okay, Bye !"
#                     Answer = ChatBot(QueryModifier(QueryFinal))
#                     ShowTextToScreen(f"{Assistantname}:{Answer}")
#                     SetAssistantStatus("ANSWERING...")
#                     TextToSpeech(Answer)
#                     SetAssistantStatus("ANSWERING....")
#                     os._exit(1)
                    

                    
# def FirstThread():
    
#     while True:
        
#         CurrentStatus = GetMicrophoneStatus()
        
#         if CurrentStatus == True:
#             MainExecution()
            
#         else:
#             AIStatus = GetAssistantStatus()
            
#             if"Available..." in AIStatus:
#                 sleep(0.1)
                
#             else:
#                 SetAssistantStatus("Available....")
    
# def SecondThread():
    
#     GraphicalUserInterface()
      
# if __name__ == "__main__":
#     thread2 = threading.Thread (target= FirstThread,daemon=True)
#     thread2.start()
#     SecondThread()

                    
            
        
            
            
            
#         #1.03.44
        
from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus
)
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition 
from Backend.TextToSpeech import TextToSpeech
from Backend.Chatbot import ChatBot
from dotenv import dotenv_values
from asyncio import run 
from time import sleep 
import subprocess 
import threading
import json 
import os 

# Load Environment Variables
env_vars = dotenv_values(r"ZBOT\Backend\key.env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname") 
DefaultMessage = f"""{Username}: Hello {Assistantname}, How are you?
{Assistantname}: Welcome {Username}. I am doing well. How may I help you?"""

subprocess_list = []  # Prevents conflict with the `subprocess` module
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

# ------------------------------ #
#        Chat Log Handling       #
# ------------------------------ #
def ShowDefaultChatIfNoChats():
    """Ensures chat log has default messages if empty."""
    try:
        with open(r'Data\ChatLog.json', "r", encoding='utf-8') as file:
            content = file.read()

        if len(content) < 5:
            with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
                file.write("")
            with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as file:
                file.write(DefaultMessage)
    except FileNotFoundError:
        print("ChatLog.json not found! Creating default logs.")
        with open(r'Data\ChatLog.json', "w", encoding='utf-8') as file:
            file.write("[]")

def ReadChatLogJson():
    """Reads and returns chat log data from JSON."""
    try:
        with open(r'Data\ChatLog.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def ChatLogIntegration():
    """Processes chat logs and stores formatted data."""
    json_data = ReadChatLogJson()
    formatted_chatlog = ""

    for entry in json_data:
        if entry.get("role") == "user":
            formatted_chatlog += f"User: {entry.get('content', '')}\n"
        elif entry.get("role") == "assistant":
            formatted_chatlog += f"Assistantname: {entry.get('content', '')}\n"

    formatted_chatlog = formatted_chatlog.replace("User", Username + " ")
    formatted_chatlog = formatted_chatlog.replace("Assistantname", Assistantname + " ")

    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI():
    """Displays chat logs in GUI."""
    try:
        with open(TempDirectoryPath('Database.data'), "r", encoding='utf-8') as file:
            data = file.read()

        if data.strip():
            with open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8') as file:
                file.write(data)
    except FileNotFoundError:
        print("Database.data not found! Skipping GUI update.")

# ------------------------------ #
#      Core Assistant Logic      #
# ------------------------------ #
def InitialExecution():
    """Prepares the system before execution."""
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()

InitialExecution()

def MainExecution():
    """Handles voice commands and chatbot logic."""
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""

    SetAssistantStatus("Listening...")
    Query = SpeechRecognition()
    ShowTextToScreen(f"{Username}: {Query}")
    SetAssistantStatus("Thinking...")

    Decision = FirstLayerDMM(Query)
    print(f"\nDecision: {Decision}\n")

    # Determine query type
    G = any(i.startswith("general") for i in Decision)
    R = any(i.startswith("realtime") for i in Decision)
    MergedQuery = " and ".join([" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")])

    # Check for image generation
    for queries in Decision:
        if "generate" in queries:
            ImageGenerationQuery = str(queries)
            ImageExecution = True

    # Perform automation tasks
    for queries in Decision:
        if not TaskExecution and any(queries.startswith(func) for func in Functions):
            run(Automation(list(Decision)))
            TaskExecution = True

    # Image Generation Handling
    if ImageExecution:
        with open(r"Frontend\Files\ImageGeneration.data", "w") as file:
            file.write(f"{ImageGenerationQuery}, True")

        try:
            p1 = subprocess.Popen(
                ['python', r'Backend\ImageGeneration.py'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                stdin=subprocess.PIPE, shell=False
            )
            subprocess_list.append(p1)
        except Exception as e:
            print(f"Error starting ImageGeneration.py: {e}")

    # Handle real-time or general queries
    if G and R or R:
        SetAssistantStatus("SEARCHING...")
        Answer = RealtimeSearchEngine(QueryModifier(MergedQuery))
        ShowTextToScreen(f"{Assistantname}: {Answer}")
        SetAssistantStatus("Answering...")
        TextToSpeech(Answer)
    else:
        for Queries in Decision:
            if "general" in Queries:
                SetAssistantStatus("THINKING...")
                Answer = ChatBot(QueryModifier(Queries.replace("general ", "")))
                SetAssistantStatus("ANSWERING...")
                TextToSpeech(Answer)
                return
            elif "realtime" in Queries:
                SetAssistantStatus("SEARCHING...")
                Answer = RealtimeSearchEngine(QueryModifier(MergedQuery))
                ShowTextToScreen(f"{Assistantname}: {Answer}")
                SetAssistantStatus("ANSWERING...")
                TextToSpeech(Answer)
                return
            elif "exit" in Queries:
                ShowTextToScreen(f"{Assistantname}: Okay, Bye!")
                SetAssistantStatus("ANSWERING...")
                TextToSpeech("Okay, Bye!")
                os._exit(1)

# ------------------------------ #
#      Multi-threading Logic     #
# ------------------------------ #
def FirstThread():
    """Handles voice detection loop."""
    while True:
        CurrentStatus = GetMicrophoneStatus()
        if CurrentStatus:
            MainExecution()
        else:
            AIStatus = GetAssistantStatus()
            if "Available..." not in AIStatus:
                SetAssistantStatus("Available...")

def SecondThread():
    """Handles GUI execution."""
    GraphicalUserInterface()

# Start Threads
if __name__ == "__main__":
    thread2 = threading.Thread(target=FirstThread, daemon=True)
    thread2.start()
    SecondThread()
