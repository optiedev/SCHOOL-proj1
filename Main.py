from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class MainApp(App):
    def build(self):
        # Ställer in ikonen för appen (valfritt)
        #self.icon = "C:/Users/Wafaa.almaliki/OneDrive -
        #Academedia/Desktop/PythonIcon/icons8-
        #calculator-50.png"

        # Definiera operatörer och spårning
        self.operators = ["/", "*", "+", "-"]
        self.last_was_operator = None
        self.last_button = None

        # Skapa huvudlayouten (vertikal)
        main_layout = BoxLayout(orientation="vertical")

        # Skapa textfältet som fungerar som kalkylatorns
        # display
        self.solution = TextInput(
            background_color="black",
            foreground_color="white",
            multiline=False,
            readonly=True,
            halign="right",
            font_size=30,
        )
        main_layout.add_widget(self.solution)

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
                    background_color=(0.5, 0.5, 0.5, 1), # Grå färg
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                )
                # Koppla knapptryckningar till on_button_press
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        # Skapa likamed-knappen

        equal_button = Button(
        text="=",
        font_size=30,
        background_color=(0.5, 0.8, 0.5, 1), # Grön färg
        pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        equal_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equal_button)

        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text # Nuvarande text idisplayen
        button_text = instance.text # Texten på knappensom trycktes

        if button_text == "C":

            # Om knappen är "C", rensa displayen
            self.solution.text = ""
        else:
            # Förhindra att två operatorer trycks efter varandra
            if current and (self.last_was_operator and
                button_text in self.operators):
                return
            elif button_text in self.operators:
                self.last_was_operator = True
            else:
                self.last_was_operator = False
                # Lägg till texten på knappen till displayen
                self.solution.text += button_text

    def on_solution(self, instance):
        """Beräknar lösningen."""
        try:
        # Utvärdera uttrycket och visa resultatet
            self.solution.text = str(eval(self.solution.text))
        except Exception:
        # Vid fel, visa "Error"
            self.solution.text = "Error"

if __name__ == "__main__":
    app = MainApp()
    app.run()