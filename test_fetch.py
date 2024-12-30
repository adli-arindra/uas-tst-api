import requests
import base64
from io import BytesIO
from PIL import Image

# Define the API endpoint
API_URL = "http://127.0.0.1:5000/haircut"

# Specify the image file to upload
image_path = "uploads/1714577980232.jpg"

def fetch_and_display_image(api_url, image_path):
    # Open the image file
    with open(image_path, "rb") as image_file:
        files = {'image': image_file}

        # Send the POST request to the API
        response = requests.post(api_url, files=files)

    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()

        # Decode the base64-encoded image
        encoded_image = data["image"]
        image_data = base64.b64decode(encoded_image)

        # Display the image using Pillow
        image = Image.open(BytesIO(image_data))
        image.show()

        # Print the haircut data
        print("Haircut Data:")
        print(data["haircut_data"])
    else:
        print(f"Failed to fetch the API. Status code: {response.status_code}")
        print(response.json())

# Call the function
fetch_and_display_image(API_URL, image_path)
