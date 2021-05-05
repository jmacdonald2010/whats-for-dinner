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
        if (random.randint(0,1)) > 0:
            table_size = conn.execute("SELECT meal_id FROM full_meals")
            table_size = len(table_size.fetchall())
            rand_num = random.randint(0, table_size)
            self.meal_q = conn.execute(f"SELECT meal_name FROM full_meals WHERE meal_id = {rand_num}")
            self.meal_q = self.meal_q.fetchall()
            self.meal_q = self.meal_q[0][0]
            self.meal.text = self.meal_q
        else:
            meal_dict = {}
            for x in ("meat", "veg", "carb"):
                q = conn.execute(f"SELECT {x} FROM {x}")
                q = q.fetchall()
                meal_dict[x] = q[random.randint(0, len(q))]
            self.meal.text = meal_dict["meat"][0]
            self.veg.text = meal_dict["veg"][0]
            self.carb.text = meal_dict["carb"][0]

    '''def build_popup(self):
        popup = Popup(title="Add Food", size_hint=(None, None))
        popup_grid = GridLayout(rows=8, cols=1)
        popup.add_widget(popup_grid)'''

class MyPopup(Popup):

    # Object Properties for the Popup, to allow for entries to be cleared after being entered.
    full_meal = ObjectProperty(None)
    meat_main = ObjectProperty(None)
    veggies = ObjectProperty(None)
    carbs = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MyPopup, self).__init__(**kwargs)

    def update_text(self, field, text, column):
        self.new_entry = {0: field, 1: text, 2: column}

    def update_db(self):
        # try:
        conn.execute(f"INSERT INTO {self.new_entry[0]} ({self.new_entry[2]}) VALUES ('{self.new_entry[1]}');")
        conn.commit()
        print(f"Added {self.new_entry[1]} to DB")
        if self.new_entry[0] == "full_meals":
            self.full_meal.text = ""
        elif self.new_entry[0] == "meat":
            self.meat_main.text = ""
        elif self.new_entry[0] == "veg":
            self.veggies.text = ""
        elif self.new_entry[0] == "carb":
            self.carbs.text = ""
        '''except:
            print("Missing Required Values or other error.")'''

# app class
class MainPage(App):

    def build(self):
        return MainGrid()

if __name__ == "__main__":
    MainPage().run()