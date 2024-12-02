from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from Parser import NumericStringParser


class Function(Widget):
    scale : float = 16
    detail : float = 3

    width : int= 3
    color : tuple[float]= (.8,.6,.6)

    point_buffer : list[float] = []

    function_str : str = ""
    parser = NumericStringParser()

    def __init__(self, **kwargs):
        super(Function, self).__init__(**kwargs)

        self.bind(size=self.update,pos=self.update)

        with self.canvas:
            Color(self.color[0],self.color[1],self.color[2])
            self.line : Line = Line(points=self.point_buffer,width = 3)

    #def parse_function(self, parser, x):


    def update(self,instance, value):
        self.create_line()

    def create_line(self):
        self.point_buffer.clear()
        if "f(x)=" not in self.function_str:
            return
        self.function_str = self.function_str[5:]
        for p in range(-self.width, self.width):
            self.point_buffer.append(p/self.detail)
            self.point_buffer.append(self.parse(p/self.detail))

        self.draw_line()

    def draw_line(self):
        points = self.point_buffer
        points = [point * self.scale for point in points]

        aspect = self.width / self.height

        for i in range(0, len(points), 2):
            points[i] *= aspect
            points[i] += self.parent.width / 2


        for i in range(1, len(points), 2):
            points[i] += self.parent.height / 2

        self.line.points = points

    def set_Function(self, fn):
        self.function_str = fn

    def parse(self, x):
        raw = self.function_str.replace("x", str(x))

        return self.parser.eval(raw)






class GraphScreen(Screen):
    scale = 16
    detail = 3
    parser = NumericStringParser()

    def __init__(self, **kwargs):
        super(GraphScreen, self).__init__(**kwargs)
        self.bind(size=self._update_size, pos=self._update_size)

        self.f1 = Function()
        self.f1.function_str = "f(x)=2*x"
        self.add_widget(self.f1)
        self.points = []
        with self.canvas:
            Color(1,1,1)
            self.xLine = Line(points=[-0xffff,self.center_y,0xffff,self.center_y],width=2)
            self.yLine = Line(points=[self.center_x,-0xffff,self.center_x,0xffff],width=2)

            Color(8., .6, .6)
            self.line = Line(points=None, width=3)

        self.input_layout = BoxLayout(size_hint=(1,.1),pos_hint={"x":0,"y":0})
        self.add_widget(self.input_layout)



        self.function_input = TextInput(text="f(x)=",multiline=False,font_size=30,size_hint=(1,None),background_color=(0.9,0.9,0.9,0.6),height=48, foreground_color=(1,1,1))
        self.function_input.bind(on_text_validate=self.create_line)
        self.input_layout.add_widget(self.function_input)

        self.back = Button(text="Back",font_size=30,size_hint=(.2,None),pos_hint={"x":0,"y":0},background_color=(0.9,0.9,0.9,0.6),height=48)
        self.back.bind(on_press = self._on_back)
        self.input_layout.add_widget(self.back)

    def _on_back(self,instance):
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


        self.create_line()


    def parse_function(self, x):
        fn_text : str = self.function_input.text[5:]

        # x_indices = ([pos for pos, char in enumerate(fn_text) if char == "x"])

        fn_text = fn_text.replace("x",str(x))

        return self.parser.eval(fn_text)

    def create_line(self, *instance):
        self.points = []

        if self.function_input.text[5:] == "":
            return

        maxy = self.height * self.scale

        for x in range(int(800/self.scale * self.detail)):
            if self.parse_function(x) >= maxy:
                break

        iterations = int(x*self.detail)

        for p in range(-iterations, iterations, 1):
            self.points.append(p/self.detail)
            self.points.append(self.parse_function(p/self.detail))

        self.draw_line()


    def draw_line(self):
        aspect = self.width / self.height

        points = self.points
        points = [point * self.scale for point in points]

        for i in range(0, len(points), 2):
            #points[i] *= self.width/100
            points[i] *= aspect
            points[i] += self.center_x


        for i in range(1, len(points), 2):
            points[i] += self.center_y

        self.line.points = points