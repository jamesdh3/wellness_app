

# -- Libraries 

# kivy stuff 
from kivy.app import App  
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import Sound, SoundLoader
import matplotlib.dates as mdates
from kivy.properties import NumericProperty # used when creating a EventDispatcher
from kivy.uix.boxlayout import BoxLayout # arranges boxes
from kivy.clock import Clock # allows me to schedule a function in the future  
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg 
from kivy.properties import ObjectProperty


# plotting libraries 
import matplotlib.pyplot as plt 
from matplotlib.dates import DateFormatter


# we're going to want to use some pandas for data manipulation and viz 
# NOTE: will need to look at how ggplot and phone apps work together 
import pandas as pd 
import numpy as np 

# handling dates  
from datetime import datetime, timedelta 
import time 

# creating calendar viz 
import calendar 


""" Screen manager and aesthetics of screens 
"""
class WindowManager(ScreenManager):
    pass


""" Holds aesthetic settings for UI 
"""
class UI():
    '''
    '''
    #audio_dir = 'C:/Users/baba/Documents/phone_apps/audio'


    def __init__(self, **kwargs): 
        self.hex_background = '#DADEE2'
        self.hex_main_color = '#5993A6'
        self.hex_complement_color = '#A66C59'
        self.hex_analogous_colors = ['#5993A6', '#596DA6', '#59A692']
        self.hex_palette = ['#5993A6', '#5888AA', '#667BA8', '#7A6B9D', '#8C5A88', '#974B6B'] # will need to fix this 
        self.hex_white = '#FFFFFF'

        self.audio_dir = 'C:/Users/baba/Documents/phone_apps/audio'
        self.onpress_button_sound_fpath = '{}/droplet1.wav'.format(self.audio_dir)
        self.onrelease_button_sound_fpath = '{}/droplet2.wav'.format(self.audio_dir) 
        self.back_button_sound_fpath = '{}/droplet3.wav'.format(self.audio_dir)
        self.start_timer = '{}/start_timer.wav'.format(self.audio_dir) 
        self.start_timer_sound = SoundLoader.load(self.start_timer)

        # stuff for summs/calendar view 
        self.week_days = 'Sun Mon Tue Wed Thu Fri Sat'.split()
        self.month_names = '''January February March April
                              May June July August
                              September October November December'''.split()

    def play_button_press(self): 
        sound = SoundLoader.load(self.onpress_button_sound_fpath)
        sound.play() 
    
    def play_button_release(self): 
        sound = SoundLoader.load(self.onrelease_button_sound_fpath)
        sound.play() 

    def play_button_back(self): 
        sound = SoundLoader.load(self.back_button_sound_fpath)
        sound.play() 
    
    def play_button_start_timer(self): 
        '''
        '''
        if self.start_timer_sound.state == 'play':
            self.start_timer_sound.stop()
        if (self.start_timer_sound.state == 'stop'): 
            self.start_timer_sound.play() 


""" Any logic to handle the main screen when a user logs in the app 
"""
class MainWindow(Screen):
    ui = UI()


""" Holds information about the file/database and that metadata info
"""               
class FileHandler():
    ''' Objects that holds metadata for the main db file 

        Should be called every time app opens up 
    ''' 
    # file metadata 
    filename = 'test_db'
    filetype = 'csv'
    workdir = 'C:/Users/baba/Documents/phone_apps/tmp_db'

    # file cols 
    activity_col = 'activity'
    time_col = 'time_elapsed' 
    date_col = 'date_inserted'
    time_inserted = 'time_inserted'
    primary_key = 'entry_id'

    # date on start 
    date = str(datetime.now().date())
    time = str(datetime.now().time())

    UI = UI() 
    def __init__(self, **kwargs): # note could initialize on file_name s
        # info on input file 
        self.input_file = pd.read_csv('{dir}/{fn}.{ft}'.format(dir=self.workdir, fn=self.filename, ft=self.filetype), parse_dates=[self.date_col])
        self.input_file = self.format_date_axis() 

        self.file_cols = self.input_file.columns 
        self.activities = self.list_activities(self.input_file) 

        color_map = self._assign_activity_colors() 

    def _assign_activity_colors(self): 
        ''' creates a dictionary where key value is an activity; and value 
            is 
        '''
        # order activities by time_elapsed 
        act_list = self.input_file.sort_values(by=self.time_col)[self.activity_col].unique().tolist() 

        # loop through each activity and assign color 
        color_dict = dict() 
        for act in self.activities: 
            color_dict[act] = self.UI.hex_palette[act_list.index(act)]
        return color_dict


    def check_acceptable_activities(self, this_activity): 
        '''
        ''' 
        pass 
    
    def format_date_axis(self): 
        ''' for plotting purposes - remove the time stamp from date-inserted  
        '''
        self.input_file[self.date_col] = self.input_file[self.date_col].dt.date
        return self.input_file 

    def datetime_to_str(self, df): 
        ''' converts a datetime.date column into str format
        '''
        assert self.date_col in df.columns, '{} is not present in the data!'.format(self.date_col)

        # grab a list of entries 
        date_entry_list = df[self.date_col].tolist() 

        # for each entry, convert to str 
        date_str = [str(d) for d in date_entry_list]
        
        # replace and return 
        df[self.date_col] = date_str 
        return df

    def list_activities(self, input_df): 
        '''
        '''
        list_act = input_df[self.activity_col].unique().tolist()
        act_no_nans = [x for x in list_act if str(x) != 'nan'] 
        return act_no_nans 


""" Any and all data formatting done to input data/database
"""
class DataManager(): 
    ''' Object that holds operations that are done on the input file.

        NOTE: will be needed for all plot/visualization classes 
    '''

    def __init__(self, **kwargs): 
        self.FH = FileHandler() 
        pass

    def is_next_date(date_list): 
        ''' compares 2 dates, and returns True if the second entry is the next day of the first entry 
        '''
        return (date_list[0] + datetime.timedelta(days=1)) == (date_list[1])


    def create_date_spans(): 
        '''
        '''
        pass 


    def collapse(self, df, groupby_cols, agg_col, agg_name='sum'): 
        ''' Does a custom aggregation for given set of columns

            Input:
                df : DataFrame
                    pandas data.frame
                groupby_cols : list
                    identifier columns you want to aggregate over
                agg_col : str
                    name of column you want to aggregate 
                agg_name : string (default='sum')
                    specify how you want to aggregate a certain column 
                    possible vals: ['sum']
            
            Output: 
                pandas dataframe
        '''
        pass 


    def days_diff_list(self, day1, day2): 
        ''' Takes 2 datetimes and returns a list of all dates in between (inclusive)
        '''
        delta = day2 - day1 
        list_of_dates = []
        for i in range(delta.days + 1): 
            day = day1 + timedelta(days=i) 
            list_of_dates += [day] 
        return list_of_dates 


    def fill_activity_data_holes(self): 
        ''' Fills in gaps of dates with 0 time elapsed (any date between min and max date)

            NOTE: could generalize and ask for column of interest as well 
            NOTE: should take some input df 
        '''

        # get dates and time for activity 
        act_df = self.FH.input_file[[self.FH.activity_col, self.FH.time_col, self.FH.date_col]].reset_index()
        act_df[self.FH.date_col] = act_df[self.FH.date_col].dt.date

        # get unique dates; and number of entries 
        min_date = act_df[self.FH.date_col].min()
        max_date = act_df[self.FH.date_col].max()

        # get the days between each element in the list 
        date_list = self.days_diff_list(min_date, max_date)

        # if dates aren't in the orig_dates, insert and create another row with 0 time_elapsed 
        for a in self.FH.activities:
            this_act = act_df.loc[act_df[self.FH.activity_col].eq(a), ] 
            orig_dates = this_act[self.FH.date_col].unique().tolist()
            for this_date in date_list: 
                if (this_date not in orig_dates): 
                    new_entry = {self.FH.activity_col : [str(a)],  
                                 self.FH.date_col : [this_date], 
                                 self.FH.time_col : [0]
                                }
                    act_df = act_df.append(pd.DataFrame(new_entry))
        return act_df


""" Class to handle making the graphs look aesthetically pleasing 
"""
class PlotAesthetics(): 
    ''' holds properties for plots 
    '''
    def __init__(self, **kwargs): 
        self.color_activity_dict = {'meditate':'#5993A6',
                                    'workout':'#596DA6',
                                    'walk_dog':'#59A692'}    

""" Screen for stopwatch/timer 
"""
class TimerScreen(Screen): 
    number = NumericProperty() 
    def __init__(self, **kwargs): 
        # returns a project object that allows me to refer to the parent class using 'super' 
        super(TimerScreen, self).__init__(**kwargs)
        self.FH = FileHandler() # file metadata 
        self.UI = UI() 

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
        # make sure to unschedule any future jobs 
        Clock.unschedule(self.increment_time) 
        Clock.unschedule(self.UI.play_button_start_timer)

        # play the start timer sound 
        self.UI.play_button_start_timer()

        # schedule jobs to increment time and play sound 
        Clock.schedule_interval(self.increment_time, .1) 
        Clock.schedule_interval(self.UI.play_button_start_timer, 10)

    def stop(self): 
        Clock.unschedule(self.increment_time) 
        Clock.unschedule(self.UI.play_button_start_timer)

        # stop any bell sounds 
        self.UI.start_timer_sound.stop()

    def datestamp(self): 
        return datetime.now() 


""" Class for handling Calendar viz 

pulled code from this repo - https://github.com/meta4/mplcal

will adjust as needed:
- ability to color coordinate with some events and colors 

NOTE: add some suggested PRs 
"""
class CalendarViz(): 
    UI = UI()
    FH = FileHandler()

    def __init__(self, year, month):
        self.year = year
        self.month = month
        self.cal = calendar.monthcalendar(year+1, month) # off by 1 - need to look into 
        
        
        # monthcalendar creates a list of lists for each week
        # Save the events data in the same format
        self.events = [[[] for day in week] for week in self.cal]

    def _monthday_to_index(self, day):
        'The index of the day in the list of lists'
        for week_n, week in enumerate(self.cal):
            try:
                i = week.index(day)
                return week_n, i
            except ValueError:
                pass
         # couldn't find the day
        raise ValueError("There aren't {} days in the month".format(day))

    def add_event(self, day, event_str):
        ''' insert a string into the events list for the specified day. will want to color this
        '''
        week, w_day = self._monthday_to_index(day)
        self.events[week][w_day].append(event_str)

    def add_activity_event(self, day, this_activity): 
        ''' this method will take a calendar object insert strings or images for a specifified date.
        '''
        week, w_day = self._monthday_to_index(day)
        self.events[week][w_day].append(this_activity)
        

    def show(self):
        ''' create the calendar
        '''
        x = [0,1]
        y = [1,1]
        y2 = [0,0]

        # test case - say we have 2 qactivities for a given day, create a blue and orange square for a given day 
        acts = ['a1', 'a2']

        f, axs = plt.subplots(len(self.cal), 7, sharex=True, sharey=True) # create the list of lists of subplots 

        # set backgrouund color of calendar; match it with the rest of the UI 
        f.set_facecolor(self.UI.hex_background)

        # load in input data.frame that has activiity info 
        df = self.FH.datetime_to_str(self.FH.input_file.copy(deep=True))

        # loop through the list of lists, creating text and activity events 
        for week, ax_row in enumerate(axs):
            for week_day, ax in enumerate(ax_row):
                ax.set_xticks([])
                ax.set_yticks([])
                if self.cal[week][week_day] != 0:
                    ax.text(.02, .98,
                            str(self.cal[week][week_day]),
                            verticalalignment='top',
                            horizontalalignment='left')

                    # check which activity events are needed for a given day 
                    sub_df = df.loc[df[self.FH.date_col].eq('{yr}-0{mt}-{d}'.format(yr=self.year, mt=self.month, d=self.cal[week][week_day])), ]
                    day_of_acts = sub_df[self.FH.activity_col].unique().tolist() 

                    # calculate how many columms and loop through the length 
                    num_cols = len(day_of_acts)

                # add any additional events/text to the calendar      
                contents = "\n".join(self.events[week][week_day])

                # the data points should be determined based on how many activities exist for a given day 
                #for this_act in day_of_acts: 
                #    pass 
                ax.plot(x, y, color='white') 
                ax.plot(x, y2, color='white')
                ax.fill_between([0,0.5], y, y2, where=(y2<=y))
                ax.fill_between([0.5,1], y, y2, where= (y2<=y)) 
                
                ax.text(.03, .85, contents,
                        verticalalignment='top',
                        horizontalalignment='left',
                        fontsize=9)

        # use the titles of the first row as the weekdays
        for n, day in enumerate(self.UI.week_days):
            axs[0][n].set_title(day)


""" Screen for summary stats 
"""
class SummStatScreen(Screen): 
    ui = UI() 
    dm = DataManager()
 

    def __init__(self, **kwargs): 
        super(SummStatScreen, self).__init__(**kwargs) 
        self.FH = FileHandler() 

        self.summary_stat_cols = ['mean','highest_time','highest_time_date','longest_streak','dates_of_streak']


        # schedule any plots and viz stuff 
        Clock.schedule_once(self.display_calendar)


    def display_calendar(self, this_activity): 
        '''
        '''
        calv = CalendarViz(2022, 1)
        # calv.add_activity_event(1, 'first date')
        #  calv.add_activity_event(2, 'this is James. he likes to program once in awhile, but he really wanted to be a dancef.')
        calv.show() 


        self.ids.cal_summary.add_widget(FigureCanvasKivyAgg(plt.gcf()))


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

            NOTE: if there are more than 1 streak, return a list of lists
        '''

        date_entries = self.FH.input_file.loc[self.FH.input_file['activity'].eq(this_activity), self.FH.date_col].drop_duplicates()
        sorted_dates = date_entries.sort_values()

        streak_list = [datetime.strptime(str(d), '%Y-%m-%d').date() for d in sorted_dates]
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

    def get_longest_streak_dict(self): 
        '''
        '''
        # get all activities, loop and append to dict 
        activity_dict = dict() 
        for act in self.FH.activities: 
            activity_dict[act] = self.get_consecutive_streak_by_activity(act)[0]
        return activity_dict 

    def get_longest_streak_dates(self, return_span=True): 
        ''' returns dictionary where keys are activity names and values are 
            dates that determine which dates contained the longest streak
        '''
            
        def _create_date_span(date_list): 
            ''' given a list of dates, create a date span
                input: [datetime.date(2022, 1,3), datetime.date(2022,1,4), datetime.date(2022,1,5)]
            return: '2022/01/03 - 2022/01/05'

            NOTE: at the moment, this is going to assume there are no gap dates in the input 
            '''
            pass


        activity_dict = dict() 
        for act in self.FH.activities: 
            # get dates and convert to a str of dates 
            streak_dates =  self.get_consecutive_streak_by_activity(act)[1]
            str_streak_dates = [str(s) for s in streak_dates]

            activity_dict[act] = str_streak_dates 

        # either return all dates in the streak or the date span 
        if return_span: 
            return _create_date_span([])
        else: 
            return 

    



    def date_span_str(self, list_of_dates): 
        ''' Returns a string that specifies the range of dates (i.e 01/01/2021-01/09/2021)
        '''
        return 


    def calculate_std(self, this_activity): 
        '''
        '''
        std_dev = self.FH.input_file.loc[self.FH.input_file['activity'].eq(this_activity), self.FH.time_col].std()
        return std_dev 


    def generate_summary_stats(self): 
        ''' some summary stats: 
                - total time per activity (in text) 
                - avg time per day (for each activity)
                - ave time per day (doing all activities)
                - longest streak 
                - percentage of days elapsed in time frame 
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


""" Screen for selecting viz 
"""
class VizSelectScreen(Screen): 
    UI = UI() 
    def __init__(self, **kwargs): 
        super(VizSelectScreen, self).__init__(**kwargs)
    pass 


""" Screen for frequency/distribution viz
"""
class FreqHistPlotScreen(Screen): 
    UI = UI() 
    def __init__(self, **kwargs): 
        super(FreqHistPlotScreen, self).__init__(**kwargs) 

        self.FH = FileHandler()
        self.DM = DataManager()  
        self.PA = PlotAesthetics()

        # schedule and run everything after deploying/build 
        # Clock.schedule_once(self.plot_freq_hist)

    
    def plot_freq_hist(self, *args): 
        ''' Plots distributio this_activity,n/freq visual for a given activity  
        '''
        this_activity = 'meditate'
        freq_plot, fx = plt.subplots() 

        input = self.DM.fill_activity_data_holes()
        sub = input.loc[input[self.FH.activity_col].eq(this_activity), ]

        # round to the nearest second 


        # lets just plot meditation for now
        freq_vals = sub[self.FH.time_col] 
        fx.hist(freq_vals, bins=range(min(freq_vals), max(freq_vals)+1), color=self.UI.hex_main_color)


        # TODO: format y axis ticks 
        fx.set_ylabel(self.FH.time_col)
        fx.set_xlabel('time in seconds')
        fx.set_title('Distribution of time entries for {}'.format(this_activity))
        self.ids.time_dist_fig.add_widget(FigureCanvasKivyAgg(plt.gcf()))
    

""" Screen for Total time bar plot viz 
"""
class TotalsBarPlotScreen(Screen): 

    UI = UI() 
    def __init__(self, **kwargs): 
        super(TotalsBarPlotScreen, self).__init__(**kwargs) 

        self.FH = FileHandler()
        self.DM = DataManager()  
        self.PA = PlotAesthetics()

        # schedule and run everything after deploying/build 
        # Clock.schedule_once(self.create_bar_plot_total)

    def create_bar_plot_total(self, *args): 
        '''
        '''
        line_plot, bx = plt.subplots() 
        this_input = self.DM.fill_activity_data_holes()
        col_looper = 0 
        for a in self.FH.activities: 
            bx.bar(str(a), # groups (x-axis) 
                this_input.loc[this_input[self.FH.activity_col].eq(a), self.FH.time_col], # values 
                0.35, # assigning width 
                label=a,
                color= self.PA.color_activity_dict[a]
            )
            col_looper += 1 
            
        # set labels and plot 
        bx.legend() 
        bx.set_ylabel(self.FH.time_col)
        bx.set_title('Total time grouped by activity')
        self.ids.box_plot_total_fig.add_widget(FigureCanvasKivyAgg(plt.gcf()))


""" Screen for line plots by activity plot viz 
"""
class LinePlotScreen(Screen): 

    UI = UI() 
    def __init__(self, **kwargs):                                      
        super(LinePlotScreen, self).__init__(**kwargs)

        self.FH = FileHandler()
        self.DM = DataManager() 
        self.PA = PlotAesthetics() 
        

        # schedule and run everything after deploying/build 
        # Clock.schedule_once(self.create_line_plot)


    def create_line_plot(self, *args): 
        ''' line plots grouped by activity. to easily visualize trends over time 
        '''
        line_plot, lx = plt.subplots() 

        # loop through each activity 
        plot_df = self.DM.fill_activity_data_holes()
        for a in self.FH.activities: 
            tmp_vals = plot_df.loc[plot_df['activity'].eq(a), ].sort_values(by=self.FH.date_col)

            # group the vals by date; 
            # there may be scenarios where a person may have multiple entries on a given day 
            tmp_vals = tmp_vals.groupby(self.FH.date_col)[self.FH.time_col].sum().reset_index() 

            x_vals = [str(x) for x in tmp_vals['date_inserted'].unique().tolist()]
            y_vals = tmp_vals['time_elapsed'].tolist()
            lx.plot(x_vals, y_vals, label=a, color=self.PA.color_activity_dict[a])

        lx.legend() 
        lx.set_ylabel('Time (seconds)')
        lx.set_xlabel('Date')
        lx.set_title('Time spent over time')

        line_plot.autofmt_xdate() 
        # lx.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
        self.ids.line_plot_fig.add_widget(FigureCanvasKivyAgg(plt.gcf()))


""" Screen for proportion plots and bar plot by activity per day  
"""
class StackedBoxPlotScreen(Screen): 

    UI = UI() 
    def __init__(self, **kwargs):                                      
        super(StackedBoxPlotScreen, self).__init__(**kwargs)
        self.FH = FileHandler()
        self.DM = DataManager()
        self.PA = PlotAesthetics() 

        # schedule and run everything after deploying/build 
        # Clock.schedule_once(self.create_stacked_bar_plot)

    def create_stacked_bar_plot(self, *args): 
        ''' stacked bar plots to visualize proportion of time spent among different activities 
            NOTE: will need to order these in some fashion 
            # need to check for squareness on dates for each activityy 
        '''
        stack_plot, sx = plt.subplots()
        input_df = self.DM.fill_activity_data_holes()
        for a in self.FH.activities:
            # subset to activity and sort by date  
            plot_df = input_df.loc[input_df[self.FH.activity_col].eq(a), ].sort_values(by=self.FH.date_col)

            # TODO: add some to data manager
            # groupby and remove duplicate date entries 
            plot_df = plot_df.groupby([self.FH.date_col, self.FH.activity_col])[self.FH.time_col].sum().reset_index() 

            # do some formatting of x-axis (dates) 
            x_vals = plot_df.loc[plot_df[self.FH.activity_col].eq(a), self.FH.date_col].tolist() 
            x_vals = [str(x) for x in x_vals]
            if (self.FH.activities.index(a) == 0): 
                bottom_vals  = np.array(plot_df.loc[plot_df[self.FH.activity_col].eq(a), self.FH.time_col])
                sx.bar(x_vals, # groups (x-axis) 
                    plot_df.loc[plot_df[self.FH.activity_col].eq(a), self.FH.time_col], # values 
                    0.35, # assigning width 
                    label=a,
                    color= self.PA.color_activity_dict[a]
                )
            else: 
                prev_activity = self.FH.activities[self.FH.activities.index(a) - 1] 
                sx.bar(x_vals, # groups (x-axis) 
                    plot_df.loc[plot_df[self.FH.activity_col].eq(a), self.FH.time_col], # values 
                    0.35, # assigning width 
                    bottom= bottom_vals, 
                    label=a,
                    color=self.PA.color_activity_dict[a]
                )
                bottom_vals  = bottom_vals + np.array(plot_df.loc[plot_df[self.FH.activity_col].eq(a), self.FH.time_col])



        # set labels and plot 
        sx.set_ylabel(self.FH.time_col)
        sx.set_title('Total time grouped by day')
        sx.legend() 
        stack_plot.autofmt_xdate() 
        self.ids.stacked_box_fig.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        

""" load the kivy file and build the app 
"""        
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