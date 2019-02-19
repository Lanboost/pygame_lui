import contextlib
with contextlib.redirect_stdout(None):
    import pygame
pygame.font.init() # you have to call this at the start,
                           # if you want to use this module.
TEXT_FONT = pygame.font.SysFont('Comic Sans MS', 16)
TEXT_FONT_SMALL = pygame.font.SysFont('Comic Sans MS', 8)
class PyGameComponent(object):
    def __init__(self):
        self.parent_control_pos = False
        self.parent_control_size = False
        self.visible = True
    def set_visible(self, value):
        self.visible = value
    def set_pos(self, x,y):
        if not self.parent_control_pos:
            self.x = x
            self.y = y
    def set_size(self, width, height):
        if not self.parent_control_size:
            self.width = width
            self.height = height
    def handle_event(self, event):
        return False
    def draw(self,surface):
        pass
    
    def handle_mouse(self, x, y, button, click_type):
        return False
class Panel(PyGameComponent):
    def __init__(self):
        super(Panel, self).__init__()
        self.children = []
    def addChild(self,obj):
        self.children += [obj]
    def removeChild(self,obj):
        self.children.remove(obj)
    def clear(self):
        self.children = []
    def handle_mouse(self, x, y, button, click_type):
        for c in self.children:
            if not c.visible:
                continue
            nx = x-c.x
            ny = y-c.y
            if nx >= 0 and ny >= 0 and nx < c.width and ny < c.height:
                if c.handle_mouse(nx, ny, button, click_type):
                    return True
        return False
    def handle_event(self,event):
        for c in self.children:
            if not c.visible:
                continue
            if self.handle_event(event):
                return True
        return False
    def draw(self, surface):
        for c in self.children:
            if not c.visible:
                continue
            if c.x < surface.get_size()[0] and c.y < surface.get_size()[1]:
                c.draw(surface.subsurface([c.x, c.y, min(surface.get_size()[0]-c.x, c.width), min(surface.get_size()[1]-c.y, c.height)]))
BUTTON_NORMAL = 0
BUTTON_HOVER = 1
BUTTON_CLICKED = 2
BUTTON_SELECTED = 3
class Button(PyGameComponent):
    def __init__(self, text):
        super(Button, self).__init__()
        self.text = text
        self.on_click = EventHandler()
        self.state = BUTTON_NORMAL
        self.font = TEXT_FONT
        self.color_scheme = [
            [(192, 192, 192), (128, 128, 128)],
            [(192, 192, 192), (128, 128, 128)],
            [(192, 192, 192), (128, 128, 128)],
            [(128, 128, 128), (90, 90, 90)]
        ]
    def handle_mouse(self, x, y, button, click_type):
        if click_type == 1:
            self.on_click.fire()
    def set_font(self, font):
        self.font = font
    def set_state(self, state):
        self.state = state
        
        
    def draw(self, surface):
        
        colors = self.color_scheme[self.state]
        pygame.draw.rect(surface, colors[0], [0, 0, self.width, self.height], 0)
        pygame.draw.rect(surface, colors[1], [0, 0, self.width, self.height], 3)
        textsurface = self.font.render(str(self.text), True, (0,0,0))
        r = textsurface.get_rect()
        surface.blit(textsurface,((self.width-r.width)/2,(self.height-r.height)/2))
class EventHandler(object):
    def __init__(self):
        self.funcs = []
    def add(self, func):
        self.funcs += [func]
    def fire(self, *args):
        for f in self.funcs:
            f(*args)
class RadioButtonHandler(object):
    def __init__(self):
        self.on_change = EventHandler()
        self.selected = -1
        self.buttons = []
        self.__own_assignment = False
        
    def clear(self):
        self.buttons = []
    def add(self, radiobutton):
        self.buttons += [radiobutton]
        radiobutton.on_click.add(self.__get_click_handler(radiobutton))
    def button_clicked(self, button):
        for i, b in enumerate(self.buttons):
            if b == button:
                self.selected = i
                button.set_state(BUTTON_SELECTED)
            else:
                b.set_state(BUTTON_NORMAL)
        self.on_change.fire()
    
    def __get_click_handler(self, button):
        def clicked():
            self.button_clicked(button)
        return clicked
    #Overload assignment to set selected
    def __setattr__(self, name, value):
        #print(self.__dict__)
        if "_RadioButtonHandler__own_assignment" in self.__dict__ and not self.__own_assignment and name == "selected":
            self.__own_assignment = True
            self.__set_selected(value)
            self.__own_assignment = False
            return 
            #raise AttributeError("MyClass does not allow assignment to .x member")
        self.__dict__[name] = value
    def __set_selected(self, selected):
        self.selected = selected
        for i, b in enumerate(self.buttons):
            if i==selected:
                b.set_state(BUTTON_SELECTED)
            else:
                b.set_state(BUTTON_NORMAL)
        self.on_change.fire()
        
class RadioButton(Button):
    def __init__(self, text):
        super(RadioButton, self).__init__(text)
class CheckBox(Button):
    def __init__(self, text, check_value = False):
        super(CheckBox, self).__init__(text)
        self.on_click.add(self.g_check)
        self.on_change = EventHandler()
        self.checked = check_value
        self.__update_check()
    def __update_check(self):
        if self.checked:
            self.state = BUTTON_SELECTED
        else:
            self.state = BUTTON_NORMAL
        self.on_change.fire()
    def g_check(self):
        self.checked = not self.checked
        self.__update_check()
    
class TabPanel(Panel):
    def __init__(self):
        super(TabPanel, self).__init__()
        self.radioh = RadioButtonHandler()
        self.menu = HorizontalLayoutPanel(100, 40)
        self.menu.set_pos(0,0)
        self.menu.set_size(400, 40)
        self.display = Panel()
        self.display.set_pos(0,45)
        self.display.set_size(400,500)
        self.panels = []
        self.addChild(self.menu)
        self.addChild(self.display)
        self.radioh.on_change.add(self.g_set_selected_panel())
        self.on_change = EventHandler()
        self.selected = -1
    def set_size(self, width, height):
        super(TabPanel, self).set_size(width, height)
        self.display.set_size(width,height-45)
        self.menu.set_size(width, 40)
    def g_set_selected_panel(self):
        def f():
            self.set_selected_panel(self.radioh.selected)
        return f
    def set_selected_panel(self, id):
        for p in self.panels:
            p.set_visible(False)
        self.panels[id].set_visible(True)
        self.selected = id
        self.on_change.fire()
    def add_tab(self, text, panel):
        b = RadioButton(text)
        self.radioh.add(b)
        self.menu.addChild(b)
        self.panels += [panel]
        panel.set_pos(0,0)
        panel.set_size(self.display.width, self.display.height)
        panel.set_visible(False)
        self.display.addChild(panel)
        
class VerticalLayoutPanel(Panel):
    def __init__(self, child_width, child_height, spacing = 10):
        super(VerticalLayoutPanel, self).__init__()
        self.child_width = child_width
        self.child_height = child_height
        self.spacing = spacing
    def addChild(self,obj):
        obj.width = self.child_width
        obj.height = self.child_height
        obj.x = 0
        obj.y = len(self.children)*(self.child_height+self.spacing)
        self.children += [obj]
    def removeChild(self,obj):
        self.children.remove(obj)
    def clear(self):
        self.children = []
class HorizontalLayoutPanel(Panel):
    def __init__(self, child_width, child_height, spacing = 10):
        super(HorizontalLayoutPanel, self).__init__()
        self.child_width = child_width
        self.child_height = child_height
        self.spacing = spacing
    def addChild(self,obj):
        obj.width = self.child_width
        obj.height = self.child_height
        obj.x = len(self.children)*(self.child_width+self.spacing)
        obj.y = 0
        self.children += [obj]
    def removeChild(self,obj):
        self.children.remove(obj)
    def clear(self):
        self.children = [] 
class CellLayoutPanel(Panel):
    def __init__(self, column_count, child_width, child_height, spacing = 10):
        super(CellLayoutPanel, self).__init__()
        self.column_count = column_count
        self.child_width = child_width
        self.child_height = child_height
        self.spacing = spacing
    def addChild(self,obj):
        obj.width = self.child_width
        obj.height = self.child_height
        obj.x = int(len(self.children)%self.column_count)*(self.child_width+self.spacing)
        obj.y = int(len(self.children)/self.column_count)*(self.child_height+self.spacing)
        self.children += [obj]
    def removeChild(self,obj):
        self.children.remove(obj)
    def clear(self):
        self.children = [] 
    
class SliderButton(PyGameComponent):
    pass
class Slider(Panel):
    def __init__(self):
        self.addChild()


class ZoomPanel(Panel):
    def __init__(self):
        super(ZoomPanel, self).__init__()
        self.view_x = 0
        self.view_y = 0
        self.view_height = 1
        self.view_width = 1
        self.content_width = 0
        self.content_height = 0

    def set_content_pane(self, width, height):
        self.content_width = width
        self.content_height = height

    def set_view(self, x, y, width, height):
        self.view_x = max(0,x)
        self.view_y = max(0, y)
        self.view_width = min(self.content_width, width)
        self.view_height = min(self.content_height, height)

    def pos_to_view(self, x, y):
        xscale = self.view_width/self.content_width
        yscale = self.view_height/self.content_height
        posx = self.view_x+x*xscale
        posy = self.view_y+y*yscale
        return (posx, posy)

    def handle_mouse(self, x, y, button, click_type):
        posx, posy = self.pos_to_view(x,y)
        for c in self.children:
            if not c.visible:
                continue
            nx = posx-c.x
            ny = posy-c.y
            if nx >= 0 and ny >= 0 and nx < c.width and ny < c.height:
                if c.handle_mouse(nx, ny, button, click_type):
                    return True
        return False

    def handle_event(self,event):
        for c in self.children:
            if not c.visible:
                continue
            if self.handle_event(event):
                return True
        return False

    def draw(self, surface):
        for c in self.children:
            if not c.visible:
                continue
            if c.x < surface.get_size()[0] and c.y < surface.get_size()[1]:
                c.draw(surface.subsurface([c.x, c.y, min(surface.get_size()[0]-c.x, c.width), min(surface.get_size()[1]-c.y, c.height)]))

    