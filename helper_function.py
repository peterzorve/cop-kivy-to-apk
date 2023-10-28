import sqlite3 as sq 
from datetime import date, datetime
from kivy.uix.popup import Popup 
from kivy.uix.label import Label
import re 


firebase_config = {
            "apiKey": "AIzaSyDuoL4c6I4Tx5XrLWxNIw3VdDBJ0EV7U7c",
            "authDomain": "cop-akumadan-english.firebaseapp.com",
            "databaseURL": "https://cop-akumadan-english-default-rtdb.europe-west1.firebasedatabase.app",
            "projectId": "cop-akumadan-english",
            "storageBucket": "cop-akumadan-english.appspot.com",
            "messagingSenderId": "111023536619",
            "appId": "1:111023536619:web:a7cc6f2e832d367adf41ae",
            "measurementId": "G-XFXYWS054M"
        }

class Popups(Popup, Label):
    def open_popup(self, title="Title", text="Wrong credential", color=[1, 0, 0, 1]):
        popup = Popup(  title=title,
                        title_size="12dp",
                        title_align="center", 
                        title_color = color,                         
                        content = Label(text=text,
                                        font_name= 'fonts/Montserrat-Regular.ttf',
                                        font_size= "10dp",
                                        halign= "center"
                                        ),
                        size_hint=(None, None), 
                        pos_hint= {'center_x':0.5, "center_y":0.5},
                        # font_name= 'fonts/Montserrat-Bold.ttf',
                        size=(400, 250)
                     )
        popup.open() 

