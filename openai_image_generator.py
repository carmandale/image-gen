import os
import io
import json
import base64
from dotenv import load_dotenv
from tkinter import Tk
from tkinter import filedialog
from PIL import Image, ImageTk
import requests

"""
OpenAI DALL-E Image Generator

This script allows you to generate images using OpenAI's DALL-E models (DALL-E 2 and DALL-E 3)
through a simple command-line interface. It supports various image sizes and multiple image generation.

The generated images are saved to a local directory. An OpenAI API key is required.
"""

def generate_image(prompt, model="dall-e-3", size="1024x1024", quality="standard", n=1):
    """
    Generate images using OpenAI's DALL-E API.
    
    Args:
        prompt (str): Text description of the image to generate
        model (str): The model to use: 'dall-e-2' or 'dall-e-3'
        size (str): Image size, e.g., '1024x1024', '1792x1024', etc.
        quality (str): Image quality, 'standard' or 'hd' (for DALL-E 3)
        n (int): Number of images to generate (1-10)
        
    Returns:
        tuple: (response_json, url, data_json, headers, cwd, headers_json) if successful, None otherwise
    """
    try:
        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}"
        }
        data = {
            "model": model,
            "prompt": prompt,
            "n": n,
            "size": size,
            "quality": quality
        }
        
        # Add timeout to prevent hanging on network issues
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            return response.json(), url, json.dumps(data), headers, os.getcwd(), json.dumps(headers)
        else:
            print(f"Error from OpenAI API: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except requests.exceptions.Timeout:
        print("Request timed out. Please check your internet connection and try again.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def save_images(response_data, size, folder_name="openai_images"):
    """
    Save images from API response to disk.
    
    Args:
        response_data (dict): The JSON response from the OpenAI API
        size (str): The size of the images (for filename)
        folder_name (str): Directory name to save images in
        
    Returns:
        list: Paths to saved image files
    """
    saved_files = []
    
    try:
        # Create output directory if it doesn't exist
        output_path = os.path.join(os.getcwd(), folder_name)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # Process each image in the response
        for i, image_data in enumerate(response_data["data"]):
            # For API responses with direct URLs
            if "url" in image_data:
                response = requests.get(image_data["url"], timeout=30)
                img = Image.open(io.BytesIO(response.content))
                
                # Save the image
                file_path = f"{output_path}/image_{i}.png"
                img.save(file_path)
                saved_files.append(file_path)
            
            # For API responses with base64 data
            elif "b64_json" in image_data:
                image_data = base64.b64decode(image_data["b64_json"])
                img = Image.open(io.BytesIO(image_data))
                
                # Save the image
                file_path = f"{output_path}/image_{i}.png"
                img.save(file_path)
                saved_files.append(file_path)
    
        return saved_files
    except Exception as e:
        print(f"Error saving images: {e}")
        return []

def select():
    """
    Function for selecting images (placeholder for future functionality).
    Currently not implemented.
    """
    return []

# Load environment variables from .env file
load_dotenv()

# Set the OpenAI API key if not already set
if not os.environ.get("OPENAI_API_KEY"):
    api_key = input("Please enter your OpenAI API key: ")
    os.environ["OPENAI_API_KEY"] = api_key

# Start the process
print("DALL-E Image Generator")
print("----------------------")

folder_name = "DALL-E" if "folder_name" not in locals() else folder_name
models = ["dall-e-2", "dall-e-3"]

while True:
    try:
        model_index = input(f"Model: {', '.join(models)} : ")
        
        # Default to DALL-E 3 if empty
        if model_index == "" or model_index.isdigit() and int(model_index) == 1:
            model = models[1]  # dall-e-3
            print(f"Using model: {model}")
        elif model_index.isdigit() and int(model_index) == 0:
            model = models[0]  # dall-e-2
            print(f"Using model: {model}")
        elif model_index.lower() in [m.lower() for m in models]:
            model = next(m for m in models if m.lower() == model_index.lower())
            print(f"Using model: {model}")
        else:
            model = models[1]  # Default to dall-e-3
            print(f"Invalid choice. Using {model}")
            
        # Handle size choices
        if model == "dall-e-2":
            sizes = ["256x256", "512x512", "1024x1024"]
        else:  # dall-e-3
            sizes = ["1024x1024", "1792x1024", "1024x1792"]
            
        size_index = input(f"Size: {', '.join(sizes)} : ")
        
        # Handle size selection
        if size_index == "":
            size = sizes[0]  # Default
        elif size_index.isdigit() and 0 <= int(size_index) < len(sizes):
            size = sizes[int(size_index)]
        else:
            try:
                # Check if input matches a size string
                size = next(s for s in sizes if s.lower() == size_index.lower())
            except:
                size = sizes[0]  # Default if not found
                print(f"Invalid size. Please use a number between 0-{len(sizes)-1}")
                
        print(f"Using size: {size}")
        
        # Get prompt from user
        prompt = input("Enter your image prompt: ")
        if prompt == "":
            print("Prompt cannot be empty. Please enter a prompt.")
            continue
            
        # Number of images
        n_images = input("Number of images to generate (1-10): ")
        try:
            n = int(n_images) if n_images else 1
            if not 1 <= n <= 10:
                print("Invalid number. Please use a number between 1-10")
                n = 1
        except:
            print("Invalid input. Please enter a number.")
            n = 1
            
        print(f"Generating {n} image(s)...")
        
        # Generate the images
        response = generate_image(prompt=prompt, model=model, size=size, n=n)
        
        # Save the images
        if response and response[0]:
            image_files = save_images(response[0], size, folder_name)
            for img_path in image_files:
                print(f"Image saved to: {img_path}")
            
            # Ask if user wants to generate more
            again = input("Generate more images? (y/n): ")
            if again.lower() != 'y':
                break
        else:
            print("Failed to generate images. Please try again.")
            
    except KeyboardInterrupt:
        print("\nExiting...")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        
print("Done.")
