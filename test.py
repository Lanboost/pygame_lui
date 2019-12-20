from pygamelui.window import *
from pygamelui.components import *
from pygamelui.factory import *

win = Window()


p1 = Panel()
p1.set_rect(-10,-10,-10,-10)
p1.set_anchors(0.3,0.3,0.7,0.7)
p1.set_background((255, 255, 255))


tab_panel = TabPanel()
tab_panel_1 = Panel()
tab_panel_2 = Panel()
tab_panel.add_tab("Tab 1", tab_panel_1)
tab_panel.add_tab("Tab 2", tab_panel_2)

tab_panel.set_rect(0,0,0,0)
tab_panel.set_anchors(0,0,0.5,0.3)

tab_panel.set_background((255,0,0))

#p1.add_child(tab_panel)
'''
b1 = Button("Test")
b1.set_rect(0,0,100,20)
b1.set_anchors(0.5,0.5,0.5,0.5)
b1.on_click.add(lambda: print("Test clicked"))

p1.add_child(b1)

b1 = Button("Test1")
b1.set_rect(0,0,100, 30)
b1.align_pivot(ALIGN_CENTER, ALIGN_CENTER)
b1.align_anchor(ALIGN_CENTER, ALIGN_CENTER)
b1.on_click.add(lambda: print("Test1 clicked"))

p1.add_child(b1)

p1.add_child(create_vertical_scrollbar())
'''
win.get_panel().add_child(tab_panel)


win.wait_to_close()