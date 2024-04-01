# import requests
# import uvicorn
from fastapi import FastAPI
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import requests
import uvicorn

# Assuming this is your initial FastAPI setup in the same script
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    # Add more origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello from your FastAPI application!"}

# Step 1: Function to fetch API response
def fetch_api_response(api_url: str) -> List[dict]:
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()  # Assuming the API returns a list of dicts
    else:
        raise Exception("Failed to fetch API response")

# Step 2: Function to generate a FastAPI function from the API response
def generate_fastapi_function(api_data: dict) -> str:
    function_name = api_data.get("name", "default_function")
    function_code = f"""
@app.get("/{function_name}")
async def {function_name}():
    return {{"message": "This endpoint was dynamically generated for {function_name}"}}
"""
    return function_code

# Step 3: Function to append the new function to the FastAPI application file
def append_function_to_file(function_code: str, filename: str="main.py"):
    with open(filename, "a") as file:
        file.write(function_code)

# Main function to tie it all together
def main(api_url: str, update_only: bool=False):
    try:
        api_response = fetch_api_response(api_url)
        for api_data in api_response:
            function_code = generate_fastapi_function(api_data)
            append_function_to_file(function_code)
        print("FastAPI application updated successfully.")
    except Exception as e:
        print(f"Error: {e}")

    if not update_only:
        # Note: Consider running this in a separate terminal or script in a real-world scenario
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

# Adjust API_URL to your actual API endpoint that provides the necessary configuration
API_URL = "https://example.com/api/configuration"

if __name__ == "__main__":
    main(API_URL)
