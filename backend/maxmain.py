from pathlib import Path
from google import genai

#current file
current_file = Path(__file__)
current_directory = current_file.parent
prompts = current_directory/"Prompts"
artworks_extracting_themes_prompt = (prompts/"Artworks_Extracting_Themes_Prompt.txt").read_text(encoding="utf-8")

google_api_key = "AIzaSyAdCvnxTFuXUCBLK3KX6rtzlyto1qaBA_U"

artwork = input("Enter the name of an artwork: ")

#Adding artwork to prompt
lines = artworks_extracting_themes_prompt.splitlines()
lines[1] += f" {artwork}"
artworks_extracting_themes_prompt = "\n".join(lines)

# Load API key from environment variable
client = genai.Client(api_key=google_api_key)

# Send a prompt to the model
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents= artworks_extracting_themes_prompt

)

if response.text == "ERROR":
    print("I do not recognize that artwork. Please try again.")
    print("")
else:
    print(response.text)
