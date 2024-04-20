from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.core.files import File
from PIL import Image

#------------------------------------------------------- Gemini model stuff (text)  -----------------------------------
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())  # Loads all environment variables

import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro  API and get response
def get_gemini_response1(question):                 # question is the prompt
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    response = chat.send_message(question)
    return response.text
# -------------------------------------------------------- Gemini model stuff------------------------------------------

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Function to set up image data
def input_image_setup(image_path):
    if os.path.exists(image_path):
        with open(image_path, 'rb') as image_file:
            bytes_data = image_file.read()
            image_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": bytes_data
                }
            ]
            return image_parts
    else:
        raise FileNotFoundError("Image file not found")



#------------------------------------------------------------------------------------------------------------------
# Create your views here.
def index(request):
    return render(request, 'index.html')

def result(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt_inp')

    response = get_gemini_response1(prompt)

    response = response.replace('**', '')
    response = response.replace('*', '')

    context = {
        "var1": response
    }

    return render(request, 'result.html', context)



def visual(request):
    return render(request, 'upload.html')

def prediction(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        image_name = image.name
        static_dir = settings.STATICFILES_DIRS[0]
        static_path = os.path.join(static_dir, 'images')

        if not os.path.exists(static_path):
            os.makedirs(static_path)

        static_path = os.path.join(static_path, image_name)

        with open(static_path, 'wb') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        image_url = f'/static/images/{image_name}'

        # Initialize the app
        input = ""
        image_path = ""
        image = ""

        # Get the input prompt and image path from user input
        input = input or "Enter the input prompt here."
        image_path = image_path or static_path    

        # Set up the image data
        if os.path.exists(image_path):
            image_data = input_image_setup(image_path)
        else:
            raise FileNotFoundError("Image file not found")
        
        input_prompt = """
You are an expert in nutrition where you need to see the food items from the image
and calculate the total calories, also provide the details of every food item with calories intake
in the below format:

1. Item 1 - number of calories
2. Item 2 - number of calories
----
----
"""
        
        # Get the response from the Gemini Pro Vision API
        response = get_gemini_response(input, image_data, input_prompt)
        response = response.strip()

        context = {
        "var1": response
        }

        return render(request, 'predict.html', context)


