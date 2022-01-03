from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder 
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg 
import matplotlib.pyplot as plt 


# plot stuff 
# random data points 
x = [1,2,3,4] 
y = [5,10,15,20]

plt.plot(x,y)

plt.ylabel('Y axis')
plt.xlabel('X axis')


class Demo(FloatLayout): 
    def __init__(self, **kwargs): 
        super().__init__(**kwargs) 
        box = self.ids.box 
        box.add_widget(FigureCanvasKivyAgg(plt.gcf())) 


class Main(App): 
    def build(self): 
        Builder.load_file('layout_test.kv')
        return Demo() 

Main().run() 