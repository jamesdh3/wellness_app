from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty # used when creating a EventDispatcher
from kivy.uix.boxlayout import BoxLayout # arranges boxes
from kivy.clock import Clock # allows me to schedule a function in the future  
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg 
import matplotlib.pyplot as plt 
from kivy.properties import ObjectProperty

# we're going to want to use some pandas for data manipulation and viz 
# NOTE: will need to look at how ggplot and phone apps work together 
import pandas as pd 

# date time 
from datetime import datetime 

# plot stuff 
# random data points 
x = [1,2,3,4] 
y = [5,10,15,20]

plt.plot(x,y) 

plt.ylabel('Y axis')
plt.xlabel('X axis')

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

    def update_and_save(self, entries): 
        ''' updates .csv file or db by appending new values 

            file : .csv 
                - temporary file meant to migrate to a db 

            entries : dict 
                -  { col : entry } value pair for each column in the db 

            NOTE: this will need to be updated once ready for android deployment 
        '''
        date_stamp = datetime.now() 
        file = pd.read_csv('C:/Users/baba/Documents/phone_apps/tmp_db/test_db.csv')

        # update & export  
        file.append(entries, ignore_index=True).to_csv('C:/Users/baba/Documents/phone_apps/tmp_db/test_db_updated.csv')


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


class StatScreen(Screen): 
    def __init__(self, **kwargs):                                      
        super(StatScreen, self).__init__(**kwargs)
        input_file = pd.read_csv('C:/Users/baba/Documents/phone_apps/tmp_db/test_db_graph.csv')
        file_cols = input_file.columns 
        Clock.schedule_once(self.plot)

    def parse_data(self): 
        pass
            

    def create_plot(self): 
        pass

    def plot(self, *args): 
        
        self.ids.stat_fig.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    
    
         
kv = Builder.load_file('main.kv')
class MyMainApp(App):
    def build(self): 
        return kv
        


if __name__ == "__main__":
    MyMainApp().run()