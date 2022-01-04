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

class MainWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class TimerScreen(Screen): 
    number = NumericProperty() 

    def __init__(self, **kwargs): 

        # returns a project object that allows me to refer to the parent class using 'super' 
        super(TimerScreen, self).__init__(**kwargs)
        
        # file metadata 
        self.filename = 'test_db'
        self.filetype = 'csv'
        self.workdir = 'C:/Users/baba/Documents/phone_apps/tmp_db'
        
        # date on start 
        self.date = str(datetime.now().date())
        self.time = str(datetime.now().time())

        # file cols 
        self.activity_col = 'activity'
        self.time_col = 'time_elapsed' 
        self.date_col = 'date_inserted'
        self.time_inserted = 'time_inserted'

        """ don't need this snipet as of now 
        # create clock and increment time 
        # NOTE: .1 = 1 sec
        Clock.schedule_interval(self.increment_time, .1) 

        self.increment_time(0) 
        """

    def get_entries(self): 
        '''
        '''
        pass 


    def update_and_save(self, entries): 
        ''' updates .csv file or db by appending new values 

            file : .csv 
                - temporary file meant to migrate to a db 

            entries : dict 
                -  { col : entry } value pair for each column in the db 

            NOTE: this will need to be updated once ready for android deployment 
        '''
        this_date = str(datetime.now().date())
        file = pd.read_csv('{dir}/{fn}.{ft}'.format(dir=self.workdir,
                                                        fn=self.filename,
                                                        ft=self.filetype)
        )

        # archive 
        file.to_csv('{dir}/{fn}_{dt}.{ft}'.format(dir=self.workdir, 
                                                  fn=self.filename,
                                                  dt=self.date,
                                                  ft=self.filetype)
        )

        # update & export  
        file.append(entries, ignore_index=True).to_csv('{dir}/{fn}.{ft}'.format(dir=self.workdir,
                                                                                fn=self.filename,
                                                                                ft=self.filetype)
        )


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

        # file metadata 
        self.filename = 'test_db'
        self.filetype = 'csv'
        self.workdir = 'C:/Users/baba/Documents/phone_apps/tmp_db'

        # file cols 
        self.activity_col = 'activity'
        self.time_col = 'time_elapsed' 
        self.date_col = 'date_inserted'
        self.time_inserted = 'time_inserted'


        # info on input file 
        self.input_file = pd.read_csv('{dir}/{fn}.{ft}'.format(dir=self.workdir, fn=self.filename, ft=self.filetype))
        self.file_cols = self.input_file.columns 
        self.activites = self.input_file['activity'].unique().tolist() 

        # schedule and run everything after deploying/build 
        Clock.schedule_once(self.create_stacked_bar_plot)

    def parse_data(self, x_col, y_col):
        ''' This method handles parsing the db and returning the parameters of interest. 

            Returns: 
                dictionary 
        '''
        # get cols 
        activities = self.input_file['activity'].unique().tolist() 

        # create tuples for each unique activity-data_point 
        tuple_dict = dict() 
        for a in activities: 
            # subset to activity 
            this_activity = self.input_file.loc[self.input_file['activity'].eq(a), ]

            # create tuple for each entry 
            this_activity['xy_vals'] = list(zip(this_activity[x_col], this_activity[y_col])) # note: these colu
            xy_vals = this_activity['xy_vals'].unique().tolist() 

            # save to dict 
            tuple_dict[a] = xy_vals
        return tuple_dict    


    def format_data(): 
        ''' format the data on build so it's ready for visualizations 
        '''
        pass 


    def create_stacked_bar_plot(self, *args): 
        '''
        '''
        stack_plot, sx = plt.subplots()
        sx.bar(self.input_file.loc[self.input_file['activity'].eq('meditate'), self.date_col].tolist(), # groups (x-axis) 
               self.input_file.loc[self.input_file['activity'].eq('meditate'), self.time_col].tolist(), # values 
               0.35, # assigning width 
               label='meditate' 
        )
        sx.bar(self.input_file.loc[self.input_file['activity'].eq('workout'), self.date_col].tolist(),
               self.input_file.loc[self.input_file['activity'].eq('workout'), self.time_col].tolist(),
               0.35,
               bottom=self.input_file.loc[self.input_file['activity'].eq('meditate'), self.time_col].tolist(),
               label='workout'
        )

        sx.set_ylabel(self.time_col)
        sx.set_title('Time by activity')
        sx.legend() 
        self.ids.stat_fig.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def create_line_plot(self, *args): 
        '''
        '''
        # loop through each activity 
        for a in self.activites: 
            tmp_vals = self.input_file.loc[self.input_file['activity'].eq(a), ]
            plt.plot(tmp_vals['date_inserted'], tmp_vals['time_elapsed'], label=a)

        plt.legend() 
        self.ids.stat_fig.add_widget(FigureCanvasKivyAgg(plt.gcf()))
         
         
kv = Builder.load_file('main.kv')
class MyMainApp(App):
    def parse_data(): 
        '''
        '''
        pass 

    def build(self): 
        return kv
        


if __name__ == "__main__":
    MyMainApp().run()