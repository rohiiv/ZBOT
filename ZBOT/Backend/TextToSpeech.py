import pygame #handle autoplaayback
import random#generate random choices
import asyncio #for asynchronous operations
import edge_tts  #text to speech functionality 
import os #file path handling 
from dotenv import dotenv_values 

env_vars = dotenv_values(".env")
AssistantVoice= env_vars.get("AssistantVoice") # gegt an assistant voice 
#Asynchronous function to convert text to audio 
    
async def TextToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3" # path where the speech will be saved 
    
    if os.path.exists(file_path):
        os.remove(file_path) #delete the file if it exists
        
    communicate = edge_tts.Communicate(text,AssistantVoice,pitch='+5Hz',rate = '+13%')
    await communicate.save(r'Data\speech.mp3')
    
def TTS(Text, func = lambda r=None: True):
    while True:
        try:
            asyncio.run(TextToAudioFile(Text))
            pygame.mixer.init()#initialize pygame for playback 
            pygame.mixer.music.load(r"Data\speech.mp3") # load the generated speech file 
            pygame.mixer.music.play() #play the audio
            
            while pygame.mixer.music.get_busy():#this looop will run until the function stops 
                if func()== False:
                    break 
                pygame.time.Clock().tick(10) #limit loop to 10 ticks per second 
                
            return True
        except Exception as e:#handle ex ceptions
            print(f"Error in TTS:{e}")
        finally:
            try:
                func(False)
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            except Exception as e:#handle exception during cleanup 
                print(f"Error in finally block:{e}")
                
def TextToSpeech(Text,func=lambda r=None: True):
    Data = str(Text).split(".") #split the lines by full stops
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out Disha.",
        "The rest of the text is now on the chat screen, Disha, please check it.",
        "You can see the rest of the text on the chat screen, Disha.",
        "The remaining part of the text is now on the chat screen, Disha.",
        "Disha, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, Disha.",
        "Disha, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, Disha.",
        "The next part of the text is on the chat screen, Disha.",
        "Disha, please check the chat screen for more information.",
        "There's more text on the chat screen for you, Disha.",
        "Disha, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, Disha.",
        "Disha, check the chat screen for the rest of the text.",
        "Disha chat screen has the rest of the text, Disha.",
        "There's more to see on the chat screen, Disha, please look.",
        "Disha, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out Disha.",
        "Please review the chat screen for the rest of the text, Disha.",
        "Disha , look at the chat screen for the complete answer."
    ]
    
    #if the text is longer than 4 line or 250 chr add a response message 
    if len(Data)>4 and len(Text)>=250:
        TTS(" ".join(Text.split(".")[0:2])+ "."+ random.choice(responses),func)
        
        # else play the whole text 
    else:
        TTS(Text,func)
if __name__=="__main__":
    while True:
        TextToSpeech(input("Enter text: "))