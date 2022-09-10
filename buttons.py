import pygame,colors as c

class Button(pygame.Rect):
    def __init__(self, x=0, y=0, width=0, height=0, color=c.white, selected=False):
        pygame.Rect.__init__(self, x, y, width, height)
        self.color = color # Original/default color
        self.color2 = [i - 80 if i >= 80 else 0 for i in self.color] # Color for when hovering over the button
        
        self.border = pygame.Rect(x - 4, y - 4, width + 8, height + 8)
        self.bttm = pygame.Rect(x - 4, y + height + 4, width + 8, 7) # "Shadow" below the button
        
        self.selected = selected

    def draw(self, surface, pos):
        pygame.draw.rect(surface, c.node, self.bttm) # Shadow
        if not self.selected:
            pygame.draw.rect(surface, c.gray, self.border)
            pygame.draw.rect(surface, self.color2 if self.collidepoint(pos) else self.color, self)
        else:
            pygame.draw.rect(surface, c.gray, (self.x - 4, self.y + 3, self.width + 8, self.height + 8))
            pygame.draw.rect(surface, self.color2, (self.x, self.y + 7, self.width, self.height))