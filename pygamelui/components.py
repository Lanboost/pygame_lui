import contextlib
with contextlib.redirect_stdout(None):
    import pygame
pygame.font.init() # you have to call this at the start,
                           # if you want to use this module.
TEXT_FONT = pygame.font.SysFont('Comic Sans MS', 16)
TEXT_FONT_SMALL = pygame.font.SysFont('Comic Sans MS', 8)

ALIGN_TOP = 0
ALIGN_CENTER = 1
ALIGN_BOTTOM = 2
ALIGN_LEFT = 0
ALIGN_RIGHT = 2


class PyGameComponent(object):
    def __init__(self):
        self.visible = True
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.rect = {"left":0, "top":0, "right":0, "bottom":0}
        self.screen_rect = {"left":0, "top":0, "right":0, "bottom":0}
        self.anchors = {"min_x":0, "min_y":0, "max_x":1, "max_y":1}
        self.pivot = {"x":0, "y":0}

        self.mouse_state = {"left_down":False,"middle_down":False, "right_down":False, "mouse_over":False}
        
    def align_pivot(self, x, y):
        if y == ALIGN_TOP:
            self.pivot["y"] = 0
        elif y == ALIGN_CENTER:
            self.pivot["y"] = 0.5
        elif y == ALIGN_BOTTOM:
            self.pivot["y"] = 1
            
        if x == ALIGN_LEFT:
            self.pivot["x"] = 0
        elif x == ALIGN_CENTER:
            self.pivot["x"] = 0.5
        elif x == ALIGN_RIGHT:
            self.pivot["x"] = 1
            
    def align_anchor(self, x, y):
        if y == ALIGN_TOP:
            self.anchors["min_y"] = 0
            self.anchors["max_y"] = 0
        elif y == ALIGN_CENTER:
            self.anchors["min_y"] = 0.5
            self.anchors["max_y"] = 0.5
        elif y == ALIGN_BOTTOM:
            self.anchors["min_y"] = 1
            self.anchors["max_y"] = 1
            
        if x == ALIGN_LEFT:
            self.anchors["min_x"] = 0
            self.anchors["max_x"] = 0
        elif x == ALIGN_CENTER:
            self.anchors["min_x"] = 0.5
            self.anchors["max_x"] = 0.5
        elif x == ALIGN_RIGHT:
            self.anchors["min_x"] = 1
            self.anchors["max_x"] = 1
        

        
    def set_visible(self, value):
        self.visible = value
    
    def set_rect(self, left, top, right, bottom):
   
        self.rect = {"left":left, "top":top, "right":right, "bottom":bottom}

    def _set_x(self, x):
        parent_offset_x = self.screen_rect['left']-self.x
        self.x = x
        self.screen_rect['left'] = self.x+parent_offset_x
        self.screen_rect['right'] = self.screen_rect['left']+self.width

    def _set_y(self, y):
        parent_offset_y = self.screen_rect['top']-self.y
        self.y = y
        self.screen_rect['top'] = self.y+parent_offset_y
        self.screen_rect['bottom'] = self.screen_rect['top']+self.height

    def _set_width(self, width):
        self.width = width
        self.screen_rect['right'] = self.screen_rect['left']+self.width

    def _set_height(self, height):
        self.height = height
        self.screen_rect['top'] = self.screen_rect['bottom']+self.height
        
    def set_anchors(self, min_x, min_y, max_x, max_y):
        self.anchors = {"min_x":min_x, "min_y":min_y, "max_x":max_x, "max_y":max_y}
        
    def set_pivot(self, pivot_x, pivot_y):
        self.pivot = {"x":pivot_x, "y":pivot_y}
        
    def revalidate(self, parent_offset_x, parent_offset_y, parent_width, parent_height, is_self=False):
        #use x,y,height, width if anchors are at one pos
        if not is_self:
            if self.anchors["max_x"] == self.anchors["min_x"]:
                self.x = parent_width*self.anchors["min_x"]+self.rect["left"]-(self.pivot["x"]*self.rect["right"])
                self.width = self.rect["right"]
            else:
                self.width = parent_width*(self.anchors["max_x"]-self.anchors["min_x"])-self.rect["left"]-self.rect["right"]
                self.x = parent_width*self.anchors["min_x"]+self.rect["left"]
            
            if self.anchors["max_y"] == self.anchors["min_y"]:
                self.y = parent_height*self.anchors["min_y"]+self.rect["top"]-(self.pivot["y"]*self.rect["bottom"])
                self.height = self.rect["bottom"]
            else:
                self.height = parent_height*(self.anchors["max_y"]-self.anchors["min_y"])-self.rect["top"]-self.rect["bottom"]
                self.y = self.rect["top"]+parent_height*self.anchors["min_y"]
            #print(self.x, self.y, self.width, self.height, parent_width, parent_height)

        self.screen_rect['left'] = self.x+parent_offset_x
        self.screen_rect['top'] = self.y+parent_offset_y
        self.screen_rect['right'] = self.screen_rect['left']+self.width
        self.screen_rect['bottom'] = self.screen_rect['top']+self.height
        
    def handle_event(self, event):
        return False

    def draw(self,surface, offsetx, offsety):
        pass

    def mouse_enter(self):
        pass

    def mouse_exit(self):
        pass

    def mouse_down(self, button):
        pass

    def mouse_up(self, button):
        pass

    def mouse_clicked(self, button):
        pass
        
class Panel(PyGameComponent):
    def __init__(self):
        super(Panel, self).__init__()
        self.children = []
        self.background_color = (0,0,0)
        
        
    def add_child(self,obj):
        obj.revalidate(self.screen_rect['left'], self.screen_rect['top'], self.width, self.height)
        self.children += [obj]
        
    def set_background(self, color):
        self.background_color = color
        
    def remove_child(self,obj):
        self.children.remove(obj)
        
    def clear(self):
        self.children = []
        
    def handle_event(self,event):
        for c in self.children:
            if not c.visible:
                continue
            if c.handle_event(event):
                return True
        return False
        
    def revalidate(self, parent_offset_x, parent_offset_y, parent_width, parent_height, is_self=False, ignore_child=False):
        super(Panel, self).revalidate(parent_offset_x, parent_offset_y, parent_width, parent_height, is_self)
        if not ignore_child:
            for c in self.children:
                c.revalidate(parent_offset_x+self.x, parent_offset_y+self.y, self.width, self.height)
        
    def draw(self, surface, offsetx, offsety):
        if self.background_color:
            pygame.draw.rect(surface, self.background_color, [offsetx+self.x, offsety+self.y, self.width, self.height], 0)
            
        for c in self.children:
            if not c.visible:
                continue
            #if c.x < surface.get_size()[0] and c.y < surface.get_size()[1]:
            
            c.draw(surface, offsetx+self.x, offsety+self.y)
            
class Button(PyGameComponent):
    def __init__(self, text):
        super(Button, self).__init__()
        self.text = text
        self.on_click = EventHandler()
        self.font = TEXT_FONT
        self.color_scheme = [
            [(192, 192, 192), (128, 128, 128)],
            [(128, 192, 192), (128, 128, 128)],
            [(192, 192, 192), (128, 128, 128)],
            [(128, 128, 128), (90, 90, 90)]
        ]
        self.hover = False
        self.mousedown = False

    def mouse_clicked(self, button):
        if button == 0:
            self.on_click.fire()

    def set_font(self, font):
        self.font = font

    def mouse_enter(self):
        self.hover = True

    def mouse_exit(self):
        self.hover = False
        
    def draw(self, surface, offsetx, offsety):
        colors = self.color_scheme[0]
        if self.mousedown:
            colors = self.color_scheme[2]
        else:
            if self.hover:
                colors = self.color_scheme[1]

        pygame.draw.rect(surface, colors[0], [offsetx+self.x, offsety+self.y, self.width, self.height], 0)
        pygame.draw.rect(surface, colors[1], [offsetx+self.x, offsety+self.y, self.width, self.height], 3)
        #textsurface = self.font.render(str(self.text), True, (0,0,0))
        #r = textsurface.get_rect()
        #surface.blit(textsurface,((self.width-r.width)/2,(self.height-r.height)/2))
        
        
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

    def draw(self, surface, offsetx, offsety):
        super(RadioButton, self).draw(surface, offsetx, offsety)
        print(self.hover)
        print(self.screen_rect)

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
    

        
class VerticalLayoutPanel(Panel):
    def __init__(self, child_width, child_height, spacing = 10, padding = (10,10,10,10)):
        super(VerticalLayoutPanel, self).__init__()
        self.child_width = child_width
        self.child_height = child_height
        self.spacing = spacing
        self.padding = padding

    def add_child(self,obj):
        obj.revalidate(self.screen_rect['left'], self.screen_rect['top'], self.width, self.height)
        self.children += [obj]

    def remove_child(self,obj):
        self.children.remove(obj)
        
    def revalidate(self, parent_offset_x, parent_offset_y, parent_width, parent_height, is_self=False):
        super(VerticalLayoutPanel, self).revalidate(parent_offset_x, parent_offset_y, parent_width, parent_height, is_self, True)
        deltay = self.padding[1]
        #if not ignore_child:
        for c in self.children:
            c.revalidate(parent_offset_x+self.x, parent_offset_y+self.y, self.width, self.height)
            c._set_y(deltay)
            deltay += c.height+self.spacing
        deltay += self.padding[3]
        self._set_height(deltay)
        
class HorizontalLayoutPanel(Panel):
    def __init__(self, child_width=None, child_height=None, spacing = 10, padding = (10,10,10,10)):
        super(HorizontalLayoutPanel, self).__init__()
        #self.child_width = child_width
        #self.child_height = child_height
        self.spacing = spacing
        self.padding = padding

    def add_child(self,obj):
        obj.revalidate(self.screen_rect['left'], self.screen_rect['top'], self.width, self.height)
        #obj.width = self.child_width
        #obj.height = self.child_height
        #obj.x = len(self.children)*(self.child_width+self.spacing)
        #obj.y = 0
        self.children += [obj]

    def remove_child(self,obj):
        self.children.remove(obj)
        
    def revalidate(self, parent_offset_x, parent_offset_y, parent_width, parent_height, is_self=False, ignore_child=False):
        super(HorizontalLayoutPanel, self).revalidate(parent_offset_x, parent_offset_y, parent_width, parent_height, is_self, True)
        deltax = self.padding[0]
        #if not ignore_child:
        for c in self.children:
            c.revalidate(parent_offset_x+self.x, parent_offset_y+self.y, self.width, self.height)
            c._set_x(deltax)
            deltax += c.width+self.spacing
        deltax += self.padding[2]
        self._set_width(deltax)

        
class CellLayoutPanel(Panel):
    def __init__(self, column_count, child_width, child_height, spacing = 10):
        super(CellLayoutPanel, self).__init__()
        self.column_count = column_count
        self.child_width = child_width
        self.child_height = child_height
        self.spacing = spacing
    def add_child(self,obj):
        obj.width = self.child_width
        obj.height = self.child_height
        obj.x = int(len(self.children)%self.column_count)*(self.child_width+self.spacing)
        obj.y = int(len(self.children)/self.column_count)*(self.child_height+self.spacing)
        self.children += [obj]
    def remove_child(self,obj):
        self.children.remove(obj)
        
    def revalidate(self, parent_offset_x, parent_offset_y, parent_width, parent_height, is_self=False):
        super(CellLayoutPanel, self).revalidate(parent_offset_x, parent_offset_y, parent_width, parent_height, is_self, True)

class TabPanel(VerticalLayoutPanel):
    def __init__(self):
        super(TabPanel, self).__init__(0,0)
        self.radioh = RadioButtonHandler()
        self.menu = HorizontalLayoutPanel(100, 40)
        self.menu.set_rect(0,0, 0, 100)
        self.menu.set_anchors(0,0,1,0)
        self.menu.set_background((0,255,0))
        self.display = Panel()
        self.display.set_rect(0,100,0,0)
        self.display.set_anchors(0,0,1,1)
        self.panels = []
        self.add_child(self.menu)
        self.add_child(self.display)
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

        b.set_anchors(0,0,0,1)
        b.set_rect(0,0, 20, 0)

        self.menu.add_child(b)
        
        self.panels += [panel]
        #panel.set_pos(0,0)
        #panel.set_size(self.display.width, self.display.height)
        #panel.set_visible(False)
        #self.display.add_child(panel)

class SliderButton(PyGameComponent):
    pass
class Slider(Panel):
    def __init__(self):
        self.add_child()

class ScrollPanel(Panel):
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
        posx = self.view_x+x
        posy = self.view_y+y
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

    def draw(self, surface, offsetx, offsety):
        for c in self.children:
            if not c.visible:
                continue
            if c.x < surface.get_size()[0] and c.y < surface.get_size()[1]:
                c.draw(surface.subsurface([c.x, c.y, min(surface.get_size()[0]-c.x, c.width), min(surface.get_size()[1]-c.y, c.height)]))

        
class Scrollbar(Panel):
    def __init__(self):
        self.buttonup = ScrollButton()
        self.buttondown = ScrollButton()
        self.slider = ScrollSlider()
    
class ScrollButton(Button):
    pass
    
class ScrollSlider(Button):
    pass
        
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

    