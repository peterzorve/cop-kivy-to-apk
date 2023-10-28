# pip install Kivy
# pip install kivymd
# pip install pyrebase4 
# pip install pandas 


from kivymd.app import MDApp 
import pyrebase 
# from kivy.lang import Builder 
from datetime import date, datetime
from kivy.uix.screenmanager import Screen, ScreenManager 
from kivy.properties import ObjectProperty
from kivy.properties import ObjectProperty
import pandas as pd 
import random 
import string
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from helper_function import firebase_config, Popups
import random


class Screen_Manger(ScreenManager):
    pass 



#===    9. MemberChurchInformationPage  ============================================================================================ 
class MemberChurchInformationPage(Screen):
    def __init__(self, **kwargs): 
        super(MemberChurchInformationPage, self).__init__(**kwargs)

    table_added = False 
    firebase = pyrebase.initialize_app(firebase_config) 
    auth     = firebase.auth() 
    database = firebase.database() 

    def church_informations(self):
        df = pd.DataFrame()
        try:
            services = self.database.child("english_assembly").child("churchservice").get() 
            dataframe = {}
            for service in services.each():
                dataframe[service.key()] = service.val()
            df = pd.DataFrame.from_dict(dataframe, orient="index") 
            df = df[["day_date_time", "weekevent", "tithe", "offertory", "attendacemen",  "attendacewomen", "attendacechildren", "visitors", "description", "person"]]
            df.rename(columns = {"day_date_time": 'Date / Day / Time',
                                'attendacechildren':'Children', 
                                "attendacemen": "Men", 
                                "attendacewomen": "Women",
                                "description": "Description", 
                                "offertory": "Offertory", 
                                "person": "Person",
                                "tithe": "Tithe", 
                                "visitors": "Visitors",
                                "weekevent": "Week Event"}, inplace = True)
        except:
            pass 
        return df 

    def display_table(self):
        user_table = self.church_informations()
        length_of_data = len(user_table)
        if length_of_data > 0:
            if self.table_added == False: 
                self.data_tables = MDDataTable(
                    pos_hint={'center_x': 0.5, 'center_y': 0.4},
                    size_hint=(0.9, 0.7),
                    use_pagination=True,
                    check=True,
                    rows_num = 100, 
                    pagination_menu_height = "240dp",
                    height= "24dp",
                    size =  (6, 6),
                    background_color_header="#000000",
                    column_data = [ (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Date / Day / Time   [/font][/color][/size]", dp(45)),                    
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Week Event          [/font][/color][/size]", dp(20)),
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Tithe               [/font][/color][/size]", dp(12)),
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Offertory           [/font][/color][/size]", dp(12)),
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Men                 [/font][/color][/size]", dp(12)),
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Women               [/font][/color][/size]", dp(12)),
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Children            [/font][/color][/size]", dp(12)),
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Visitors            [/font][/color][/size]", dp(12)),
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Person              [/font][/color][/size]", dp(20)),
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Description         [/font][/color][/size]", dp(45))
                                ],
                    row_data = [(   f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['Date / Day / Time'][i]}  [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['Week Event'][i]}         [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['Tithe'][i]}              [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['Offertory'][i]}          [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['Men'][i]}                [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['Women'][i]}              [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['Children'][i]}           [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['Visitors'][i]}           [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['Person'][i]}             [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['Description'][i]}        [/font][/color][/size]",
                                    )  for i in range(length_of_data)
                                ])
                self.add_widget(self.data_tables)
                self.table_added = True 
        else: 
            Popups().open_popup(title="NO DATA", text=f"No Data to display", color=[1, 0, 0, 1])
            
    def dismiss_table(self):
        if self.table_added == True: 
            self.remove_widget(self.data_tables)
            self.table_added = False 

    def go_back(self):
        self.manager.current = "name_memberprofile"
        if self.table_added == True: 
            self.remove_widget(self.data_tables)
            self.table_added = False 

#=================================================================================================================================== 
#===    8. MemberCheckMembersInformationPage  ============================================================================================
#=================================================================================================================================== 
class MemberCheckMembersInformationPage(Screen):
    id_type_of_member_by_member = ObjectProperty(None)
    table_added = False 
    result_found = False 
    firebase = pyrebase.initialize_app(firebase_config)
    authentication = firebase.auth() 
    database = firebase.database()

    def __init__(self, **kwargs): 
        super(MemberCheckMembersInformationPage, self).__init__(**kwargs)

    def members_informations(self, type_of_member):  
        dataframe = {} 
        df = pd.DataFrame() 
        if type_of_member == "Members":
            try:
                members = self.database.child("english_assembly").child("church_members").get() 
                for member in members.each():
                    dataframe[member.key()] = member.val()
                df = pd.DataFrame.from_dict(dataframe, orient="index") 
                df = df[["fullname",  "email", "phonenumber",  "statue"]]
            except: 
                pass 
        if type_of_member == "Presbytery":
            try:
                members = self.database.child("english_assembly").child("church_presbytery").get() 
                for member in members.each():
                    dataframe[member.key()] = member.val()
                df = pd.DataFrame.from_dict(dataframe, orient="index") 
                df = df[["fullname",  "email", "phonenumber",  "statue"]]
            except: 
                pass 
        return df 


    def display_table(self):
        type_of_member = self.id_type_of_member_by_member.text.strip()
        user_table = self.members_informations(type_of_member) 
        length_of_data = len(user_table) 
        if length_of_data > 0:
            if self.table_added == False: 
                self.data_tables = MDDataTable(
                    pos_hint={'center_x': 0.5, 'center_y': 0.44},
                    size_hint=(0.6, 0.7),
                    use_pagination=True,
                    check=True,
                    rows_num = 100, 
                    pagination_menu_height = "240dp",
                    height= "24dp",
                    size =  (6, 6),
                    background_color_header="#000000",
                    column_data = [ (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Name            [/font][/color][/size]", dp(40)),                    
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Email           [/font][/color][/size]", dp(40)),
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Phone number    [/font][/color][/size]", dp(25)),
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Statue          [/font][/color][/size]", dp(25))
                                ],
                    row_data = [(   f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['fullname'][i].title()}       [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['email'][i]}          [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['phonenumber'][i]}    [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['statue'][i].capitalize()}         [/font][/color][/size]"
                                    )  for i in range(length_of_data)
                                ])
                
                self.add_widget(self.data_tables)
                self.table_added = True 
        else: 
            Popups().open_popup(title="NO DATA", text=f"No Data to display", color=[1, 0, 0, 1])
            
    def dismiss_table(self):
        if self.table_added == True: 
            self.remove_widget(self.data_tables)
            self.table_added = False

    def go_back(self):
        self.manager.current = "name_memberprofile"
        if self.table_added == True: 
            self.remove_widget(self.data_tables)
            self.table_added = False
        # print("go back")


#=================================================================================================================================== 
#===    7.  ChurchMemberProfilePage  ====================================================================================================
#===================================================================================================================================
class ChurchMemberProfilePage(Screen):
    id_welcome_member = ObjectProperty(None)  
    id_email_phonenumber_member =  ObjectProperty(None)  
    user_credential = ""

    def login_credential(self, name): 
        self.user_credential = name 
        user_name = self.user_credential["name"]
        user_email = self.user_credential["email"]
        user_phonenumber = self.user_credential["phonenumber"]
        user_statue = self.user_credential["statue"]
        user_name = user_name.title() 
        self.ids.id_welcome_member.text = "" + user_name
        self.ids.id_email_phonenumber_member.text = user_email + "    ||    " + user_phonenumber 

#=================================================================================================================================== 
#===    6. CheckMembersInformationPage  ============================================================================================
#=================================================================================================================================== 
class CheckMembersInformationPage(Screen):
    id_type_of_member = ObjectProperty(None)
    table_added = False 
    result_found = False 
    firebase = pyrebase.initialize_app(firebase_config)
    authentication = firebase.auth() 
    database = firebase.database()

    def __init__(self, **kwargs): 
        super(CheckMembersInformationPage, self).__init__(**kwargs)

    def members_informations(self, type_of_member):  
        dataframe = {} 
        df = pd.DataFrame()
        if type_of_member == "Members":
            try:
                members = self.database.child("english_assembly").child("church_members").get() 
                for member in members.each():
                    dataframe[member.key()] = member.val()
                df = pd.DataFrame.from_dict(dataframe, orient="index") 
                df = df[["fullname",  "email", "phonenumber",  "statue"]]
            except: 
                pass 
        if type_of_member == "Presbytery":
            try:
                members = self.database.child("english_assembly").child("church_presbytery").get() 
                for member in members.each():
                    dataframe[member.key()] = member.val()
                df = pd.DataFrame.from_dict(dataframe, orient="index") 
                df = df[["fullname",  "email", "phonenumber",  "statue"]]
            except: 
                pass 
        return df 

    def display_table(self):
        type_of_member = self.id_type_of_member.text.strip()
        user_table = self.members_informations(type_of_member) 
        length_of_data = len(user_table) 
        if length_of_data > 0:
            if self.table_added == False: 
                self.data_tables = MDDataTable(
                    pos_hint={'center_x': 0.5, 'center_y': 0.44},
                    size_hint=(0.65, 0.7),
                    use_pagination=True,
                    check=True,
                    rows_num = 100, 
                    pagination_menu_height = "240dp",
                    height= "24dp",
                    size =  (6, 6),
                    background_color_header="#000000",
                    column_data = [ (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Name            [/font][/color][/size]", dp(40)),                    
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Email           [/font][/color][/size]", dp(40)),
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Phone number    [/font][/color][/size]", dp(25)),
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Statue          [/font][/color][/size]", dp(25))
                                ],
                    row_data = [(   f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['fullname'][i].title()}       [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['email'][i]}          [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['phonenumber'][i]}    [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['statue'][i].capitalize()}         [/font][/color][/size]"
                                    )  for i in range(length_of_data)
                                ])
                self.add_widget(self.data_tables)
                self.table_added = True 
        else: 
            Popups().open_popup(title="NO DATA", text=f"No Data to display", color=[1, 0, 0, 1])
            
    def dismiss_table(self):
        if self.table_added == True: 
            self.remove_widget(self.data_tables)
            self.table_added = False 
    
    def go_back(self):
        self.manager.current = "name_administrationpage"
        if self.table_added == True: 
            self.remove_widget(self.data_tables)
            self.table_added = False   


#=================================================================================================================================== 
#===    5. ChurchInformationPage  ============================================================================================
#=================================================================================================================================== 
class ChurchInformationPage(Screen):
    table_added = False 
    firebase = pyrebase.initialize_app(firebase_config)
    auth = firebase.auth() 
    database = firebase.database()

    def __init__(self, **kwargs): 
        super(ChurchInformationPage, self).__init__(**kwargs)

    def church_informations(self):
        df = pd.DataFrame()
        try:
            services = self.database.child("english_assembly").child("churchservice").get() 
            dataframe = {}
            for service in services.each():
                dataframe[service.key()] = service.val()
            df = pd.DataFrame.from_dict(dataframe, orient="index") 
            df = df[["day_date_time", "weekevent", "tithe", "offertory", "attendacemen",  "attendacewomen", "attendacechildren", "visitors", "description", "person"]]
            df.rename(columns = {"day_date_time": 'Date / Day / Time',
                                'attendacechildren':'Children', 
                                "attendacemen": "Men", 
                                "attendacewomen": "Women",
                                "description": "Description", 
                                "offertory": "Offertory", 
                                "person": "Person",
                                "tithe": "Tithe", 
                                "visitors": "Visitors",
                                "weekevent": "Week Event"}, inplace = True)
        except:
            pass 
        return df 

    def display_table(self):
        user_table = self.church_informations()
        length_of_data = len(user_table)
        if length_of_data > 0:
            if self.table_added == False: 
                self.data_tables = MDDataTable(
                    pos_hint={'center_x': 0.5, 'center_y': 0.40},
                    size_hint=(0.9, 0.78),
                    use_pagination=True,
                    check=True,
                    rows_num = 100, 
                    pagination_menu_height = "240dp",
                    height= "20dp",
                    size =  (6, 6),
                    background_color_header="#000000",
                    column_data = [ (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Date / Day / Time   [/font][/color][/size]", dp(45)),                    
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Week Event          [/font][/color][/size]", dp(20)),
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Tithe               [/font][/color][/size]", dp(12)),
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Offertory           [/font][/color][/size]", dp(12)),
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Men                 [/font][/color][/size]", dp(12)),
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Women               [/font][/color][/size]", dp(12)),
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Children            [/font][/color][/size]", dp(12)),
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Visitors            [/font][/color][/size]", dp(12)),
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Updated by          [/font][/color][/size]", dp(20)),
                                    (f"[size=12][color=#FCA510][font=fonts/Montserrat-Bold.ttf] Description         [/font][/color][/size]", dp(45))
                                ],
                    row_data = [(   f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['Date / Day / Time'][i]}  [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['Week Event'][i]}         [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['Tithe'][i]}              [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['Offertory'][i]}          [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['Men'][i]}                [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['Women'][i]}              [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['Children'][i]}           [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['Visitors'][i]}           [/font][/color][/size]",
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['Person'][i]}             [/font][/color][/size]", 
                                    f"[size=10][color=#000000][font=fonts/Montserrat-Regular.ttf] {user_table['Description'][i]}        [/font][/color][/size]"
                                    )  for i in range(length_of_data)
                                ])
                self.add_widget(self.data_tables)
                self.table_added = True 
        else: 
            Popups().open_popup(title="NO DATA", text=f"No Data to display", color=[1, 0, 0, 1])
            
    def dismiss_table(self):
        if self.table_added == True: 
            self.remove_widget(self.data_tables)
            self.table_added = False

    def go_back(self):
        self.manager.current = "name_administrationpage"
        if self.table_added == True: 
            self.remove_widget(self.data_tables)
            self.table_added = False
        # pass 

#===================================================================================================================================
#===    4.  UpdateAfterService      ============================================================================================
#===================================================================================================================================
class UpdateAfterService(Screen): 

    id_weekevent = ObjectProperty(None) 
    id_attendacemen = ObjectProperty(None) 
    id_attendacewomen = ObjectProperty(None) 
    id_attendacechildren = ObjectProperty(None) 
    id_tithe = ObjectProperty(None) 
    id_offertory = ObjectProperty(None) 
    id_description  = ObjectProperty(None) 
    id_visitors = ObjectProperty(None) 
    user_fullname = ""
    user_credential = ""
    table_added = False  
    firebase = pyrebase.initialize_app(firebase_config)
    auth = firebase.auth() 
    database = firebase.database()

    def login_credential(self, name):
        self.user_credential = name 
        user_name = self.user_credential["name"]
        user_email = self.user_credential["email"]
        user_phonenumber = self.user_credential["phonenumber"]
        user_statue = self.user_credential["statue"]
        self.user_fullname = user_name

    def day_date_time(self):
        today = date.today()
        if today.weekday() == 0:
            day_of_week = "Monday"
        elif today.weekday() == 1:
            day_of_week = "Tuesday"
        elif today.weekday() == 2:
            day_of_week = "Wednesday"
        elif today.weekday() == 3:
            day_of_week = "Thursday"
        elif today.weekday() == 4:
            day_of_week = "Friday"
        elif today.weekday() == 5:
            day_of_week = "Saturday"
        else:
            day_of_week = "Sunday"
        today_date = str(today)
        now = datetime.now()
        return today_date + ", " + day_of_week + ", " + str(now.strftime("%H:%M:%S"))

    def submit(self): 
        day_date_time = self.day_date_time()
        weekevent = self.id_weekevent.text.strip() 
        attendacemen = self.id_attendacemen.text.strip() 
        attendacewomen = self.id_attendacewomen.text.strip() 
        attendacechildren = self.id_attendacechildren.text.strip() 
        tithe = self.id_tithe.text.strip() 
        visitors = self.id_visitors.text.strip() 
        offertory = self.id_offertory.text.strip() 
        description = self.id_description .text.strip() 
        person = self.user_fullname 
        
        if (weekevent == "Week Event"):
            Popups().open_popup(title="WEEK EVENT MISSING", text="Select the week event", color=[1, 0, 0, 1])
        elif (weekevent != "Week Event") and ((len(str(attendacemen)) > 0 ) or (len(str(attendacewomen)) > 0 ) or (len(str(attendacechildren)) > 0 )) and len(str(tithe)) > 0 and len(str(offertory)) > 0:
            if attendacemen == "":
                attendacemen = 0 
            if attendacewomen == "":
                attendacewomen = 0 
            if attendacechildren == "":
                attendacechildren = 0 
            if visitors == "":
                visitors = 0 
            data = {    "day_date_time": day_date_time,         
                        "weekevent": weekevent, 
                        "attendacemen": attendacemen,           
                        "attendacewomen": attendacewomen, 
                        "attendacechildren": attendacechildren, 
                        "tithe": tithe, 
                        "offertory": offertory,                 
                        "visitors": visitors,
                        "description": description,             
                        "person": person 
                    }
            try:
                self.database.child("english_assembly").child("churchservice").child(day_date_time).set(data)
                self.ids.id_weekevent.text = "Week Event" 
                self.ids.id_attendacemen.text = "" 
                self.ids.id_attendacewomen.text = "" 
                self.ids.id_attendacechildren.text = "" 
                self.ids.id_tithe.text = "" 
                self.ids.id_visitors.text = "" 
                self.ids.id_offertory.text = "" 
                self.ids.id_description.text = "" 
                Popups().open_popup(title="UPLOAD SUCCESSFULLY", text="Data uploaded successfullly", color=[0, 1, 0, 1])
            except:
                Popups().open_popup(title="FAILED", text="Something went wrong. \nTry again later", color=[1, 0, 0, 1])
        else:
            Popups().open_popup(title="ITEM MISSING", text="One or more colums missing", color=[1, 0, 0, 1])
        
    def clear_information(self):
        self.ids.id_weekevent.text = "Week Event"
        self.ids.id_attendacemen.text = ""
        self.ids.id_attendacewomen.text = ""
        self.ids.id_attendacechildren.text = ""
        self.ids.id_tithe.text = ""
        self.ids.id_visitors.text = "" 
        self.ids.id_offertory.text = ""
        self.ids.id_description.text = ""

    def go_back(self):
        self.manager.current = "name_administrationpage"
    
    def dismiss_table(self):
        if self.table_added == True: 
            self.remove_widget(self.data_tables)
            self.table_added = False


#=================================================================================================================================== 
#====   3.  AddChurchMemberPage  ===================================================================================================
#===================================================================================================================================
class AddChurchMemberPage(Screen):
    id_membertype = ObjectProperty(None) 
    id_generate_code = ObjectProperty(None)
    id_generated_code_signup =  ObjectProperty(None)

    firebase = pyrebase.initialize_app(firebase_config)
    authentication = firebase.auth() 
    database = firebase.database()

    def __init__(self, **kwargs): 
        super(AddChurchMemberPage, self).__init__(**kwargs)

    def day_date_time(self):
        today = date.today()
        if today.weekday() == 0:
            day_of_week = "Monday"
        elif today.weekday() == 1:
            day_of_week = "Tuesday"
        elif today.weekday() == 2:
            day_of_week = "Wednesday"
        elif today.weekday() == 3:
            day_of_week = "Thursday"
        elif today.weekday() == 4:
            day_of_week = "Friday"
        elif today.weekday() == 5:
            day_of_week = "Saturday"
        else:
            day_of_week = "Sunday"
        today_date = str(today)
        now = datetime.now()
        return today_date + ", " + day_of_week + ", " + str(now.strftime("%H:%M:%S"))
    
    def generate_code(self):
        membertype = self.id_membertype.text 
        if membertype == "Select Member":
            Popups().open_popup(title="MEMBERSHIP STATUE MISSING", text="Select the membeship statue first", color=[1, 0, 0, 1])
        if membertype == "Elder":
            try:
                random_code = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + str(random.randint(10, 99)) + str(random.randint(10, 99))     
                time = self.day_date_time()
                data = { "code": random_code} 
                self.database.child("english_assembly").child("signup_code_elders").child(time).set(data) 
                self.id_generated_code_signup.text = "Elder :  " + random_code
                self.id_membertype.text = "Select Member"    
                self.id_generate_code.text = "Generate a new code"
                self.id_generate_code.text_color = "#ff0000" 
                self.id_generate_code.md_bg_color = "#ffefea"
                self.id_generate_code.line_color = "#ff0000"
                self.id_generate_code.line_width = 2  
            except:
                Popups().open_popup(title="MISSING COLUMN", text="Something went wrong! \nCheck your network and try again later...", color=[1, 0, 0, 1])
        if membertype == "Deacon":
            try:
                random_code = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + str(random.randint(10, 99)) + str(random.randint(10, 99))     
                time = self.day_date_time()
                data = { "code": random_code} 
                self.database.child("english_assembly").child("signup_code_deacons").child(time).set(data) 
                self.id_generated_code_signup.text = "Deacon :  " + random_code
                self.id_membertype.text = "Select Member"   
                self.id_generate_code.text = "Generate a new code"
                self.id_generate_code.text_color = "#ff0000" 
                self.id_generate_code.md_bg_color = "#ffefea"
                self.id_generate_code.line_color = "#ff0000"
                self.id_generate_code.line_width = 2  
            except:
                Popups().open_popup(title="MISSING COLUMN", text="Something went wrong! \nCheck your network and try again later...", color=[1, 0, 0, 1])
        if membertype == "Deaconness":
            try:
                random_code = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + str(random.randint(10, 99)) + str(random.randint(10, 99))     
                time = self.day_date_time()
                data = { "code": random_code} 
                self.database.child("english_assembly").child("signup_code_deaconness").child(time).set(data) 
                self.id_generated_code_signup.text = "Deaconness :  " + random_code
                self.id_membertype.text = "Select Member"    
                self.id_generate_code.text = "Generate a new code"
                self.id_generate_code.text_color = "#ff0000" 
                self.id_generate_code.md_bg_color = "#ffefea"
                self.id_generate_code.line_color = "#ff0000"
                self.id_generate_code.line_width = 2 
            except:
                Popups().open_popup(title="MISSING COLUMN", text="Something went wrong! \nCheck your network and try again later...", color=[1, 0, 0, 1]) 
        if membertype == "Member":
            try:
                random_code = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + str(random.randint(10, 99)) + str(random.randint(10, 99))     
                time = self.day_date_time()
                data = { "code": random_code} 
                self.database.child("english_assembly").child("signup_code_members").child(time).set(data) 
                self.id_generated_code_signup.text = "Member :  " + random_code
                self.id_membertype.text = "Select Member" 
                self.id_generate_code.text = "Generate a new code"
                self.id_generate_code.text_color = "#ff0000" 
                self.id_generate_code.md_bg_color = "#ffefea"
                self.id_generate_code.line_color = "#ff0000"
                self.id_generate_code.line_width = 2   
            except:
                Popups().open_popup(title="MISSING COLUMN", text="Something went wrong! \nCheck your network and try again later...", color=[1, 0, 0, 1])

    def go_back(self): 
        self.ids.id_membertype.text = "Select Member"
        self.ids.id_generated_code_signup.text = ""
        self.ids.id_generate_code.text = "Generate code"
        self.ids.id_generate_code.text_color = "#ffffff"
        self.ids.id_generate_code.md_bg_color = "#0000ff"
        self.ids.id_generate_code.line_color = "#0000ff"
        self.manager.current = "name_administrationpage"

    def clear(self):
        self.ids.id_membertype.text = "Select Member"



#========================================================================================================================================
#===    2.  AdministrationPage  =========================================================================================================
#========================================================================================================================================
class AdministrationPage(Screen): 
    id_welcome_presibery_member = ObjectProperty(None) 
    id_email_phonenumber = ObjectProperty(None) 
    user_credential = ""

    def login_credential(self, name):  
        self.user_credential = name 
        user_name = self.user_credential["name"]
        user_email = self.user_credential["email"]
        user_phonenumber = self.user_credential["phonenumber"]
        user_statue = self.user_credential["statue"]
        if (user_statue == "elder") or (user_statue == "deacon") or (user_statue == "deaconness"):
            user_name = user_statue + " " + user_name 
        user_name = user_name.title()
        self.ids.id_welcome_presibery_member.text =  user_name 
        self.ids.id_email_phonenumber.text = user_email + "    ||     " + user_phonenumber 


#========================================================================================================================================
#===     AdministrationPage  =========================================================================================================
#========================================================================================================================================

class SignupPage(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    id_signup_fullname  = ObjectProperty(None)
    id_signup_phonenumber  = ObjectProperty(None)
    id_signup_registration_code  = ObjectProperty(None)
    id_signup_email  = ObjectProperty(None)
    id_signup_password  = ObjectProperty(None)
    id_signup_password_confirm  = ObjectProperty(None)
    firebase = pyrebase.initialize_app(firebase_config) 
    auth     = firebase.auth() 
    database = firebase.database() 

    def signup(self):
        signup_fullname = self.id_signup_fullname.text.strip().title()
        signup_phonenumber = self.id_signup_phonenumber.text.strip()
        signup_registration_code = self.id_signup_registration_code.text.strip()
        signup_email = self.id_signup_email.text.strip()
        signup_password = self.id_signup_password.text.strip()
        signup_password_confirm = self.id_signup_password_confirm.text.strip()
        if (len(signup_fullname) == 0) or (len(signup_phonenumber) == 0) or (len(signup_registration_code) == 0) or (len(signup_email) == 0) or (len(signup_password) == 0) or (len(signup_password_confirm) == 0):
            Popups().open_popup(title="MISSING COLUMN", text="All columns must be filled", color=[1, 0, 0, 1])
        else: 
            if signup_password == signup_password_confirm: 
                elders_code, deacons_code, deaconness_code, members_code = [], [], [], []
                try:
                    fetch_elder_codes = self.database.child("english_assembly").child("signup_code_elders").get()   
                    fetch_deacon_codes = self.database.child("english_assembly").child("signup_code_deacons").get()   
                    fetch_deaconness_codes = self.database.child("english_assembly").child("signup_code_deaconness").get()   
                    fetch_member_codes = self.database.child("english_assembly").child("signup_code_members").get()  
                    for elder in fetch_elder_codes.each(): 
                        elders_code.append( elder.val()["code"] ) 
                    for deacon in fetch_deacon_codes.each(): 
                        deacons_code.append( deacon.val()["code"] )
                    for deaconness in fetch_deaconness_codes.each(): 
                        deaconness_code.append( deaconness.val()["code"] )
                    for member in fetch_member_codes.each(): 
                        members_code.append( member.val()["code"] )
                except: 
                    pass 
                all_signin_codes = elders_code + deacons_code + deaconness_code + members_code  
                if signup_registration_code in all_signin_codes:
                    if len(signup_password) < 8:
                        Popups().open_popup(title="WEAK PASSWORD", text="You need a stronger password! At least 8 characters", color=[0, 1, 0, 1])
                    else:
                        try:
                            current_user = self.auth.create_user_with_email_and_password(email=signup_email, password=signup_password)
                            token = (current_user["idToken"]) 
                            self.auth.send_email_verification(token) 
                            if signup_registration_code in elders_code:
                                data = { "fullname": signup_fullname, "phonenumber": signup_phonenumber, "email": signup_email, "statue" : "elder", "token": token, "password": signup_password} 
                                id = str(signup_fullname) + " " + str(signup_phonenumber)
                                self.database.child("english_assembly").child("church_members").child(id).set(data)
                                self.database.child("english_assembly").child("church_elders").child(id).set(data) 
                                self.database.child("english_assembly").child("church_presbytery").child(id).set(data)
                                Popups().open_popup(title="SIGNUP SUCCESSFUL", text="You have successfully signed up. \nVerification link sent to your email.", color=[0, 1, 0, 1])
                            elif signup_registration_code in deacons_code:
                                data = { "fullname": signup_fullname, "phonenumber": signup_phonenumber, "email": signup_email, "statue" : "deacon", "token": token, "password": signup_password}
                                id = str(signup_fullname) + " " + str(signup_phonenumber)
                                self.database.child("english_assembly").child("church_members").child(id).set(data) 
                                self.database.child("english_assembly").child("church_deacon").child(id).set(data) 
                                self.database.child("english_assembly").child("church_presbytery").child(id).set(data)
                                Popups().open_popup(title="SIGNUP SUCCESSFUL", text="You have successfully signed up. \nVerification link sent to your email.", color=[0, 1, 0, 1])
                            elif signup_registration_code in deaconness_code:
                                data = { "fullname": signup_fullname, "phonenumber": signup_phonenumber, "email": signup_email, "statue" : "deaconness", "token": token, "password": signup_password}
                                id = str(signup_fullname) + " " + str(signup_phonenumber)
                                self.database.child("english_assembly").child("church_members").child(id).set(data)
                                self.database.child("english_assembly").child("church_deaconness").child(id).set(data) 
                                self.database.child("english_assembly").child("church_presbytery").child(id).set(data)
                                Popups().open_popup(title="SIGNUP SUCCESSFUL", text="You have successfully signed up. \nVerification link sent to your email.", color=[0, 1, 0, 1])
                            elif signup_registration_code in members_code:
                                data = { "fullname": signup_fullname, "phonenumber": signup_phonenumber, "email": signup_email, "statue" : "member", "token": token, "password": signup_password}
                                id = str(signup_fullname) + " " + str(signup_phonenumber)
                                self.database.child("english_assembly").child("church_members").child(id).set(data)
                                Popups().open_popup(title="SIGNUP SUCCESSFUL", text="You have successfully signed up. \nVerification link sent to your email.", color=[0, 1, 0, 1]) 
                            self.id_signup_fullname.text = ""
                            self.id_signup_phonenumber.text = ""
                            self.id_signup_registration_code.text = ""
                            self.id_signup_email.text = ""
                            self.id_signup_password.text = ""
                            self.id_signup_password_confirm.text = ""
                        except:
                            Popups().open_popup(title="SIGNUP FAILED", text="Something went wrong with the registration!!!", color=[1, 0, 0, 1])
                else: 
                    Popups().open_popup(title="REGISTRATION CODE NEEDED", text="You need a registration code to proceed! \nContact your presbytery member for a code. \nIf you already have one, \nthen check your internet connection", color=[1, 0, 0, 1])
            else:
                Popups().open_popup(title="PASSWORDS DON'T MATCH", text="Passwords do need", color=[1, 0, 0, 1])                 

    def already_exit(self):
        self.manager.current = "name_homepage" 

class SendEmailVerificationScreen(Screen):
    pass


#===================================================================================================================================
#=== 1. HomePage ===================================================================================================================
#===================================================================================================================================
class HomePage(Screen):
    id_login_email = ObjectProperty(None) 
    id_login_password = ObjectProperty(None)

    firebase = pyrebase.initialize_app(firebase_config)
    auth = firebase.auth() 
    database = firebase.database() 

    def church_presbytery_emails(self):
        presbytery_emails = ["zorvepeter28@gmail.com"]
        try:
            presbytery_members = self.database.child("english_assembly").child("church_presbytery").get() 
            dataframe = {}
            for service in presbytery_members.each():
                dataframe[service.key()] = service.val()
            df = pd.DataFrame.from_dict(dataframe, orient="index") 
            length_df = len(df["emailaddress"])
            presbytery_emails = [df["emailaddress"][i] for i in range(length_df)]
        except:
            pass  
        return presbytery_emails  

    def login(self):
        login_email = self.id_login_email.text 
        login_password = self.id_login_password.text    
        if (len(str(login_email)) > 0) and (len(str(login_password)) > 0):  
            try: 
                current_user = self.auth.sign_in_with_email_and_password(email=login_email, password=login_password) 
                token = (current_user["idToken"])
                account_infor = self.auth.get_account_info(token) 
                is_verified = account_infor["users"][0]["emailVerified"]   
                if is_verified: 
                    persons = self.database.child("english_assembly").child("church_members").get() 
                    for person in persons.each():
                        if person.val()["email"] == login_email: 
                            current_user_fullname = person.val()["fullname"]
                            current_user_email = person.val()["email"] 
                            current_user_phonenumber = person.val()["phonenumber"]
                            current_user_statue = person.val()["statue"]
                            data = {"name": current_user_fullname, "email": current_user_email, "phonenumber": current_user_phonenumber, "statue": current_user_statue}
                            if (current_user_statue == "elder") or (current_user_statue == "deacon") or (current_user_statue == "deaconness"):
                                app = MDApp.get_running_app()
                                admin_screen = app.root.get_screen("name_administrationpage")
                                upload_screen = app.root.get_screen("name_upload_information")
                                admin_screen.login_credential(data)
                                upload_screen.login_credential(data)
                                self.manager.current = "name_administrationpage"
                                self.id_login_email.text = ""
                                self.id_login_password.text = ""
                            if (current_user_statue == "member"): 
                                print("login as a member")
                                app = MDApp.get_running_app()
                                member_screen = app.root.get_screen("name_memberprofile")
                                member_screen.login_credential(data)
                                self.manager.current = "name_memberprofile" 
                                self.id_login_email.text = ""
                                self.id_login_password.text = ""
                else:
                    Popups().open_popup(title="EMAIL NOT VERIFIED YET", text="Your account exist, but you have to verify it first. \nVerfication links was sent to your email", color=[1, 0, 0, 1]) 
            except:
                Popups().open_popup(title="SIGNIN FAILED", text="Something went wrong with the signin. \nCheck your email or password or internet connection", color=[1, 0, 0, 1])
        else:
            Popups().open_popup(title="MISSING ITEM", text="Missing email or password or both", color=[1, 0, 0, 1])
    
    def signup(self):
        self.manager.current = "name_signup_homepage"
    
    def forget_password(self):
        Popups().open_popup(title="Unavailable", text="This feature is not imprementated yet", color=[1, 0, 0, 1])
        pass 

# ===================================================================================================================================
class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        return super().build()

MainApp().run() 

#===================================================================================================================================
