from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty # used when creating a EventDispatcher
from kivy.uix.boxlayout import BoxLayout # arranges boxes
from kivy.clock import Clock # allows me to schedule a function in the future  

# we're going to want to use some pandas for data manipulation and viz 
# NOTE: will need to look at how ggplot and phone apps work together 
import pandas as pd 

# date time 
from datetime import datetime 

class MainWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class TimerScreen(Screen): 
    number = NumericProperty() 

    def __init__(self, **kwargs): 

        # returns a project object that allows me to refer to the parent class using 'super' 
        super(TimerScreen, self).__init__(**kwargs)
        self.activity_col = 'activity'
        self.time_col = 'time_elapsed' 
        self.date_col = 'date_inserted'
        """
        # create clock and increment time 
        # NOTE: .1 = 1 sec
        Clock.schedule_interval(self.increment_time, .1) 

        self.increment_time(0) 
        """

    def increment_time(self, interval): 
        '''
        Used to increment time 
        '''
        self.number += .1 

    # start button     
    def start(self): 
        Clock.unschedule(self.increment_time) 
        Clock.schedule_interval(self.increment_time, .1) 

    def stop(self): 
        Clock.unschedule(self.increment_time) 

    def datestamp(self): 
        return datetime.now() 


# load in aesthetic settings 
kv = Builder.load_file("kv_homepage.kv")


class MyMainApp(App):
    def update_and_save(self, entries): 
        ''' updates .csv file or db by appending new values 

            file : .csv 
                - temporary file meant to migrate to a db 

            entries : dict 
                -  { col : entry } value pair for each column in the db 
        '''
        date_stamp = datetime.now() 

        file = pd.read_csv('C:/Users/baba/Documents/phone_apps/tmp_db/test_db.csv')

        # update & export  
        file.append(entries, ignore_index=True).to_csv('C:/Users/baba/Documents/phone_apps/tmp_db/test_db_updated.csv')


    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()