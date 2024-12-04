from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock

from Parser import NumericStringParser


class Function(Widget):
    scale : float = 16
    detail : float = 4

    line_width : int= 3
    color : tuple[float]= (.8,.6,.6)

    point_buffer : list[float] = []

    function_str : str = ""
    parser = NumericStringParser()

    def __init__(self, **kwargs):
        super(Function, self).__init__(**kwargs)

        self.bind(size=self.update,pos=self.update)

        with self.canvas:
            Color(self.color[0],self.color[1],self.color[2])
            self.line : Line = Line(points=None,width = self.line_width)

    def update(self,_instance, _value=None):
        Clock.schedule_once(self.draw_line, 1/60)
        Clock.schedule_once(self.create_line, 1/60)


    def create_line(self,_instance ):
        self.point_buffer.clear()
        if "f(x)=" not in self.function_str:
            return
        function_str = self.function_str[5:]
        print(function_str)
        for p in range(-self.width*self.detail, self.width*self.detail):
            self.point_buffer.append(p/self.detail)
            self.point_buffer.append(self.parse(function_str, p/self.detail))

    def draw_line(self,_instance):
        points = self.point_buffer
        points = [point * self.scale for point in points]

        aspect = self.parent.width / self.parent.height

        for i in range(0, len(points), 2):
            # points[i] *= aspect
            points[i] += self.center_x

        print(self.center_x)

        for i in range(1, len(points), 2):
            points[i] += self.center_y

        self.line.points = points

    def set_Function(self, instance):
        self.function_str = instance.text

    def parse(self, function_str:str, x:float):
        raw = function_str.replace("x", str(x))
        print(raw+" | "+str(self.parser.eval(raw)))
        return self.parser.eval(raw)






class GraphScreen(Screen):
    scale = 16
    detail = 3
    parser = NumericStringParser()

    def __init__(self, **kwargs):
        super(GraphScreen, self).__init__(**kwargs)
        self.bind(size=self._update_size, pos=self._update_size)

        self.lines = []
        self.lines.append(Function())

        for line in self.lines:
            self.add_widget(line)

        with self.canvas:
            Color(1,1,1)
            self.xLine = Line(points=[-0xffff,self.center_y,0xffff,self.center_y],width=2)
            self.yLine = Line(points=[self.center_x,-0xffff,self.center_x,0xffff],width=2)

        self.input_layout = BoxLayout(size_hint=(1,.1),pos_hint={"x":0,"y":0})
        self.add_widget(self.input_layout)



        self.function_input = TextInput(text="f(x)=",multiline=False,font_size=30,size_hint=(1,None),background_color=(0.9,0.9,0.9,0.6),height=48, foreground_color=(1,1,1))
        self.function_input.bind(on_text_validate=self.lines[0].set_Function)
        self.input_layout.add_widget(self.function_input)

        self.back = Button(text="Back",font_size=30,size_hint=(.2,None),pos_hint={"x":0,"y":0},background_color=(0.9,0.9,0.9,0.6),height=48)
        self.back.bind(on_press = self._on_back)
        self.input_layout.add_widget(self.back)

    def _on_back(self,_instance):
        self.parent.current = "main"

    def _update_size(self, _instance, _value):
        xline_points = self.xLine.points
        xline_points[1] = self.center_y
        xline_points[3] = self.center_y
        self.xLine.points = xline_points

        yline_points = self.yLine.points
        yline_points[0] = self.center_x
        yline_points[2] = self.center_x
        self.yLine.points = yline_points