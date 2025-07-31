import asyncio
import os
import requests
from random import randint
from PIL import Image
from time import sleep
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
DATA_FOLDER = "Data"
FRONTEND_FILE = os.path.join("Frontend", "Files", "ImageGeneration.data")

# Ensure Data folder exists
os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(FRONTEND_FILE), exist_ok=True)

def get_api_key():
    """Get API key from environment variables"""
    api_key = os.getenv("HuggingFaceAPIKey")
    if not api_key:
        raise ValueError("HuggingFaceAPIKey not found in environment variables")
    return api_key

def open_images(prompt):
    """Open and display generated images"""
    prompt_safe = prompt.replace(" ", "_")
    files = [f"{prompt_safe}{i}.jpg" for i in range(1, 5)]
    
    images_opened = 0
    for jpg_file in files:
        image_path = os.path.join(DATA_FOLDER, jpg_file)
        try:
            if os.path.exists(image_path):
                img = Image.open(image_path)
                print(f"Opening image: {image_path}")
                img.show()
                images_opened += 1
                sleep(2)  # Pause before showing next image
            else:
                print(f"Image not found: {image_path}")
        except IOError as e:
            print(f"Error opening image {image_path}: {e}")
    
    print(f"Successfully opened {images_opened} out of 4 images")

async def query_api(payload, session, semaphore):
    """Query the Hugging Face API with rate limiting"""
    async with semaphore:  # Limit concurrent requests help prevent overwhelming the API
        try:
            headers = {"Authorization": f"Bearer {get_api_key()}"}
            
            # Convert requests.post to async
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: requests.post(API_URL, headers=headers, json=payload, timeout=60)
            )
            
            if response.status_code == 200:
                return response.content
            elif response.status_code == 503:
                print("Model is loading, waiting...")
                await asyncio.sleep(20)  # Wait for model to load
                # Retry once
                response = await loop.run_in_executor(
                    None, 
                    lambda: requests.post(API_URL, headers=headers, json=payload, timeout=60)
                )
                if response.status_code == 200:
                    return response.content
            
            print(f"API Error {response.status_code}: {response.text}")
            return None
            
        except requests.exceptions.Timeout:
            print("Request timed out")
            return None
        except Exception as e:
            print(f"API request failed: {e}")
            return None

async def generate_images(prompt):
    """Generate images asynchronously"""
    print(f"Starting image generation for prompt: '{prompt}'")
    
    # Create semaphore to limit concurrent requests (avoid rate limiting)
    semaphore = asyncio.Semaphore(2)  # Max 2 concurrent requests
    
    tasks = []
    session = None  # Not using aiohttp, but keeping for future upgrade
    
    for i in range(4):
        payload = {
            "inputs": f"{prompt}, 4K quality, ultra high detail, high resolution, masterpiece",
            "parameters": {
                "seed": randint(0, 1000000),
                "num_inference_steps": 25,
                "guidance_scale": 7.5
            }
        }
        
        task = asyncio.create_task(query_api(payload, session, semaphore))
        tasks.append(task)
        
        # Small delay between task creation to avoid overwhelming the API
        await asyncio.sleep(0.1)
    
    print("Waiting for all images to generate...")
    image_bytes_list = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Save generated images
    successful_saves = 0
    prompt_safe = prompt.replace(' ', '_')
    
    for i, image_bytes in enumerate(image_bytes_list):
        if isinstance(image_bytes, Exception):
            print(f"Task {i+1} failed with exception: {image_bytes}")
            continue
            
        if image_bytes:
            image_path = os.path.join(DATA_FOLDER, f"{prompt_safe}{i + 1}.jpg")
            try:
                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                print(f"Image {i+1} saved: {image_path}")
                successful_saves += 1
            except Exception as e:
                print(f"Failed to save image {i+1}: {e}")
        else:
            print(f"No data received for image {i+1}")
    
    print(f"Successfully generated and saved {successful_saves} out of 4 images")
    return successful_saves > 0

def GenerateImages(prompt):
    """Wrapper function to run async image generation"""
    try:
        success = asyncio.run(generate_images(prompt))
        if success:
            open_images(prompt)
        else:
            print("No images were generated successfully")
    except Exception as e:
        print(f"Error in GenerateImages: {e}")

def read_generation_request():
    """Read and parse the image generation request file"""
    try:
        if not os.path.exists(FRONTEND_FILE):
            return None, None
            
        with open(FRONTEND_FILE, "r") as f:
            data = f.read().strip()
        
        if not data:
            return None, None
            
        parts = data.split(",")
        if len(parts) >= 2:
            return parts[0].strip(), parts[1].strip()
        else:
            print(f"Invalid data format in {FRONTEND_FILE}: {data}")
            return None, None
            
    except Exception as e:
        print(f"Error reading request file: {e}")
        return None, None

def write_generation_status(status="False,False"):
    """Write status back to the request file"""
    try:
        with open(FRONTEND_FILE, "w") as f:
            f.write(status)
    except Exception as e:
        print(f"Error writing status file: {e}")

def main():
    """Main loop to check and process image generation requests"""
    print("Image generation service started. Waiting for requests...")
    
    while True:
        try:
            prompt, status = read_generation_request()
            
            if prompt and status == "True":
                print(f"New request received: '{prompt}'")
                print("Generating images...")
                
                GenerateImages(prompt)
                
                # Mark as completed
                write_generation_status("False,False")
                print("Request completed. Waiting for next request...")
                
            sleep(1)  # Check every second
            
        except KeyboardInterrupt:
            print("\nService stopped by user")
            break
        except Exception as e:
            print(f"Unexpected error in main loop: {e}")
            sleep(5)  # Wait longer on unexpected errors

if __name__ == "__main__":
    try:
        # Test API key availability
        get_api_key()
        main()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please make sure your .env file contains HuggingFaceAPIKey")
    except Exception as e:
        print(f"Fatal error: {e}")
    
    
    
# #REGULAR CODE  
# import asyncio 
# from random import randint 
# from PIL import Image 
# import requests 
# from dotenv import get_key
# import os
# from time import sleep 


# #open and dispaly the image 
# def open_images (prompt):
#     folder_path = r"Data"
#     prompt = prompt.replace(" ","_")
    
#     #generate filenames for the image 
#     Files = [f"{prompt}{i}.jpg" for i in range(1,5) ]
    
#     for jpg_file in Files :
#         image_path = os.path.join(folder_path, jpg_file )
        
#         try:
#             img = Image.open(image_path)
#             print (f"Opening image:{image_path}")
#             img.show()
#             sleep(1) #pause for 2 second before showing the next image 
        
#         except IOError:
#             print(f"Error opening image: {image_path}")
            
# API_URL= "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
# headers ={"Authorization": f"Bearer {get_key('.env','HuggingFaceAPIKey')}"}
# async def query(payload):
#     response= await asyncio.to_thread(requests.post,API_URL,headers=headers,json=payload)
#     return response.content

# async def generate_images(prompt: str):
#     tasks=[]
    
#     for _ in range (4):
#         payload = {
#             "inputs":f"{prompt}, quality=4K, sharpness = maximum, Ultra High details, high resolution, seed ={randint(0,1000000)}",
            
#         }        
#         task = asyncio.create_task(query(payload))  
#         tasks.append(task)  
        
#         #WAIT FOR ALL TASKS TO COMPLETE 
#     image_bytes_list= await asyncio.gather(*tasks)
    
#     #save the generated iamge as a file 
#     for i, image_bytes in enumerate(image_bytes_list):
#         with open(fr"Data\{prompt.replace(' ','_')}{i + 1}.jpg","wb") as f :
#             f.write(image_bytes)
            
# def GenerateImages(prompt: str):
#     asyncio.run(generate_images(prompt))
#     open_images(prompt)
    
# while True :
#     try:
#         with open(r"Frontend\Files\ImageGeneration.data","r") as f:
#             Data: str= f.read()
            
#         Prompt, Status = Data.split(",")
        
#         if Status== "True":
#             print("generating image....")
#             ImageStatus = GenerateImages(prompt=Prompt)
            
#             with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
#                 f.write("False,False")
#                 break 
#         else:
#             sleep(1)
            
#     except:
#         pass







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




