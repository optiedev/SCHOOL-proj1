from kivy.app import App
from kivy.graphics import Rectangle, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.uix.textinput import TextInput

import Graph
from Parser import NumericStringParser


class MainScreen(Screen):
    def on_button_press(self, instance):
        current = self.solution.text  # Nuvarande text i displayen
        button_text = instance.text  # Texten på knappen som trycktes

        if button_text == "C":
            # Om knappen är "C", rensa displayen
            self.solution.text = ""
            return
            # Förhindra att två operatorer trycks efter varandra

        # if  len(self.solution.text) > 2 and self.solution.text[len(self.solution.text)-2] in self.operators:
        #    return
        # Lägg till texten på knappen till displayen
        self.solution.text += button_text

    def on_solution(self, instance):
        """Beräknar lösningen."""
        try:
            # Utvärdera uttrycket och visa resultatet
            self.solution.text = str(self.parser.eval(self.solution.text))
        except Exception:
            # Vid fel, visa "Error"
            self.solution.text = "Error"

    def _on_graph(self,instance):
        app.root.current = "graph"

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.parser = NumericStringParser()
        # Definiera operatörer och spårning
        self.operators = ["/", "*", "+", "-"]
        # Skapa huvudlayouten (vertikal)
        self.main_layout = BoxLayout(orientation="horizontal")
        self.add_widget(self.main_layout)

        self.graph_button = Button(
            #background_normal="graph_normal.png",
            #background_down="graph_down.png",
            text= "Graph",
            size_hint=(.2, .2),
            pos_hint={"x":0,"y":.8}
        )
        self.graph_button.bind(on_press=self._on_graph)
        self.main_layout.add_widget(self.graph_button)

        self.calc_layout = BoxLayout(orientation="vertical")
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
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "+"],
            [".", "0", "C", "-"],

        ]

        # Lägg till knapparna i huvudlayouten
        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(
                    text=label,
                    font_size=30,
                    background_color=(0.5, 0.5, 0.5, 1),  # Grå färg
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            self.calc_layout.add_widget(h_layout)

        equal_button = Button(
            text="=",
            font_size=30,
            background_color=(0.5, 0.8, 0.5, 1),  # Grön färg
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        equal_button.bind(on_press=self.on_solution)
        self.calc_layout.add_widget(equal_button)

class MainApp(App):
    def build(self):
        self.icon = ".\\icon.png"

        self.root = ScreenManager(transition=NoTransition())
        self.root.add_widget(Graph.GraphScreen(name="graph"))
        self.root.add_widget(MainScreen(name="main"))

        self.root.current = "main"

        self.root.bind(size=self._update_rect, pos=self._update_rect)
        # Background Color

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
