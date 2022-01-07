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
import numpy as np 

# date time 
from datetime import datetime, timedelta 



class WindowManager(ScreenManager):
    pass


class UI():
    '''
    '''
    def __init__(self, **kwargs): 
        self.hex_background = '#DADEE2'
        self.hex_main_color = '#5993A6'
        self.hex_complement_color = '#A66C59'
        self.hex_analogous_colors = ['#5993A6', '#596DA6', '#59A692']
        self.hex_white = '#FFFFFF'
    pass 

class MainWindow(Screen):
    ui = UI()
    

class PlotAesthetics(): 
    ''' holds properties for plots 
    '''
    pass


class FileHandler():
    ''' Objects that holds metadata for the main db file 

        Should be called every time app opens up 
    ''' 
    def __init__(self, **kwargs): 
        # file metadata 
        self.filename = 'test_db'
        self.filetype = 'csv'
        self.workdir = 'C:/Users/baba/Documents/phone_apps/tmp_db'

        # file cols 
        self.activity_col = 'activity'
        self.time_col = 'time_elapsed' 
        self.date_col = 'date_inserted'
        self.time_inserted = 'time_inserted'

        # date on start 
        self.date = str(datetime.now().date())
        self.time = str(datetime.now().time())

        # info on input file 
        self.input_file = pd.read_csv('{dir}/{fn}.{ft}'.format(dir=self.workdir, fn=self.filename, ft=self.filetype))
        self.file_cols = self.input_file.columns 
        self.activities = self.input_file['activity'].unique().tolist() 


    def check_acceptable_activities(self, this_activity): 
        '''
        ''' 
        return this_activity.isin(self.activities)
    


class TimerScreen(Screen): 
    number = NumericProperty() 
    def __init__(self, **kwargs): 

        # returns a project object that allows me to refer to the parent class using 'super' 
        super(TimerScreen, self).__init__(**kwargs)
        self.FH = FileHandler() # file metadata 
        
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
        file = pd.read_csv('{dir}/{fn}.{ft}'.format(dir=self.FH.workdir,
                                                        fn=self.FH.filename,
                                                        ft=self.FH.filetype)
        )

        # archive 
        file.to_csv('{dir}/{fn}_{dt}.{ft}'.format(dir=self.FH.workdir, 
                                                  fn=self.FH.filename,
                                                  dt=self.FH.date,
                                                  ft=self.FH.filetype)
        )

        # update & export  
        file.append(entries, ignore_index=True).to_csv('{dir}/{fn}.{ft}'.format(dir=self.FH.workdir,
                                                                                fn=self.FH.filename,
                                                                                ft=self.FH.filetype)
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


class SummStatScreen(Screen): 
    ui = UI() 
    def __init__(self, **kwargs): 

        super(SummStatScreen, self).__init__(**kwargs) 
        self.FH = FileHandler() 

        self.summary_stat_cols = ['mean','highest_time','highest_time_date','longest_streak','dates_of_streak']

    def get_activity_mean(self, this_activity): 
        '''
        '''
        # subset to rows with activity 
        mean = self.FH.input_file.loc[self.FH.input_file['activity'].eq(this_activity), self.FH.time_col].mean()
        return mean 


    def get_activity_max_time_entry(self, this_activity): 
        ''' Most time spent doing activities 
        '''
        sub = self.FH.input_file.loc[self.FH.input_file[self.FH.activity_col].eq(this_activity), [self.FH.date_col, self.FH.time_col]]
        max_val = max(sub[self.FH.time_col])
        max_entry = sub.loc[sub[self.FH.time_col].eq(max_val), ]
        return max_entry


    def get_activity_date_of_max(self, this_activity): 
        '''
        '''
        this_max = self.get_activity_max_time_entry(this_activity)

        # return date(s)
        return this_max[self.FH.date_col].unique().tolist()


    def is_next_day(self, start_date, suggested_next_date):
        ''' Checks that any 2 dates are in consecutive order 
        '''
        pass


    def get_consecutive_streak_by_activity(self, this_activity): 
        ''' Given an activity, return the longest streak(s) and dates of streak(s)
        '''

        date_entries = self.FH.input_file.loc[self.FH.input_file['activity'].eq(this_activity), self.FH.date_col]
        sorted_dates = date_entries.sort_values()

        streak_list = [datetime.strptime(d, '%m/%d/%Y').date() for d in sorted_dates]
        streak_df = pd.DataFrame() 
        streak_df[self.FH.date_col] = streak_list 
        streak_df['group_series'] = (streak_df.diff() > pd.Timedelta('1 day')).cumsum() # NOTE: need better check I think 
 
        counts = streak_df.groupby('group_series').count()['date_inserted'].reset_index()
        highest_streak = max(counts['date_inserted'])
        streak_group = counts.loc[counts['date_inserted'].eq(highest_streak), 'group_series'].unique().tolist()

        # should check if we have 1 or more of same length of streak
        dates_of_streak = streak_df.loc[streak_df['group_series'].isin(streak_group), 'date_inserted'].unique().tolist() 

        # return tuple 
        return (highest_streak, dates_of_streak)


    def date_span_str(self, list_of_dates): 
        ''' Returns a string that specifies the range of dates (i.e 01/01/2021-01/09/2021)
        '''
        return 


    def generate_summary_stats(self): 
        ''' some summary stats: 
                - total time per activity (in text) 
                - avg time per day (for each activity)
                - ave time per day (doing all activities)
                - longest streak 

            should return all stats in table format 
        '''
        stats_df = pd.DataFrame(columns=self.summary_stat_cols) 
        for ac in self.FH.activities: 
            this_mean = self.get_activity_mean(ac)
            this_highest_time = int(self.get_activity_max_time_entry(ac)[self.FH.time_col])
            this_highest_time_date = self.get_activity_max_time_entry(ac)[self.FH.date_col].unique().tolist()
            this_streak_val = self.get_consecutive_streak_by_activity(ac)[0]
            this_streak_dates = self.get_consecutive_streak_by_activity(ac)[1] 
            '''
            tmp_df = pd.DataFrame(data = {'mean':this_mean, 
                                          'highest_time' : this_highest_time, 
                                          'highest_time_date':this_highest_time_date,
                                          'longest_streak':this_streak_val, 
                                          'dates_of_streak' : this_streak_dates})
            stats_df = stats_df.append(tmp_df)  
            '''
        return 


class TotalsBarPlotScreen(Screen): 
    def __init__(self, **kwargs): 
        super(TotalsBarPlotScreen, self).__init__(**kwargs) 

        self.FH = FileHandler()

        # schedule and run everything after deploying/build 
        Clock.schedule_once(self.create_bar_plot_total)

    def create_bar_plot_total(self, *args): 
        '''
        '''
        line_plot, bx = plt.subplots() 
        for a in self.FH.activities: 

            bx.bar(str(a), # groups (x-axis) 
                self.FH.input_file.loc[self.FH.input_file[self.FH.activity_col].eq(a), self.FH.time_col], # values 
                0.35, # assigning width 
                label=a
            )

        # set labels and plot 
        bx.set_ylabel(self.FH.time_col)
        bx.set_title('Total time grouped by activity')
        bx.legend() 
        self.ids.box_plot_total_fig.add_widget(FigureCanvasKivyAgg(plt.gcf()))



class LinePlotScreen(Screen): 
    def __init__(self, **kwargs):                                      
        super(LinePlotScreen, self).__init__(**kwargs)

        self.FH = FileHandler()

        # schedule and run everything after deploying/build 
        Clock.schedule_once(self.create_line_plot)

    def parse_data(self, x_col, y_col):
        ''' This method handles parsing the db and returning the parameters of interest. 

            Returns: 
                dictionary 
        '''
        # get cols 
        activities = self.FH.input_file['activity'].unique().tolist() 

        # create tuples for each unique activity-data_point 
        tuple_dict = dict() 
        for a in activities: 
            # subset to activity 
            this_activity = self.FH.input_file.loc[self.FH.input_file['activity'].eq(a), ]

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

    def create_line_plot(self, *args): 
        ''' line plots grouped by activity. to easily visualize trends over time 
        '''
        line_plot, lx = plt.subplots() 

        # loop through each activity 
        for a in self.FH.activities: 
            tmp_vals = self.FH.input_file.loc[self.FH.input_file['activity'].eq(a), ]
            plt.plot(tmp_vals['date_inserted'], tmp_vals['time_elapsed'], label=a)

        lx.legend() 
        lx.set_ylabel('Time (seconds)')
        lx.set_xlabel('Date')
        lx.set_title('Time spent over time')
        self.ids.line_plot_fig.add_widget(FigureCanvasKivyAgg(plt.gcf()))


class StackedBoxPlotScreen(Screen): 
    def __init__(self, **kwargs):                                      
        super(StackedBoxPlotScreen, self).__init__(**kwargs)
        self.FH = FileHandler()

        # schedule and run everything after deploying/build 
        #Clock.schedule_once(self.create_stacked_bar_plot)

    def create_stacked_bar_plot(self, *args): 
        ''' stacked bar plots to visualize proportion of time spent among different activities 
            NOTE: will need to order these in some fashion 
            # need to check for squareness on dates for each activityy 
        '''
        stack_plot, sx = plt.subplots()
        for a in self.FH.activities: 
            if (self.FH.activities.index(a) == 0): 
                bottom_vals  = np.array(self.FH.input_file.loc[self.FH.input_file[self.FH.activity_col].eq(a), self.FH.time_col])
                sx.bar(self.FH.input_file.loc[self.FH.input_file[self.FH.activity_col].eq(a), self.FH.date_col].tolist(), # groups (x-axis) 
                    self.FH.input_file.loc[self.FH.input_file[self.FH.activity_col].eq(a), self.FH.time_col], # values 
                    0.35, # assigning width 
                    label=a
                )
            else: 
                prev_activity = self.FH.activities[self.FH.activities.index(a) - 1] 
                sx.bar(self.FH.input_file.loc[self.FH.input_file[self.FH.activity_col].eq(a), self.FH.date_col].tolist(), # groups (x-axis) 
                    self.FH.input_file.loc[self.FH.input_file[self.FH.activity_col].eq(a), self.FH.time_col], # values 
                    0.35, # assigning width 
                    bottom= bottom_vals, 
                    label=a
                )
                bottom_vals  = bottom_vals + np.array(self.FH.input_file.loc[self.FH.input_file[self.FH.activity_col].eq(a), self.FH.time_col])


        # set labels and plot 
        sx.set_ylabel(self.FH.time_col)
        sx.set_title('Total time grouped by day')
        sx.legend() 
        self.ids.stacked_box_fig.add_widget(FigureCanvasKivyAgg(plt.gcf()))

         
         
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