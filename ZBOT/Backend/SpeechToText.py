                       
                          
                          # // BLEH WALA CODE 
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# import os
# from dotenv import dotenv_values
# import mtranslate as mt

# # Load environment variables
# env_vars = dotenv_values(r"ZBOT\Backend\key.env")
# InputLanguage = env_vars.get("InputLanguage", "en")  # Default to English if not set

# # HTML Code
# HtmlCode = '''<!DOCTYPE html>
# <html lang="en">
# <head>
#     <title>Speech Recognition</title>
# </head>
# <body>
#     <button id="start" onclick="startRecognition()">Start Recognition</button>
#     <button id="end" onclick="stopRecognition()">Stop Recognition</button>
#     <p id="output"></p>
#     <script>
#         const output = document.getElementById('output');
#         let recognition;

#         function startRecognition() {
#             recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
#             recognition.lang = '';
#             recognition.continuous = true;

#             recognition.onresult = function(event) {
#                 const transcript = event.results[event.results.length - 1][0].transcript;
#                 output.textContent += transcript;
#             };

#             recognition.onend = function() {
#                 recognition.start();
#             };
#             recognition.start();
#         }

#         function stopRecognition() {
#             recognition.stop();
#             output.innerHTML = "";
#         }
#     </script>
# </body>
# </html>'''

# # Replace recognition.lang with the selected input language
# HtmlCode = HtmlCode.replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# # Save HTML file
# os.makedirs("Data", exist_ok=True)  # Ensure directory exists
# with open("Data/Voice.html", "w", encoding="utf-8") as f:
#     f.write(HtmlCode)

# # Get current working directory
# current_dir = os.getcwd()
# Link = f"file://{current_dir}/Data/Voice.html"

# # Configure Chrome options
# chrome_options = Options()
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--disable-software-rasterizer")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--disable-features=VizDisplayCompositor")

# # Start Selenium WebDriver
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service, options=chrome_options)

# # Speech Recognition Function
# def SpeechRecognition():
#     driver.get(Link)
#     driver.find_element(By.ID, "start").click()
    
#     while True:
#         try:
#             text = driver.find_element(By.ID, "output").text
#             if text:
#                 driver.find_element(By.ID, "end").click()
#                 return text.capitalize()
#         except Exception as e:
#             pass

# # Run Speech Recognition
# if __name__ == "__main__":
#     text = SpeechRecognition()
#     print(text)


#                                  #THE OG CODE OF THE HOUSE 
# from selenium import webdriver 
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from dotenv import dotenv_values
# import os
# import mtranslate as mt
# # PACKAGES TO BE INSTALLED 

# env_vars = dotenv_values(".env")# load env variablees 
# InputLanguage =env_vars.get("InputLanguage")#get the ip lang.
# HtmlCode = '''<!DOCTYPE html> 
# <html lang="en">
# <head>
#     <title>Speech Recognition</title>
# </head>
# <body>
#     <button id="start" onclick="startRecognition()">Start Recognition</button>
#     <button id="end" onclick="stopRecognition()">Stop Recognition</button>
#     <p id="output"></p>
#     <script>
#         const output = document.getElementById('output');
#         let recognition;

#         function startRecognition() {
#             recognition = new webkitSpeechRecognition() || new SpeechRecognition();
#             recognition.lang = '';
#             recognition.continuous = true;

#             recognition.onresult = function(event) {
#                 const transcript = event.results[event.results.length - 1][0].transcript;
#                 output.textContent += transcript;
#             };

#             recognition.onend = function() {
#                 recognition.start();
#             };
#             recognition.start();
#         }

#         function stopRecognition() {
#             recognition.stop();
#             output.innerHTML = "";
#         }
#     </script>
# </body>
# </html>'''
# # the line below replaces the language in the html code with our ip language
# HtmlCode = str(HtmlCode).replace("recognition.lang = ''; ", f"recognition.lang='{InputLanguage}';")
# with open(r"Data\Voice.html","w") as f : 
#     f.write(HtmlCode)
#     #get to current working directory 
# current_dir = os.getcwd()
# # file path for Html
# Link = f"{current_dir}/Data/Voice.html"  
# #set chrome options 
# chrome_options = Options()
# user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML,like Gecko)Chrome?89.0.142.86 Safari/537.36"
# chrome_options.add_argument(f"user-agent={user_agent}")
# chrome_options.add_argument("--user-fake-ui-for-media-stream")
# chrome_options.add_argument("--user-fake-device-for-media-stream")
# # chrome_options.add_argument("--headless=new")  
# service =Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service , options = chrome_options)
# TempDirPath = rf"{current_dir}/Frontend/Files"
# def SetAssistantStatus(Status):
#     with open(rf'{TempDirPath}/Status.data',"w",encoding='utf-8') as file :
#         file.write(Status)
        
# def QueryModifier (Query):
#     new_query =Query.lower().strip()
#     query_words = new_query.split()
#     question_words ={"how","what","where","who","when","why","which","whose","whom","can you","what's","where's","how's","can you"}
#     if any(word + " " in new_query for word in question_words):
#         if query_words[-1][-1] in ['.','?','!']:
#             new_query = new_query[:-1]+"?"
#         else:
#             new_query+="?"
#     else :
#         if query_words[-1][-1] in ['.','?','!']:
#             new_query = new_query[:-1]+"."
#         else:
#             new_query += "."
#     return new_query.capitalize()
    
# def UniversalTranslate(Text):
#     english_translation = mt.translate(Text,"en","auto")
#     return english_translation.capitalize()
# def SpeechRecognition():
#     driver.get("file:///"+Link)
#     driver.find_element (by=By.ID, value="start").click()
#     while True:
#         try:
#             Text = driver.find_element(by=By.ID, value ="output").text
#             if Text:
#                 driver.find_element(by=By.ID,value="end").click()
#                 if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
#                     return QueryModifier(Text)
#                 else:
#                     SetAssistantStatus("Translating...")
#                     return QueryModifier(UniversalTranslate(Text))
#         except Exception as e :
#             pass 
#         #main execution 
# if __name__ == "__main__":
#     while True:
#         Text= SpeechRecognition()
#         print (Text)
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# from selenium import webdriver 
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from dotenv import dotenv_values
# import os
# import mtranslate as mt

# env_vars = dotenv_values(".env")
# InputLanguage = env_vars.get("InputLanguage", "en")  # Default to English if missing

# # HTML Code for Speech Recognition
# HtmlCode = '''<!DOCTYPE html> 
# <html lang="en">
# <head>
#     <title>Speech Recognition</title>
# </head>
# <body>
#     <button id="start" onclick="startRecognition()">Start Recognition</button>
#     <button id="end" onclick="stopRecognition()">Stop Recognition</button>
#     <p id="output"></p>
#     <script>
#         const output = document.getElementById('output');
#         let recognition;

#         function startRecognition() {
#             recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
#             recognition.lang = '{InputLanguage}';
#             recognition.continuous = true;

#             recognition.onresult = function(event) {
#                 const transcript = event.results[event.results.length - 1][0].transcript;
#                 output.textContent += transcript;
#             };

#             recognition.onend = function() {
#                 recognition.start();
#             };
#             recognition.start();
#         }

#         function stopRecognition() {
#             recognition.stop();
#         }
#     </script>
# </body>
# </html>'''.replace("{InputLanguage}", InputLanguage)

# # Save HTML file
# os.makedirs("Data", exist_ok=True)
# html_path = os.path.abspath("Data/Voice.html")
# with open(html_path, "w", encoding="utf-8") as f:
#     f.write(HtmlCode)

# # Chrome Options
# chrome_options = Options()
# chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Auto grant mic access
# chrome_options.add_argument("--use-fake-device-for-media-stream")  # Simulate mic input
# chrome_options.add_argument("--allow-file-access-from-files")  # Allow local HTML
# chrome_options.add_argument("--disable-popup-blocking")  # Prevent pop-ups
# chrome_options.add_argument("--no-sandbox")  
# chrome_options.add_argument("--disable-infobars")  
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")  
# chrome_options.add_argument("--mute-audio")  # Mute unwanted audio
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_options.add_experimental_option("useAutomationExtension", False)


# chrome_options.add_argument("--incognito")  # ✅ Prevents caching issues
# chrome_options.add_argument("--start-maximized")  # ✅ Ensures proper rendering
# # # chrome_options.add_argument("--headless=new")  



# # service = Service(ChromeDriverManager().install())#############################
# # driver = webdriver.Chrome(service=service, options=chrome_options)

# # # # Open the correct file
# # driver.get(f"file:///{html_path.replace(os.sep, '/')}") ####################IF I ADD THIS TO THE CODE I GET TWO POP UPS FROM CHROME SO DO NOT ADD IT 





# # Set up WebDriver
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service, options=chrome_options)

# def SpeechRecognition():
    
#     driver.get("file:///" + html_path)
#     driver.find_element(By.ID, "start").click() 
    
#     while True:
#         try:
#             Text = driver.find_element(By.ID, "output").text
#             if Text:
#                 driver.find_element(By.ID, "end").click()
#                 return Text.strip().capitalize()
#         except Exception:
#             pass

# if __name__ == "__main__":
#     while True:
#         print("Listening...")
#         recognized_text = SpeechRecognition()
#         print(f"Recognized: {recognized_text}")
















from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import http.server
import socketserver
import threading

# Load environment variables
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en")  # Default to English if missing

# HTML Code for Speech Recognition
HtmlCode = '''<!DOCTYPE html> 
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = '{InputLanguage}';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
        }
    </script>
</body>
</html>'''.replace("{InputLanguage}", InputLanguage)

# Save HTML file in a local directory
os.makedirs("Data", exist_ok=True)
html_path = os.path.abspath("Data/Voice.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# Start an HTTP server to serve the file
PORT = 8000
def start_server():
    os.chdir("Data")  # Serve files from "Data" directory
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}/Voice.html")
        httpd.serve_forever()

threading.Thread(target=start_server, daemon=True).start()

# Chrome Options
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Auto grant mic access
chrome_options.add_argument("--use-fake-device-for-media-stream")  # Simulate mic input
chrome_options.add_argument("--disable-popup-blocking")  # Prevent pop-ups
chrome_options.add_argument("--no-sandbox")  
chrome_options.add_argument("--disable-infobars")  
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  
chrome_options.add_argument("--mute-audio")  # Mute unwanted audio
chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")  # Prevents unwanted pop-ups
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument("--start-maximized")  # ✅ Ensures proper rendering
chrome_options.add_argument("--headless=new")  # ✅ Runs Chrome in headless mode (remove if you need UI)

# Set up WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def SpeechRecognition():
    driver.get(f"http://localhost:{PORT}/Voice.html")
    driver.find_element(By.ID, "start").click() 
    
    while True:
        try:
            Text = driver.find_element(By.ID, "output").text
            if Text:
                driver.find_element(By.ID, "end").click()
                return Text.strip().capitalize()
        except Exception:
            pass

if __name__ == "__main__":
    while True:
        print("Listening...")
        recognized_text = SpeechRecognition()
        print(f"Recognized: {recognized_text}")
