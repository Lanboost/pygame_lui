from .components import *

def create_vertical_scrollbar():
    p1 = Panel()
    p1.set_rect(0,20,20,20)
    p1.set_anchors(0,0,0,1)
    p1.set_background((128, 128, 128))
    
    
    def update_button(value):
        pass
    
    button_height = 20
    
    button = Button("")
    button.set_rect(0,0,20,button_height)
    button.set_anchors(0,0,0,0)
    #button.set_background((255, 255, 255))
    p1.add_child(button)
    return p1
    
    
def create_scrollpanel():
    p1 = Panel()
    p1.set_rect(-10,-10,-10,-10)
    p1.set_anchors(0.3,0.3,0.7,0.7)
    p1.set_background((255, 255, 255))