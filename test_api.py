import requests
import json

def test_model(prompt: str):
    """
    test_model is a function that tests the API by sending a prompt to the /generate endpoint.
    It sends a POST request to the endpoint with the prompt and stream set to False.
    """
    url = "http://localhost:8000/generate"
    data = {
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: {response.status_code}")


def test_stream(prompt: str):
    """
    test_stream is a function that tests the API by sending a prompt to the /generate/stream endpoint.
    It sends a POST request to the endpoint and processes the streaming response.
    """
    url = "http://localhost:8000/generate/stream"  # Fixed URL
    data = {
        "prompt": prompt,
        "stream": True
    }
    
    response = requests.post(url, json=data, stream=True)  # Added stream=True
    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                try:
                    json_response = json.loads(line)
                    print(json_response.get('response', ''), end='', flush=True)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON: {line}")
    else:
        print(f"Error: {response.status_code}")


if __name__ == "__main__":
    # API
    # test_model("What is artificial intelligence?") 
    test_stream("What is space travel?")