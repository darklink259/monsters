import os, pygame
from gamemode import *
from constants import *
class FightMode(GameMode):
    class FightBoxes(object):
        top       = pygame.Rect(24,  24,  88,  36)
        middle    = pygame.Rect(24,  76,  88,  36)
        bottom    = pygame.Rect(24, 128,  88,  36)
        elsewhere = pygame.Rect( 0,   0, 320, 180)
        
        @staticmethod
        def textStart(box):
            return (box.x + 8, box.y + 8)
            
        @staticmethod
        def textWidth(box):
            return box.w - 16
            
        @classmethod
        def boxIn(cls, box, pos):
            """Return a rectangle containing the position."""
            if cls.top.collidepoint(pos):
                return cls.top
            if cls.middle.collidepoint(pos):
                return cls.middle
            if cls.bottom.collidepoint(pos):
                return cls.bottom
            return cls.elsewhere
            
        @classmethod
        def boxKey(cls, box, key):
            """Return a rectangle based on the current rectangle and the key pressed."""
            if (box is cls.middle and key in (  pygame.K_UP,  pygame.K_LEFT))\
            or (box is cls.bottom and key in (pygame.K_DOWN, pygame.K_RIGHT)):
                return cls.top
            if (box is cls.bottom and key in (  pygame.K_UP,  pygame.K_LEFT))\
            or (box is    cls.top and key in (pygame.K_DOWN, pygame.K_RIGHT)):
                return cls.middle
            if (box is    cls.top and key in (  pygame.K_UP,  pygame.K_LEFT))\
            or (box is cls.middle and key in (pygame.K_DOWN, pygame.K_RIGHT)):
                return cls.bottom
            return box
            
    black_box = pygame.image.load(os.path.join('gfx', 'backgrounds', 'blackbox.png'))
    background = pygame.image.load(os.path.join('gfx', 'backgrounds', 'layout2boxes.png'))
    converted = False
    
    def __init__(self, player_mon, enemy_mon):
        super(FightMode, self).__init__()
        if not FightMode.converted:
            FightMode.black_box = FightMode.black_box.convert_alpha()
            FightMode.shared['font_wrap'].renderToInside(FightMode.background,
                FightMode.FightBoxes.textStart(   FightMode.FightBoxes.top),
                FightMode.FightBoxes.textWidth(   FightMode.FightBoxes.top),
                "Attack", False, TEXT_COLOR
            )
            FightMode.shared['font_wrap'].renderToInside(FightMode.background,
                FightMode.FightBoxes.textStart(FightMode.FightBoxes.middle),
                FightMode.FightBoxes.textWidth(FightMode.FightBoxes.middle),
                "Defend", False, TEXT_COLOR
            )
            FightMode.shared['font_wrap'].renderToInside(FightMode.background,
                FightMode.FightBoxes.textStart(FightMode.FightBoxes.bottom),
                FightMode.FightBoxes.textWidth(FightMode.FightBoxes.bottom),
                "Escape", False, TEXT_COLOR
            )
            FightMode.background = FightMode.background.convert_alpha()
            FightMode.converted = True
        
    def input(self, event_list):
        pass
        
    def update(self):
        pass
        
    def draw(self, screen):
        screen.fill(WHITE)
        screen.blit(FightMode.background, (0,0))
        