import sqlite3
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
import random

# build db or load\
conn = sqlite3.connect("data.db")

# build big meal table
conn.execute("""CREATE TABLE IF NOT EXISTS full_meals (
    meal_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    meal_name TEXT NOT NULL
);
""")

# build meat table
conn.execute("""CREATE TABLE IF NOT EXISTS meat (
    meat_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    meat TEXT NOT NULL
);
""")

# build veg table
conn.execute("""CREATE TABLE IF NOT EXISTS veg (
    veg_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    veg TEXT NOT NULL
);
""")

# build carb table
conn.execute("""CREATE TABLE IF NOT EXISTS carb (
    carb_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    carb TEXT NOT NULL
);
""")

# import kv file
kv_file = Builder.load_file("main.kv")

# Grid Layout Class
class MainGrid(GridLayout):
    # variables for the kv file
    meal = ObjectProperty(None)
    veg = ObjectProperty(None)
    carb = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainGrid, self).__init__(**kwargs)
        self.largest_table = 0

        # determine how many items are in the db
        tables = {"full_meals": "meal_name", "meat": "meat", "veg": "veg", "carb": "carb"}
        for x in tables:
            q = conn.execute(f"SELECT {tables[x]} FROM {x}")
            q = q.fetchall()
            if len(q) > self.largest_table:
                self.largest_table = len(q)

    def build_meal(self):
        if (random.range(0,1)) > 0:
            table_size = ("SELECT meal_id FROM full_meals")
            table_size = len(table_size.fetchall())
            rand_num = random.range(0, (table_size - 1))
            self.meal = conn.execute(f"SELECT * FROM full_meals WHERE meal_id = {rand_num}")
            self.meal = self.meal.fetchall()
            self.meal = self.meal[0]
        else:
            meal_dict = {}
            for x in ("meat", "veg", "carb"):
                q = conn.execute(f"SELECT {x} FROM {x}")
                q = q.fetchall()
                meal_dict[x] = q[random.range(0, (len(q) - 1))]
            self.meal = meal_dict["meat"]
            self.veg = meal_dict["veg"]
            self.carb = meal_dict["carb"]

# app class
class MainPage(App):

    def build(self):
        return MainGrid()

if __name__ == "__main__":
    MainPage().run()