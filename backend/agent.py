from pathlib import Path
from google import genai
import re

class Agent:
    # API Key, remove later
    google_api_key = "AIzaSyAdCvnxTFuXUCBLK3KX6rtzlyto1qaBA_U"

    # Gemini Model
    model_name = "gemini-2.5-flash"
    def __init__(self, media_type, name: str = ""):
        if media_type == "artwork":
            self.__artwork = name

            #Gathering files
            current_file = Path(__file__)
            current_directory = current_file.parent
            prompts = current_directory / "Prompts"
            self.__artworks_extracting_themes_prompt = (prompts / "Artworks_Extracting_Themes_Prompt.txt").read_text(
                encoding="utf-8")
            self.__artworks_get_suggestions_prompt = (prompts/ "Artworks_Get_Suggestions_Prompt.txt").read_text(
                encoding="utf-8")

        # Load API key from environment variable
        self.__client = genai.Client(api_key=Agent.google_api_key)

    def add_artwork_to_prompt(self):
        lines = self.__artworks_extracting_themes_prompt.splitlines()
        lines[1] += f" {self.__artwork}"
        self.__artworks_extracting_themes_prompt = "\n".join(lines)

    def get_themes(self):
        response = self.__client.models.generate_content(
            model=Agent.model_name,
            contents=self.__artworks_extracting_themes_prompt
        )
        return response.text

    def suggestions(self):
        response = self.__client.models.generate_content(
            model=Agent.model_name,
            contents=self.__artworks_get_suggestions_prompt
        )
        gemini_list = eval(re.sub(r'```python\n?|```\n?', '', response.text.strip()))
        suggestion_list = []
        for innerList in gemini_list:
            if type(innerList) is list:
                suggestion_list.append(
                    {"Name": innerList[0], "Artist": innerList[1], "Year": innerList[2],
                     "Current Location": innerList[3], "Wikipedia": innerList[4]
                     })
        return suggestion_list

my_agent = Agent("artwork", "The Scream")
my_agent.add_artwork_to_prompt()
print(my_agent.get_themes())
print(my_agent.suggestions())
