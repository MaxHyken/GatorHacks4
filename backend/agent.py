from pathlib import Path
from google import genai

class Agent:
    # API Key, remove later
    google_api_key = "AIzaSyAdCvnxTFuXUCBLK3KX6rtzlyto1qaBA_U"
    def __init__(self, media_type, name: str = ""):
        if media_type == "artwork":
            self.__artwork = name

            #Gathering files
            current_file = Path(__file__)
            current_directory = current_file.parent
            prompts = current_directory / "Prompts"
            self.__artworks_extracting_themes_prompt = (prompts / "Artworks_Extracting_Themes_Prompt.txt").read_text(
                encoding="utf-8")

        # Load API key from environment variable
        self.__client = genai.Client(api_key=Agent.google_api_key)

    def add_artwork_to_prompt(self):
        lines = self.__artworks_extracting_themes_prompt.splitlines()
        lines[1] += f" {self.__artwork}"
        self.__artworks_extracting_themes_prompt = "\n".join(lines)

    def get_themes(self):
        response = self.__client.models.generate_content(
            model="gemini-2.5-flash",
            contents=self.__artworks_extracting_themes_prompt
        )
        return response


'''
if response.text == "ERROR":
    print("I do not recognize that artwork. Please try again.")
    print("")
else:
    print(response.text)'''
