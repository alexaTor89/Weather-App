import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap

#Function to get weather info from OpenWeatherMap API
def get_weather(city):
    API_key = "a9a1492e5d479ee09ddbc2ad6885827c"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)
    
    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None
    
    #Parse the response JSON to get weather info
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']

    #Get the icon URL and return weather info
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, city, country)


#Function to search weather for city
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    #if the city is found, unpack the weather 
    icon_url, temperature, description, city, country = result
    location_label.configure(text = f"{city}, {country}")

    #get the icon image from url and update the icon label
    image = Image.open(requests.get(icon_url, stream = True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image = icon)
    icon_label.image = icon

    #update temp and description labels
    temperature_label.configure(text = f"Temperature: {temperature:.2f}°C")
    description_label.configure(text = f"Description: {description}")


root = ttkbootstrap.Window(themename="morph")
root.title("Weather App")
root.geometry("400x500")

#Entry the city name
city_entry = ttkbootstrap.Entry(root, font = "Helvetica, 20")
city_entry.pack(pady=20)

#Button to search
search_button = ttkbootstrap.Button(root, text="Search" , command = search, bootstyle="warning")
search_button.pack(pady=10)

#Show the city name
location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack(pady=20)

#Show the weather icon
icon_label=tk.Label(root)
icon_label.pack()

#Shot the temperature
temperature_label = tk.Label(root, font = "Helvetica, 20")
temperature_label.pack()

#Show weather description
description_label = tk.Label(root, font = "Helvetica, 20")
description_label.pack()

root.mainloop()