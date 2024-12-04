from kivy.app import App
from kivy.graphics import Rectangle, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.uix.textinput import TextInput
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.core.window import Window

import Graph
from Parser import NumericStringParser


class MainScreen(Screen):
    def on_button_press(self, instance):
        current : str = self.solution.text  # Nuvarande text i displayen
        button_text : str = instance.text  # Texten på knappen som trycktes


        if button_text == "C":
            # Om knappen är "C", rensa displayen
            self.solution.text = ""
            return
            # Förhindra att två operatorer trycks efter varandra
        elif button_text == "=":
            self.on_solution()
            return
        elif button_text == "xⁿ":
            button_text = "^"
        elif button_text == "<":
            self.solution.text = self.solution.text[:-1]
            return
        elif len(button_text) > 2:
            button_text = button_text + "("

        # Lägg till texten på knappen till displayen
        self.solution.text += button_text

    def on_solution(self):
        """Beräknar lösningen."""
        try:
            # Utvärdera uttrycket och visa resultatet
            self.solution.text = str(self.parser.eval(self.solution.text))
        except Exception:
            # Vid fel, visa "Error"
            self.solution.text = "Error"
        else:
            self.history.append(self.solution.text)

    def _on_graph(self,instance):
        app.root.current = "graph"

    def on_history(self, instance):
        try:
            self.solution.text += self.history[len(self.history)-1]
        except:
            self.solution.text += "0"


    def __init__(self, **kwargs):
            super(MainScreen, self).__init__(**kwargs)

            self.history = []

            self.parser = NumericStringParser()
            # Definiera operatörer och spårning
            self.operators = ["/", "*", "+", "-"]
            # Skapa huvudlayouten (vertikal)
            self.main_layout = BoxLayout(orientation="vertical")
            self.add_widget(self.main_layout)

            self.top_layout = RelativeLayout(size_hint=(1,.05))
            self.to_graph = Button(
                    text= "Graph",
                    size_hint=(.2, 1),
                    pos_hint={"x":0,"y":0},
                    background_normal="button_rect_down.png",
                    background_down="button_rect_down.png",

                )

            self.to_graph.bind(on_press=self._on_graph)
            self.top_layout.add_widget(self.to_graph)

            self.to_history = Button(
                    text= "Ans",
                    size_hint=(.2, 1),
                    pos_hint={"x":.8,"y":0},
                    background_normal="button_rect_down.png",
                    background_down="button_rect_down.png",

                )

            self.to_history.bind(on_press=self.on_history)
            self.top_layout.add_widget(self.to_history)

            self.main_layout.add_widget(self.top_layout)

            self.calc_layout = BoxLayout(orientation="vertical",size_hint=(1,1))
            self.main_layout.add_widget(self.calc_layout)
            # Skapa textfältet som fungerar som kalkylatorns
            # display
            self.solution = TextInput(
                background_color="black",
                foreground_color="white",
                multiline=False,
                readonly=True,
                halign="left",
                size_hint=(1,1),
                font_size=50,
            )
            self.calc_layout.add_widget(self.solution)

            # Skapa knapparna för kalkylatorn

            # Lägg till knapparna i huvudlayouten

            buttons = [
                ["(",")","xⁿ","/","PI"],
                ["7", "8", "9", "*","sin"],
                ["4", "5", "6", "+","cos"],
                ["1", "2", "3", "-","tan"],
                ["0", ".", "C", "<","="],

            ]

            for row in buttons:
                h_layout = BoxLayout()
                for label in row:
                    per_button_layout = BoxLayout()
                    button = Button(
                        text=label,
                        font_size=30,
                        background_color=(0.5, 0.5, 0.5, 1),  # Grå färg
                        pos_hint={"center_x": 0.5, "center_y": 0.5},
                        # size = (100,100),
                        padding=[100,0],
                        size_hint=(0,0),
                        background_normal="button_normal.png",
                        background_down="button_down.png",
                        border =(0,0,0,0)
                    )
                    button.bind(on_press=self.on_button_press)
                    per_button_layout.add_widget(button)
                    h_layout.add_widget(per_button_layout)
                self.calc_layout.add_widget(h_layout)

class MainApp(App):
    def build(self):
        self.icon = ".\\icon.png"

        self.root = ScreenManager(transition=NoTransition())
        self.root.add_widget(Graph.GraphScreen(name="graph"))
        self.root.add_widget(MainScreen(name="main"))

        self.root.current = "main"

        self.root.bind(size=self._update_rect, pos=self._update_rect)
        # Background Color

        Window.size = (600, 800)
        Window.minimum_width = 500
        Window.minimum_height = 640


        with self.root.canvas.before:
            Color(.09, .09, .13, 1)
            self.rect = Rectangle(size=self.root.size, pos=self.root.pos)
        return self.root

    def _update_rect(self, instance, _value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


app = MainApp()
if __name__ == "__main__":
    app.run()
