
    
    
    
#REGULAR CODE  
import asyncio 
from random import randint 
from PIL import Image 
import requests 
from dotenv import get_key
import os
from time import sleep 


#open and dispaly the image 
def open_images (prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ","_")
    
    #generate filenames for the image 
    Files = [f"{prompt}{i}.jpg" for i in range(1,5) ]
    
    for jpg_file in Files :
        image_path = os.path.join(folder_path, jpg_file )
        
        try:
            img = Image.open(image_path)
            print (f"Opening image:{image_path}")
            img.show()
            sleep(1) #pause for 2 second before showing the next image 
        
        except IOError:
            print(f"Error opening image: {image_path}")
            
API_URL= "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers ={"Authorization": f"Bearer {get_key('.env','HuggingFaceAPIKey')}"}
async def query(payload):
    response= await asyncio.to_thread(requests.post,API_URL,headers=headers,json=payload)
    return response.content

async def generate_images(prompt: str):
    tasks=[]
    
    for _ in range (4):
        payload = {
            "inputs":f"{prompt}, quality=4K, sharpness = maximum, Ultra High details, high resolution, seed ={randint(0,1000000)}",
            
        }        
        task = asyncio.create_task(query(payload))  
        tasks.append(task)  
        
        #WAIT FOR ALL TASKS TO COMPLETE 
    image_bytes_list= await asyncio.gather(*tasks)
    
    #save the generated iamge as a file 
    for i, image_bytes in enumerate(image_bytes_list):
        with open(fr"Data\{prompt.replace(' ','_')}{i + 1}.jpg","wb") as f :
            f.write(image_bytes)
            
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)
    
while True :
    try:
        with open(r"Frontend\Files\ImageGeneration.data","r") as f:
            Data: str= f.read()
            
        Prompt, Status = Data.split(",")
        
        if Status== "True":
            print("generating image....")
            ImageStatus = GenerateImages(prompt=Prompt)
            
            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")
                break 
        else:
            sleep(1)
            
    except:
        pass







# # CHATGPT
# import asyncio
# import os
# from random import randint
# from PIL import Image
# import requests
# from dotenv import get_key
# from time import sleep

# # Function to open and display images
# def open_images(prompt):
#     folder_path = "Data"
#     prompt = prompt.replace(" ", "_")

#     # Generate filenames for the images
#     files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

#     for jpg_file in files:
#         image_path = os.path.join(folder_path, jpg_file)

#         try:
#             img = Image.open(image_path)
#             print(f"Opening image: {image_path}")
#             img.show()
#             sleep(2)  # Pause before showing the next image

#         except IOError:
#             print(f"Error opening image: {image_path}")

# # Hugging Face API setup
# API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
# headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

# # Function to send image generation request
# async def query(payload):
#     try:
#         response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
#         return response.content
#     except Exception as e:
#         print(f"API Request Failed: {e}")
#         return None

# # Function to generate images asynchronously
# async def generate_images(prompt: str):
#     tasks = []

#     for _ in range(4):
#         payload = {
#             "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed={randint(0,1000000)}",
#         }

#         task = asyncio.create_task(query(payload))
#         tasks.append(task)

#     # Wait for all tasks to complete
#     image_bytes_list = await asyncio.gather(*tasks)

#     # Save generated images as files
#     for i, image_bytes in enumerate(image_bytes_list):
#         if image_bytes:
#             with open(os.path.join("Data", f"{prompt.replace(' ', '_')}{i+1}.jpg"), "wb") as f:
#                 f.write(image_bytes)

# # Wrapper function to run async functions
# def GenerateImages(prompt: str):
#     asyncio.run(generate_images(prompt))
#     open_images(prompt)

# # Main loop to check and process image generation requests
# while True:
#     try:
#         with open(os.path.join("Frontend", "Files", "ImageGeneration.data"), "r") as f:
#             data = f.read().strip()

#         values = data.split(",")
#         if len(values) >= 2:
#             Prompt, Status = values[:2]  # Take only the first two values
#         else:
#             print("Invalid data format in ImageGeneration.data")
#             exit()

#         if Status == "True":
#             print("Generating image...")
#             GenerateImages(prompt=Prompt)

#             # Update file to mark completion
#             with open(os.path.join("Frontend", "Files", "ImageGeneration.data"), "w") as f:
#                 f.write("False,False")
#             break
#         else:
#             sleep(1)

#     except Exception as e:
#         print(f"Unsuccessful: {e}")





# import asyncio
# import os
# import requests
# from random import randint
# from PIL import Image
# from time import sleep
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()
# HUGGINGFACE_API_KEY = os.getenv("HuggingFaceAPIKey")

# # API URL
# API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0" #https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0
# HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

# # Ensure Data folder exists
# DATA_FOLDER = "Data"
# os.makedirs(DATA_FOLDER, exist_ok=True)

# # Open and display generated images
# def open_images(prompt):
#     prompt = prompt.replace(" ", "_")
#     files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

#     for jpg_file in files:
#         image_path = os.path.join(DATA_FOLDER, jpg_file)
#         try:
#             img = Image.open(image_path)
#             print(f"Opening image: {image_path}")
#             img.show()
#             sleep(1)  # Pause before showing the next image
#         except IOError:
#             print(f"Error opening image: {image_path}")

# # Function to query Hugging Face API
# async def query(payload):
#     response = await asyncio.to_thread(requests.post, API_URL, headers=HEADERS, json=payload)

#     if response.status_code != 200:
#         print(f"API Error {response.status_code}: {response.text}")
#         return None
#     return response.content

# # Function to generate images
# async def generate_images(prompt):
#     tasks = []
    
#     for _ in range(4):
#         payload = {
#             "inputs": f"{prompt}, 4K quality, ultra high detail, high resolution, seed={randint(0, 1000000)}"
#         }
#         tasks.append(asyncio.create_task(query(payload)))

#     image_bytes_list = await asyncio.gather(*tasks)

#     for i, image_bytes in enumerate(image_bytes_list):
#         if image_bytes:
#             image_path = os.path.join(DATA_FOLDER, f"{prompt.replace(' ', '_')}{i + 1}.jpg")
#             with open(image_path, "wb") as f:
#                 f.write(image_bytes)
#             print(f"Image saved: {image_path}")
#         else:
#             print(f"Failed to generate image {i + 1}")

# # Wrapper function to run the asyncio loop
# def GenerateImages(prompt):
#     asyncio.run(generate_images(prompt))
#     open_images(prompt)

# # Main loop to check for image requests
# while True:
#     try:
#         file_path = r"Frontend\Files\ImageGeneration.data"

#         # Check if file exists before reading
#         if not os.path.exists(file_path):
#             print(f"File {file_path} not found. Waiting...")
#             sleep(1)
#             continue

#         with open(file_path, "r") as f:
#             data = f.read().strip()

#         if not data:
#             sleep(1)
#             continue

#         prompt, status = data.split(",")

#         if status == "True":
#             print("Generating image...")
#             GenerateImages(prompt)

#             with open(file_path, "w") as f:
#                 f.write("False,False")
#             break
#         else:
#             sleep(1)

#     except Exception as e:
#         print(f"Error: {e}")




