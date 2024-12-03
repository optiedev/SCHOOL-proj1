from kivy.app import App
from kivy.graphics import Rectangle, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.uix.textinput import TextInput
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label

import Graph
from Parser import NumericStringParser


class MainScreen(Screen):
    def on_button_press(self, instance):
        current : str = self.solution.text  # Nuvarande text i displayen
        button_text : str = instance.text  # Texten på knappen som trycktes
        sound = SoundLoader.load(r"morse.mp3")  # Byt ut till din ljudfil
        if sound:
            sound.play()  # Spela upp ljudet

        if button_text == "C":
            # Om knappen är "C", rensa displayen
            self.solution.text = ""
            return
            # Förhindra att två operatorer trycks efter varandra
        elif button_text == "xⁿ":
            button_text = "^"
        elif button_text == "<":
            self.solution.text = self.solution.text[:-1]
            return
        elif len(button_text) > 2:
            button_text = button_text + "("

        # if  len(self.solution.text) > 2 and self.solution.text[len(self.solution.text)-2] in self.operators:
        #    return
        # Lägg till texten på knappen till displayen
        self.solution.text += button_text

    def on_history_pressed(self, instance):
        self.solution_history.append(str(self.solution.text))


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


    # Updaterar additionalButtons i additionalButtonLayouten.
    def update_buttons(self):
        self.additionalButtonsLayout.clear_widgets()

        for row in self.additionalButtons:
            for label in row:
                button = Button(
                    text=label,
                    font_size=30,
                    background_color=(0.5, 0.5, 0.5, 1),  # Grå färg
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                )
                button.bind(on_press=self.on_button_press)
                self.additionalButtonsLayout.add_widget(button)

    # Switchar knapparna
    def on_buttonSwitch_pressed(self,instance):
        if self.functionSwitch == 0:
            self.functionSwitch = 1

            self.additionalButtons = [
                ["atan", "asin", "acos"],
                ["tanh", "sinh", "cosh"],
                ["atanh", "asinh", "acosh"]
                ]

            # Kallar på updaterings funktionen och lägger tilbaks bytes knappen.
            self.update_buttons()
            self.additionalButtonsLayout.add_widget(self.switchFunctions)

        elif self.functionSwitch == 1:
            self.functionSwitch = 0
            self.additionalButtons = [
                ["tan", "sin", "cos"],
                ["In", "log", "1/"],
                ["e^", "^2", "+"],
                ["abs", "pi", "e"]
                ]

            # Kallar på updaterings funktionen och lägger tilbaks bytes knappen.
            self.update_buttons()
            self.additionalButtonsLayout.add_widget(self.switchFunctions)

    # Definerar vad som händer när knappen är tryckt. Det ska tilläga eller ta bort additionalButtonLayouten.
    def more_buttons_pressed(self,instance):
        if self.moreButtonsShowing == 0:
            self.moreButtonsShowing = 1
            self.calc_layout.add_widget(self.additionalButtonsLayout)
        elif self.moreButtonsShowing == 1:
            self.moreButtonsShowing = 0
            self.calc_layout.remove_widget(self.additionalButtonsLayout)


    def __init__(self, **kwargs):
            super(MainScreen, self).__init__(**kwargs)
            self.moreButtonsShowing = 0
            self.functionSwitch = 0
            self.solution_history = []

            self.parser = NumericStringParser()
            # Definiera operatörer och spårning
            self.operators = ["/", "*", "+", "-"]
            # Skapa huvudlayouten (vertikal)
            self.main_layout = BoxLayout(orientation="horizontal")
            self.add_widget(self.main_layout)

            self.left_layout = BoxLayout(orientation="vertical",size_hint=(.2,1))
            self.graph_button = Button(
                #background_normal="graph_normal.png",
                #background_down="graph_down.png",
                text= "Graph",
                size_hint=(1, .2),
                pos_hint={"x":0,"y":.8}
            )
            self.graph_button.bind(on_press=self._on_graph)

            # Knapp som ska tilläga eller ta bort additionalbuttonlayouten med kallalse av funktionen more_buttons_pressed.
            self.more_functions = Button(
                #background_normal="graph_normal.png",
                #background_down="graph_down.png",
                text= "More functions",
                size_hint=(1, .8),
                #pos_hint={"x":0,"y":0}
            )

            self.show_solution_history = Button(
                text="History",
                font_size=30,
                background_color=(0.5, 0.5, 0.5, 1),  # Grå färg
                pos_hint={"center_x": 0.5, "center_y": 0.5},
            )

            self.show_solution_history.bind(on_press=self.on_history_pressed)


            self.more_functions.bind(on_press=self.more_buttons_pressed)
            self.left_layout.add_widget(self.graph_button)
            self.left_layout.add_widget(self.more_functions)
            self.left_layout.add_widget(self.show_solution_history)
            self.main_layout.add_widget(self.left_layout)


            self.calc_layout = BoxLayout(orientation="vertical",size_hint=(.8,1))
            self.main_layout.add_widget(self.calc_layout)
            # Skapa textfältet som fungerar som kalkylatorns
            # display
            self.solution = TextInput(
                background_color="black",
                foreground_color="white",
                multiline=False,
                readonly=True,
                halign="left",
                size_hint=(1,.2),
                font_size=50,
            )
            self.calc_layout.add_widget(self.solution)

            # Skapa knapparna för kalkylatorn
            self.buttons = [
                ["(",")","xⁿ","/"],
                ["7", "8", "9", "*"],
                ["4", "5", "6", "+"],
                ["1", "2", "3", "-"],
                [".", "0", "C", "<"],

            ]

            self.ButtonLayout = GridLayout(cols=4, size_hint=(1,.8))

            for row in self.buttons:
                for label in row:
                    button = Button(
                        text=label,
                        font_size=30,
                        background_color=(0.5, 0.5, 0.5, 1),  # Grå färg
                        pos_hint={"center_x": 0.5, "center_y": 0.5},
                    )
                    button.bind(on_press=self.on_button_press)
                    self.ButtonLayout.add_widget(button)
            self.calc_layout.add_widget(self.ButtonLayout)


            self.additionalButtons = [
                ["tan", "sin", "cos"],
                ["In", "log", "1/"],
                ["e^", "^2", "+"],
                ["abs", "pi", "e"]
                ]

            self.additionalButtonsLayout = GridLayout(cols=4, size_hint=(1,.8))

            for row in self.additionalButtons:
                for label in row:
                    button = Button(
                        text=label,
                        font_size=30,
                        background_color=(0.5, 0.5, 0.5, 1),  # Grå färg
                        pos_hint={"center_x": 0.5, "center_y": 0.5},
                    )
                    button.bind(on_press=self.on_button_press)
                    self.additionalButtonsLayout.add_widget(button)

            self.switchFunctions = Button(
                text="ChangeFunctions",
                font_size=30,
                background_color=(0.6, 0.8, 0.8,),  # Turkås färg
                pos_hint={"center_x": 0.5, "center_y": 0.5},
            )

            self.switchFunctions.bind(on_press = self.on_buttonSwitch_pressed)
            self.additionalButtonsLayout.add_widget(self.switchFunctions)




            equal_button = Button(
                text="=",
                font_size=30,
                background_color=(0.5, 0.8, 0.5, 1),  # Grön färg
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                size_hint=(1,.2)
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
