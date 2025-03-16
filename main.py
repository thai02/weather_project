import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap
import os
from dotenv import load_dotenv

load_dotenv()

# Function to get weather information from OpenWeatherMap API
def get_weather(city):
    api_key = os.getenv("api_key_weather") #Include your API Key in a ".env" file and put the variable from the file here
    lang_mapping = {"English": "en", "简体中文": "zh_cn", "Português(Brasil)":"pt_br"}
    selected_lang = choose_language.get()
    global lang
    lang = lang_mapping.get(selected_lang, "en")
    base_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang={lang}"
    weather_data = requests.get(base_url)

    update_button_text()

    if weather_data.status_code == 404 and lang == "en":
        messagebox.showerror(title="Error - City not found", message="Please try searching for a different city.")
    elif weather_data.status_code == 404 and lang == "zh_cn":
        messagebox.showerror(title="错误 - 未找到城市", message="请尝试搜索其他城市。")
    elif weather_data.status_code == 404 and lang == "pt_br":
        messagebox.showerror(title="Erro - cidade não encontrada", message="Por favor tente buscar por uma cidade diferente.")
        return None
    
    # Parse the response JSON to get weather information 
    weather = weather_data.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15 
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']
    

    # Get the icon and return all the weather information
    if icon_id == "11d" or icon_id == "11n":
        icon_id = Image.open("./icons/thunderstorm.png").resize((100,100))
    elif icon_id == "10d" or icon_id == "09d" or icon_id == "10n" or icon_id == "09n":
        icon_id = Image.open("./icons/rain.png").resize((100,100))
    elif icon_id == "13d" or icon_id == "13n":
        icon_id = Image.open("./icons/snow.png").resize((100,100))
    elif icon_id == "50d" or icon_id == "50n":
        icon_id = Image.open("./icons/mist.png").resize((100,100))
    elif icon_id == "01d":
        icon_id = Image.open("./icons/sunny.png").resize((100,100))
    elif icon_id == "01n":
        icon_id = Image.open("./icons/moon.png").resize((100,100))
    elif icon_id == "02d":
        icon_id = Image.open("./icons/few_clouds_day.png").resize((100,100))
    elif icon_id == "02n":
        icon_id = Image.open("./icons/few_clouds_night.png").resize((100,100))
    elif icon_id == "03d" or icon_id == "03n" or icon_id == "04d" or icon_id == "04n":
        icon_id = Image.open("./icons/scattered_broken_clouds.png").resize((100,100))
    return (lang, icon_id, temperature, description, city, country)
  
# Function to update the button text
def update_button_text():
    if lang == "en":
        search_button.config(text="Search")
    elif lang == "zh_cn":
        search_button.config(text="搜索")
    elif lang == "pt_br":
        search_button.config(text="Buscar")

# Function to search weather for a city
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    # If the city is found, unpack the weather information
    lang, icon_id, temperature, description, city, country = result
    location_label.configure(text=f"{city}, {country}")

    # Get the weather icon image from the file and update the icon label
    icon_id = ImageTk.PhotoImage(icon_id)
    icon_label.configure(image=icon_id)
    icon_label.image = icon_id

    #Update the temperature and description labels
    if lang == "en":
        temperature_label.configure(text=f"Temperature: {temperature:.2f}°C")
        description_label.configure(text=f"Description: {description}")
    elif lang == "zh_cn":
        temperature_label.configure(text=f"温度: {temperature:.2f}°C")
        description_label.configure(text=f"描述: {description}")
    elif lang == "pt_br":
        temperature_label.configure(text=f"Temperatura: {temperature:.2f}°C")
        description_label.configure(text=f"Descrição: {description}")


root = ttkbootstrap.Window(themename="superhero")
root.title("Weather App")
root.geometry("800x500")

# Dropdown to choose the language
choices = ["Português(Brasil)", "简体中文", "English"]
choose_language = ttkbootstrap.Combobox(root, values=choices)
choose_language.set("Choose your language")
choose_language.pack(side="bottom", anchor="sw", pady=10, padx=10)

#Entry widget - to enter the city name
city_entry = ttkbootstrap.Entry(root, font="Helvetica, 18")
city_entry.pack(pady=10)

#Button widget - to search for the weather information
search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="info")
search_button.pack(pady=10)

#Label widget - to show the city/country name
location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack(pady=10)

#Label widget - to show the weather icon
icon_label = tk.Label(root)
icon_label.pack()

#Label widget - to show the temperature
temperature_label = tk.Label(root, font="Helvetica, 20")
temperature_label.pack(pady=10)
temperature_label.pack()

#Label widget - to show the weather description
description_label = tk.Label(root, font="Helvetica, 20")
description_label.pack()

root.mainloop()
