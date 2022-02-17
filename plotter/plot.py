
'''
'''

# libraries 
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg 



""" Class to handle making the graphs look aesthetically pleasing 
"""
class PlotAesthetics(): 
    ''' holds properties for plots 
    '''
    def __init__(self, **kwargs): 
        self.color_activity_dict = {'meditate':'#5993A6',
                                    'workout':'#596DA6',
                                    'walk_dog':'#59A692'}   

""" Screen for frequency/distribution viz
"""
class FreqHistPlotScreen(Screen, FileHandler): 
    UI = UI() 
    def __init__(self, **kwargs): 
        super(FreqHistPlotScreen, self).__init__(**kwargs) 

        self.DM = DataManager()  
        self.PA = PlotAesthetics()

        # schedule and run everything after deploying/build 
        Clock.schedule_once(self.plot_freq_hist)

    
    def plot_freq_hist(self, *args): 
        ''' Plots distributio this_activity,n/freq visual for a given activity  
        '''
        this_activity = 'meditate'
        freq_plot, fx = plt.subplots() 
        input = self.load().copy(deep=True)
        sub = input.loc[input[self.activity_col].eq(this_activity), ]

        # round to the nearest second 


        # lets just plot meditation for now
        freq_vals = sub[self.time_col] 
        fx.hist(freq_vals, bins=range(min(freq_vals), max(freq_vals)+1), color=self.UI.hex_main_color)


        # TODO: format y axis ticks 
        fx.set_ylabel(self.time_col)
        fx.set_xlabel('time in seconds')
        fx.set_title('Distribution of time entries for {}'.format(this_activity))
        self.ids.time_dist_fig.add_widget(FigureCanvasKivyAgg(plt.gcf()))
    

""" Screen for Total time bar plot viz 
"""
class TotalsBarPlotScreen(Screen, FileHandler): 

    UI = UI() 
    def __init__(self, **kwargs): 
        super(TotalsBarPlotScreen, self).__init__(**kwargs) 
        self.DM = DataManager()  
        self.PA = PlotAesthetics()

        # schedule and run everything after deploying/build 
        Clock.schedule_once(self.create_bar_plot_total)

    def create_bar_plot_total(self, *args): 
        '''
        '''
        line_plot, bx = plt.subplots() 
        this_input = self.load()
        col_looper = 0 
        for a in this_input[self.activity_col].unique().tolist(): 
            bx.bar(str(a), # groups (x-axis) 
                this_input.loc[this_input[self.activity_col].eq(a), self.time_col], # values 
                0.35, # assigning width 
                label=a,
                color= self.PA.color_activity_dict[a]
            )
            col_looper += 1 
            
        # set labels and plot 
        bx.legend() 
        bx.set_ylabel(self.time_col)
        bx.set_title('Total time grouped by activity')
        self.ids.box_plot_total_fig.add_widget(FigureCanvasKivyAgg(plt.gcf()))



""" Screen for line plots by activity plot viz 
"""
class LinePlotScreen(Screen, FileHandler): 

    UI = UI() 
    def __init__(self, **kwargs):                                      
        super(LinePlotScreen, self).__init__(**kwargs)

        # self.FH = FileHandler()
        self.DM = DataManager() 
        self.PA = PlotAesthetics() 
        

        # schedule and run everything after deploying/build 
        Clock.schedule_once(self.create_line_plot)


    def create_line_plot(self, *args): 
        ''' line plots grouped by activity. to easily visualize trends over time 
        '''
        line_plot, lx = plt.subplots() 

        # loop through each activity 
        plot_df = self.load() #self.DM.fill_activity_data_holes(self.load())
        for a in plot_df[self.activity_col].unique().tolist(): 
            tmp_vals = plot_df.loc[plot_df['activity'].eq(a), ].sort_values(by=self.date_col)

            # group the vals by date; 
            # there may be scenarios where a person may have multiple entries on a given day 
            tmp_vals = tmp_vals.groupby(self.date_col)[self.time_col].sum().reset_index() 

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
class StackedBoxPlotScreen(Screen, FileHandler): 

    UI = UI() 
    def __init__(self, **kwargs):                                      
        super(StackedBoxPlotScreen, self).__init__(**kwargs)
        # self.FH = FileHandler()
        self.DM = DataManager()
        self.PA = PlotAesthetics() 

        # schedule and run everything after deploying/build 
        Clock.schedule_once(self.create_stacked_bar_plot)

    def create_stacked_bar_plot(self, *args): 
        ''' stacked bar plots to visualize proportion of time spent among different activities 
            NOTE: will need to order these in some fashion 
            # need to check for squareness on dates for each activityy 
        '''
        stack_plot, sx = plt.subplots()
        input_df = self.DM.fill_activity_data_holes(self.load())
        activity_list = input_df[self.activity_col].unique().tolist()
        for a in activity_list:
            # subset to activity and sort by date  
            plot_df = input_df.loc[input_df[self.activity_col].eq(a), ].sort_values(by=self.date_col)

            # TODO: add some to data manager
            # groupby and remove duplicate date entries 
            plot_df = plot_df.groupby([self.date_col, self.activity_col])[self.time_col].sum().reset_index() 

            # do some formatting of x-axis (dates) 
            x_vals = plot_df.loc[plot_df[self.activity_col].eq(a), self.date_col].tolist() 
            x_vals = [str(x) for x in x_vals]
            if (activity_list.index(a) == 0): 
                bottom_vals  = np.array(plot_df.loc[plot_df[self.activity_col].eq(a), self.time_col])
                sx.bar(x_vals, # groups (x-axis) 
                    plot_df.loc[plot_df[self.activity_col].eq(a), self.time_col], # values 
                    0.35, # assigning width 
                    label=a,
                    color= self.PA.color_activity_dict[a]
                )
            else: 
                prev_activity = activity_list[activity_list.index(a) - 1] 
                sx.bar(x_vals, # groups (x-axis) 
                    plot_df.loc[plot_df[self.activity_col].eq(a), self.time_col], # values 
                    0.35, # assigning width 
                    bottom= bottom_vals, 
                    label=a,
                    color=self.PA.color_activity_dict[a]
                )
                bottom_vals  = bottom_vals + np.array(plot_df.loc[plot_df[self.activity_col].eq(a), self.time_col])



        # set labels and plot 
        sx.set_ylabel(self.time_col)
        sx.set_title('Total time grouped by day')
        sx.legend() 
        stack_plot.autofmt_xdate() 
        self.ids.stacked_box_fig.add_widget(FigureCanvasKivyAgg(plt.gcf()))
      