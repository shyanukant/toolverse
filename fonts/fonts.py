import os
import requests

# download popular font from google fonts api
def fetch_google_font(font_name):
    api_key = os.environ.get('GOOGLE_API_KEY')
    api_url = f"https://www.googleapis.com/webfonts/v1/webfonts?key={api_key}&family={font_name}:regular"

    path = "C:/Users/admin/Desktop/buildspace/buildsocia/static/fonts"
    try:
        response = requests.get(api_url)
        font_path = os.path.join(path, f"{font_name}.ttf")
        with open(font_path, "wb") as font_file:
            font_file.write(response.content)
        

    except requests.exceptions.RequestException as e:
        print(f"Error {e}")
        return []


# downlaod fonts 
popular_google_fonts = [
    "Roboto",
    "Open Sans",
    "Lato",
    "Montserrat",
    "Poppins",
    "Merriweather",
    "Raleway",
    "Playfair Display",
    "Source Sans Pro",
    "Crimson Text",
    "Nunito",
    "Oswald",
    "Quicksand",
    "Ubuntu",
    "Inconsolata",
    "Pacifico",
    "Dancing Script",
    "Cabin",
    "Bebas Neue",
    "Alegreya",
    "Arimo",
    "Karla",
    "Fira Sans",
    "Archivo",
    "Cormorant Garamond"
]


# for font in popular_google_fonts:
#     print("processing")
#     fetch_google_font(font)
#     print("end")
    