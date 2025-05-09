from groq import Groq # to use Groq ka API
from json import load , dump # read and write json file 
import datetime 
from dotenv import dotenv_values # read env variables 
 
env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey") #go to env for apikeysssss
#initialize the Groq client using the provided APi Key
client = Groq(api_key =GroqAPIKey)
messages=[]



System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
***Talk frankly like a teenager***
***Do not use bad words ***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""
SystemChatBot= [
    {"role":"system","content":System}
    ]
try:
    with open(r"Data\ChatLog.json","r") as f:
        messages = load(f) #load existing messges from chatbot 
except FileNotFoundError:
    with open(r"Data\ChatLog.json","w") as f:
        dump([],f) #create a new json file if it does not exist
#TO GET REAL TIME DATA 
def RealtimeInformation():
    current_data_time = datetime.datetime.now()
    day = current_data_time.strftime("%A")
    date =current_data_time.strftime("%d")
    month = current_data_time.strftime("%B")
    year =current_data_time.strftime("%Y") 
    hour = current_data_time.strftime("%H")   
    minute = current_data_time.strftime("%M")
    second = current_data_time.strftime("%S")
    
    #formatting all of the values in a string 
    
    data = f"Please use this real-time info. if needed \n"
    data += f"Day: {day}\n Date:{date}\n Month:{month}\n Year:{year}\n"
    data+= f"Time :{hour} hpurs :{minute}minutes :{second}seconds.\n"
    return data 
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines =[line for line in lines if line.strip()]
    modified_answer ='\n'.join(non_empty_lines)
    return modified_answer
def ChatBot(Query):
    """This function sends the user's query to chatbot and returns the AI response."""
    try:
        with open(r"Data\Chatlog.json","r") as f :
            messages = load(f) #load existing messages from chatbot
        messages.append({"role": "user", "content": f"{Query}"})
        completion= client.chat.completions.create(
            model ="llama3-70b-8192", #AI MODEL USED     #    llama3-70b-8192
            messages=SystemChatBot+[{"role":"system","content":RealtimeInformation()}]+messages,
            max_tokens=512 , #2^10 NO. OF MAXIMUM TOKENS IN RESPONSE 
            temperature =0.7,
            top_p =1,
            stream =True,
            stop =None
        )
        
        Answer = ""
        stream =False #DOUBT
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        Answer = Answer.replace("</s>"," ")
        messages.append({"role":"assistant","content":Answer})
        with open(r"Data\ChatLog.json","w") as f:
            dump(messages,f,indent=4)
        return AnswerModifier(Answer=Answer)
    except Exception as e :
        print(f"Error:{e}")
        return "An error has occured "
        # with open(r"Data\ChatLog.json","w") as f : 
        #     dump([], f , indent =4)
        #     return ChatBot(Query)
if __name__ == "__main__":
    while True:
        user_input = input ("Enter your question:")
        print(ChatBot(user_input))
        
        #MAXIMUM TOKENS EXCEEDED ALREADY 
        #NEW MODEL LIKE DEEPSEK OR LLAMA3.3 
        # HAVE TO DELETE CHATLOG.JSON 