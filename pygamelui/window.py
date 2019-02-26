import pygame
from .components import Panel

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
        
        self.panel.revalidate(self.display_width, self.display_height)
        
    def get_panel(self):
        return self.panel
        
    def update(self):
        #event handling
        for event in pygame.event.get():
        
            #panel
            if self.panel:
                if event.type == pygame.MOUSEBUTTONUP:
                    self.panel.handle_mouse(*pygame.mouse.get_pos(), event.button, 0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.panel.handle_mouse(*pygame.mouse.get_pos(), event.button, 1)
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
                self.panel.revalidate(self.display_width, self.display_height)
    
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
