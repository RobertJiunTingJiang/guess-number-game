import requests

URL = "https://tavstphloajcmrfkgzkv.supabase.co/rest/v1/?apikey=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRhdnN0cGhsb2FqY21yZmtnemt2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc5MzcxNzUsImV4cCI6MjA4MzUxMzE3NX0.GG-f63-TTGbWapOQrKLxjQt3axCnMOcqUIp_24eHwLg"

headers = {
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRhdnN0cGhsb2FqY21yZmtnemt2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc5MzcxNzUsImV4cCI6MjA4MzUxMzE3NX0.GG-f63-TTGbWapOQrKLxjQt3axCnMOcqUIp_24eHwLg",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRhdnN0cGhsb2FqY21yZmtnemt2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc5MzcxNzUsImV4cCI6MjA4MzUxMzE3NX0.GG-f63-TTGbWapOQrKLxjQt3axCnMOcqUIp_24eHwLg"
}

try:
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        spec = response.json()
        definitions = spec.get("definitions", {})
        table_info = definitions.get("py_scores_0120c", {})
        properties = table_info.get("properties", {})
        print("Table 'py_scores_0120c' has the following columns:")
        for col in properties.keys():
            print(f"- {col}")
    else:
        print(f"Failed to fetch spec: {response.status_code}, {response.text}")
except Exception as e:
    print(f"Error: {e}")
