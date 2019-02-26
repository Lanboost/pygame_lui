from pygamelui.window import *
from pygamelui.components import *
from pygamelui.factory import *

win = Window()


p1 = Panel()
p1.set_rect(-10,-10,-10,-10)
p1.set_anchors(0.3,0.3,0.7,0.7)
p1.set_background((255, 255, 255))

b1 = Button("Test")
b1.set_rect(0,0,100,20)
b1.set_anchors(0.5,0.5,0.5,0.5)

p1.add_child(b1)

b1 = Button("Test1")
b1.set_rect(0,0,100, 30)
b1.align_pivot(ALIGN_CENTER, ALIGN_CENTER)
b1.align_anchor(ALIGN_CENTER, ALIGN_CENTER)

p1.add_child(b1)

p1.add_child(create_vertical_scrollbar())

win.get_panel().add_child(p1)


win.wait_to_close()