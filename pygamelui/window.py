import pygame
from .components import Panel

MOUSE_LEFT = 0
MOUSE_MIDDLE = 1
MOUSE_RIGHT = 2

class Window(object):
    def __init__(self, width=800, height=600, title="Window pygameliu"):
        
        self._should_close = False
        pygame.init()
        self.display_width = width
        self.display_height = height



        self.canvas = pygame.display.set_mode((self.display_width,self.display_height), pygame.RESIZABLE)
        pygame.display.set_caption(title)


        self.clock = pygame.time.Clock()
        self.fps = 30

        self.panel = Panel()
        self.panel.set_rect(0,0,0,0)
        self.panel.set_anchors(0,0,1,1)
        
        self.panel.revalidate(0,0, self.display_width, self.display_height)
        
    def get_panel(self):
        return self.panel
        
    def update(self):
        #event handling

        def update_mouse(component, mouse_x, mouse_y, left_down, middle_down, right_down):
            if isinstance(component, Panel):
                for co in component.children:
                    update_mouse(co, mouse_x, mouse_y, left_down, middle_down, right_down)
            else:
                if component.screen_rect['left'] <= mouse_x and mouse_x < component.screen_rect['right'] and \
                                    component.screen_rect['top'] <= mouse_y and mouse_y < component.screen_rect['bottom']:
                    
                    if left_down:
                        if not component.mouse_state['left_down']:
                            component.mouse_down(MOUSE_LEFT)
                            component.mouse_state['left_down'] = True
                    else:
                        if component.mouse_state['left_down']:
                            component.mouse_clicked(MOUSE_LEFT)
                            component.mouse_up(MOUSE_LEFT)
                            component.mouse_state['left_down'] = False

                    if middle_down:
                        if not component.mouse_state['middle_down']:
                            component.mouse_clicked(MOUSE_MIDDLE)
                            component.mouse_down(MOUSE_MIDDLE)
                            component.mouse_state['middle_down'] = True
                    else:
                        component.mouse_state['middle_down'] = False

                    if right_down:
                        if not component.mouse_state['right_down']:
                            component.mouse_clicked(MOUSE_RIGHT)
                            component.mouse_down(MOUSE_RIGHT)
                            component.mouse_state['right_down'] = True
                    else:
                        component.mouse_state['right_down'] = False

                    if not component.mouse_state['mouse_over']:
                        component.mouse_state['mouse_over'] = True
                        component.mouse_enter()
                else:
                    if component.mouse_state['mouse_over']:
                        component.mouse_state['mouse_over'] = False
                        component.mouse_exit()
                    


        update_mouse(self.panel, *pygame.mouse.get_pos(), *pygame.mouse.get_pressed())

        for event in pygame.event.get():
        
            #panel
            if self.panel:
                if event.type == pygame.MOUSEBUTTONUP:
                    pass
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                else:
                    self.panel.handle_event(event)

            if event.type == pygame.QUIT:
                self._should_close = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._should_close = True
                    
            elif event.type == pygame.VIDEORESIZE:
                # There's some code to add back window content here.
                self.display_width, self.display_height = event.w, event.h
                self.canvas = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self.panel.revalidate(0, 0, self.display_width, self.display_height)
    
        #clear previous rendering
        self.canvas.fill((0,0,0))



        if self.panel:
            self.panel.draw(self.canvas, 0, 0)




        #update stuffs
        pygame.display.update()
        self.clock.tick(self.fps)
        
    def should_close(self):
        return self._should_close

    def close(self):
        pygame.quit()
        
    def wait_to_close(self):
        while True:
            self.update()
            if self.should_close():
                break
