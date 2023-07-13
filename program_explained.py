from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
# from PIL import ImageTk

root = Tk()     # It is an intance/object of class "Tk()".

root.title("Weather App")
root.geometry("900x500")
root.resizable(False, False)        # This method is used when user wants a specific size of the GUI window. 
                                    # The "minimize"/"maximize" button is disabled when false. 
root.minsize(900, 500)          
# root.maxsize(1380, 720)

def getWeather():
    try:

        # To get the user input, which the user will provide in the GUI. 
        # The "city" name entered by the user is passed to the "city" variable by using the ".get()" method. 
        city = textfield.get()

        # To get the timezone of the seached city
        # "geolocator" is an instance of the "Nominatim" geocoding service from the "geopy.geocoders" module.
        # The "nominatim" class proivdes the access for geocoding which is converting the city names into their
        # geographic coordinates. 
        # So to use the methods of "Nominatim" class or to get the geographic coordinates of the city, an instance of 
        # this class is created, which is "geolocator. 
        #"user_agent" - is a parameter which makes geocoding requests, in this case it is using the "geoapiExercises". 
        geolocator = Nominatim(user_agent = "geoapiExercises")

        # By using the "geolocator" instance of the "Nominatim" class, we are using the "geocode()" method to find the 
        # location of the user input "city". 
        # The "geocode()" method then takes the city name and tries to find a match in its database. 
        # After the method finds a match, it sends a geolocation object that contains various information about the city
        # like latittude and longitude, and "location" variable is used to store this geolocation object.
        location = geolocator.geocode(city)

        # these coordinates are then used to find the timezone of the city. 
        # "obj" is an instance of the "TimezoneFinder()" class. 
        obj = TimezoneFinder()

        # with the help of "obj" object we are using the "timezone_at()" method to get the timezone of the searched city.
        result = obj.timezone_at(lng = location.longitude, lat=location.latitude)
        # print(result)

        # To display the Current time when a city is searched.
        home = pytz.timezone(result)    # creating a "pytz.timezone" object. 

        local_time = datetime.now(home)     # retrives the current time, based on the timezone speicified by the "home" object.
        # the "datetime.now()" function is used get the current date and time of the passed timezone. 
        current_time = local_time.strftime("%I:%M %p")      # the "strftime()" method is used to format the local_time 
        # according to the speicifed format string. 
        clock.config(text=current_time)     # Updating in the GUI. 
        name.config(text="CURRENT WEATHER")     # updating in the GUI. 

        # Weather
        api = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=7d8b97ff910062a8c9905c256aa3be43"

        json_data = requests.get(api).json()       # the request is sent to the api, and the result is stored in json format
                                                   # because of ".json()" function, and is stored in the json_data variable.
        print(json_data)

        condition = json_data['weather'][0]['main']     # this retrives the value of "main" key from the first element
                                                        # of the "weather" array in the json data.
                                                        # "[0]" means accessing the first element of the "weather" array.
        description = json_data['weather'][0]['description']    # retrives the value of "desctiption" key from the 
                                                                # first element of the "weather" array in json data. 
        temp = int(json_data['main']['temp']-273.15)    # getting "temp" value from the "temp" key in the "main" 
                                                        # dictionary. 
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity'] 
        wind = json_data['wind']['speed']

        t.config(text=(temp, "°"))
        c.config(text=(condition, "|", "FEELS", "LIKE", temp, "°"))

        w.config(text=wind)
        h.config(text=humidity)
        d.config(text=description)
        p.config(text=pressure)

    except Exception as e:
        messagebox.showerror("Weather Application", "Invalid Entry!!")

# Search box
Search_image = PhotoImage(file="Images\search.png")
myimage = Label(image = Search_image)
myimage.place(x=20, y=20)

textfield = tk.Entry(root, justify="center", width=17, font=("poppins", 23), bg="#404040", border=0, fg="white")
textfield.place(x=60, y=40)
textfield.focus()       # "focus()" method means, by default the following will have active cursor. It is like the dotted
                        # outline on the button.

Search_icon = PhotoImage(file="Images\search_icon.png")
myimage_icon = Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getWeather)
# The above line uses the "maginifier" icon image as a button to read user input and initiate "getWeather" function.
myimage_icon.place(x=400, y=33)

# Logo
# This is the weather image but it does not correspond to the weather data. Like it remains same for sunny day or snowfall.
Logo_image = PhotoImage(file="Images\logo.png")
logo = Label(image=Logo_image)
logo.place(x=150, y=100)

# Bottom Box
# This is a box containing the stats about weather, like wind speed, humidity, description and pressure. 
Frame_image = PhotoImage(file="Images\Box.png")
Frame_myimage = Label(image=Frame_image)
Frame_myimage.pack(padx=5, pady=5, side=BOTTOM)

# Time
# This is used to display the current time of the searched location.
name = Label(root, font=("arial", 15, "bold"))
name.place(x=30, y=100)
clock = Label(root, font=("helvetica", 20))
clock.place(x=30, y=130)


# Label
label1 = Label(root, text="WIND", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label1.place(x=120, y=400)

label2 = Label(root, text="HUMIDITY", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label2.place(x=250, y=400)

label3 = Label(root, text="DESCRIPTION", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label3.place(x=430, y=400)

label4 = Label(root, text="PRESSURE", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label4.place(x=650, y=400)

t = Label(font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)

c = Label(font=("arial", 15, "bold"))
c.place(x=400, y=250)

# Ideal loading
w = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
w.place(x=120, y=430)

h = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
h.place(x=280, y=430)

d = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
d.place(x=450, y=430)

p = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
p.place(x=670, y=430)

root.mainloop()     