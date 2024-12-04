from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout


class RoundCorner(RelativeLayout):
    def __init__(self,r=50,**kwargs):
        super(RoundCorner, self).__init__(**kwargs)
        self.surf=FloatLayout(); self.add_widget(self.surf)
        with self.canvas:
            Color(.3,0,3,0.3)
            Rectangle(pos=[-r,0],size=[r,self.size[1]])
            Rectangle(pos=[0,-r],size=[self.size[0],self.size[1]+2*r])
            Rectangle(pos=[self.size[0],0],size=[r,self.size[1]])

            Color(0,.3,0,.5)
            Ellipse(pos=[-r,-r],size=[2*r,2*r])
            Ellipse(pos=[self.size[0]-r,-r],size=[2*r,2*r])
            Ellipse(pos=[-r,self.size[1]-r],size=[2*r,2*r])
            Ellipse(pos=[self.size[0]-r,self.size[1]-r],size=[2*r,2*r])

            Color(1,1,1,0.3)
            self.bg=Rectangle(size=self.size)