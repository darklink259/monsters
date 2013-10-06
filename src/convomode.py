import os, pygame
from gamemode import *
class ConvoMode(GameMode):
    class ConvoBoxes(object):
        top_left     = pygame.Rect(  8, 88, 88, 36)
        top_right    = pygame.Rect(224, 88, 88, 36)
        bottom_left  = pygame.Rect(  8,132, 88, 36)
        bottom_right = pygame.Rect(224,132, 88, 36)
        elsewhere    = pygame.Rect(  0,  0,320,180)
        
        @classmethod
        def boxIn(cls, box, pos):
            """Return a rectangle containing the position."""
            if cls.top_left.collidepoint(pos):
                return cls.top_left
            if cls.top_right.collidepoint(pos):
                return cls.top_right
            if cls.bottom_left.collidepoint(pos):
                return cls.bottom_left
            if cls.bottom_right.collidepoint(pos):
                return cls.bottom_right
            return cls.elsewhere
            
        @classmethod
        def boxKey(cls, box, key):
            """Return a rectangle based on the current rectangle and the key pressed."""
            if (box, key) in ((cls.top_right, pygame.K_LEFT), (cls.bottom_right, pygame.K_RIGHT)):
                return cls.top_left
            if (box, key) in ((cls.bottom_left, pygame.K_LEFT), (cls.top_left, pygame.K_RIGHT)):
                return cls.top_right
            if (box, key) in ((cls.bottom_right, pygame.K_LEFT), (cls.top_right, pygame.K_RIGHT)):
                return cls.bottom_left
            if (box, key) in ((cls.top_left, pygame.K_LEFT), (cls.bottom_left, pygame.K_RIGHT)):
                return cls.bottom_right
            return box
            
    SCROLL_AMOUNT_MOUSE = 10
    SCROLL_AMOUNT_KEY = 1
    black_box = pygame.image.load(os.path.join('gfx', 'backgrounds', 'blackbox.png'))
    converted = False
    
    def _textMain(self):
        #return text for main section
        raise NotImplementedError(self.__class__.__name__ + "._textMain(self)")
    def _textButton0(self):
        #return text for button 0
        raise NotImplementedError(self.__class__.__name__ + "._textButton0(self)")
    def _textButton1(self):
        #return text for button 1
        raise NotImplementedError(self.__class__.__name__ + "._textButton1(self)")
    def _textButton2(self):
        #return text for button 2
        raise NotImplementedError(self.__class__.__name__ + "._textButton2(self)")
    def _textButton3(self):
        #return text for button 3
        raise NotImplementedError(self.__class__.__name__ + "._textButton3(self)")
    def _goButton0(self):
        #do stuff for button 0
        raise NotImplementedError(self.__class__.__name__ + "._goButton0(self)")
    def _goButton1(self):
        #do stuff for button 1
        raise NotImplementedError(self.__class__.__name__ + "._goButton1(self)")
    def _goButton2(self):
        #do stuff for button 2
        raise NotImplementedError(self.__class__.__name__ + "._goButton2(self)")
    def _goButton3(self):
        #do stuff for button 3
        raise NotImplementedError(self.__class__.__name__ + "._goButton3(self)")
        
    def _readyText(self):
        #mainly, make the surfaces based on the text for view and buttons, fitting some criteria
        self.surf_text = self.shared['font_wrap'].renderInside(288, self._textMain(), False, (164, 162, 165))
        self.surf_rect = self.surf_text.get_rect()
        self.text_rect = pygame.Rect(0,0,288,48)
        self.shared['font_wrap'].renderToInside(self.background, ( 16, 96), 72, self._textButton0(), False, (164, 162, 165))
        self.shared['font_wrap'].renderToInside(self.background, (232, 96), 72, self._textButton1(), False, (164, 162, 165))
        self.shared['font_wrap'].renderToInside(self.background, ( 16,140), 72, self._textButton2(), False, (164, 162, 165))
        self.shared['font_wrap'].renderToInside(self.background, (232,140), 72, self._textButton3(), False, (164, 162, 165))
        
    def __init__(self):
        super(ConvoMode, self).__init__()
        if not ConvoMode.converted:
            ConvoMode.converted = True
            ConvoMode.black_box.convert_alpha()
        self.background = pygame.image.load(os.path.join('gfx', 'backgrounds', 'layout1boxes.png')).convert_alpha()
        self._readyText()
        self.y_scroll = {'up': 0, 'down': 0}
        self.box_selected = ConvoMode.ConvoBoxes.top_left
        #what else do conversations need?
        
    def _buttonPress(self):
        if self.box_selected == ConvoMode.ConvoBoxes.top_left:
            self._goButton0()
        elif self.box_selected == ConvoMode.ConvoBoxes.top_right:
            self._goButton1()
        elif self.box_selected == ConvoMode.ConvoBoxes.bottom_left:
            self._goButton2()
        elif self.box_selected == ConvoMode.ConvoBoxes.bottom_right:
            self._goButton3()
            
    def input(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEMOTION:
                select = ConvoMode.ConvoBoxes.boxIn(self.box_selected, event.pos)
                if select != ConvoMode.ConvoBoxes.elsewhere:
                    self.box_selected = select
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    select = ConvoMode.ConvoBoxes.boxIn(self.box_selected, event.pos)
                    if select != ConvoMode.ConvoBoxes.elsewhere:
                        self.box_selected = select
                        self._buttonPress()
                elif event.button == 4:
                    self.text_rect.move_ip(0, -ConvoMode.SCROLL_AMOUNT_MOUSE)
                elif event.button == 5:
                    self.text_rect.move_ip(0, ConvoMode.SCROLL_AMOUNT_MOUSE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._buttonPress()
                elif event.key == pygame.K_UP:
                    self.y_scroll['up'] = ConvoMode.SCROLL_AMOUNT_KEY
                elif event.key == pygame.K_DOWN:
                    self.y_scroll['down'] = ConvoMode.SCROLL_AMOUNT_KEY
                else:
                    self.box_selected = ConvoMode.ConvoBoxes.boxKey(self.box_selected, event.key)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.y_scroll['up'] = 0
                elif event.key == pygame.K_DOWN:
                    self.y_scroll['down'] = 0
                    
    def update(self):
        self.text_rect.move_ip(0, self.y_scroll['down'] - self.y_scroll['up'])
        
        self.text_rect.clamp_ip(self.surf_rect)
        
    def draw(self, screen):
        screen.fill((255,255,255))
        screen.blit(self.background, (0,0))
        screen.blit(self.surf_text, (16,16), self.text_rect)
        if self.box_selected != ConvoMode.ConvoBoxes.elsewhere:
            screen.blit(ConvoMode.black_box, self.box_selected)
            