import os
import pygame

from constants import *
from gamemode import *
from boxes import *

class ConvoMode(GameMode):
    class ConvoBoxes(Boxes):
        rects = [
            pygame.Rect(  8,  88,  88,  36),
            pygame.Rect(224,  88,  88,  36),
            pygame.Rect(  8, 132,  88,  36),
            pygame.Rect(224, 132,  88,  36),
        ]

        def keySelect(self, key):
            if key == pygame.K_LEFT:
                return self.changeSelect(-1)
            elif key == pygame.K_RIGHT:
                return self.changeSelect(1)

    SCROLL_AMOUNT_MOUSE = 10
    SCROLL_AMOUNT_KEY = 1
    sprite_path = os.path.join(GRAPHICS_DIRECTORY, BACKGROUNDS_DIRECTORY)
    black_box = pygame.image.load(os.path.join(sprite_path, 'blackbox.png'))
    converted = False

    def _textMain(self):
        # return text for main section
        raise NotImplementedError(self.__class__.__name__ + "._textMain(self)")
    def _textButton(self, index):
        # return text for button
        raise NotImplementedError(self.__class__.__name__ + "._textButton(self, index)")
    def _goButton(self, index):
        # do stuff for button
        raise NotImplementedError(self.__class__.__name__ + "._goButton(self, index)")

    def __init__(self):
        super(ConvoMode, self).__init__()
        if not ConvoMode.converted:
            ConvoMode.black_box = ConvoMode.black_box.convert_alpha()
            ConvoMode.converted = True
        self.background = pygame.image.load(os.path.join(ConvoMode.sprite_path, 'layout1boxes.png')).convert_alpha()
        # mainly, make the surfaces based on the text for view and buttons, fitting some criteria
        self.text_rect = pygame.Rect(0, 0, 288, 48)
        self.surf_text = self.shared['font_wrap'].renderInside(288, self._textMain(), False, TEXT_COLOR)
        for index, rect in enumerate(ConvoMode.ConvoBoxes.rects):
            self.shared['font_wrap'].renderToInside(
                self.background,
                ConvoMode.ConvoBoxes.textStart(index),
                ConvoMode.ConvoBoxes.textWidth(index),
                self._textButton(index),
                False,
                TEXT_COLOR
            )
        self.boxes = ConvoMode.ConvoBoxes()

        self.y_scroll = {'up': 0, 'down': 0}
        # what else do conversations need?

    def input(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEMOTION:
                self.boxes.posSelect(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.boxes.posSelect(event.pos) != None:
                        self._goButton(self.boxes.select)
                elif event.button == 4:
                    self.text_rect.move_ip(0, -ConvoMode.SCROLL_AMOUNT_MOUSE)
                elif event.button == 5:
                    self.text_rect.move_ip(0, ConvoMode.SCROLL_AMOUNT_MOUSE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._goButton(self.boxes.select)
                elif event.key == pygame.K_UP:
                    self.y_scroll['up'] = ConvoMode.SCROLL_AMOUNT_KEY
                elif event.key == pygame.K_DOWN:
                    self.y_scroll['down'] = ConvoMode.SCROLL_AMOUNT_KEY
                else:
                    self.boxes.keySelect(event.key)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.y_scroll['up'] = 0
                elif event.key == pygame.K_DOWN:
                    self.y_scroll['down'] = 0

    def update(self):
        self.text_rect.move_ip(0, self.y_scroll['down'] - self.y_scroll['up'])
        self.text_rect.clamp_ip(self.surf_text.get_rect())

    def draw(self, screen):
        screen.fill(WHITE)
        screen.blit(self.background, (0,0))
        screen.blit(self.surf_text, (16,16), self.text_rect)
        screen.blit(ConvoMode.black_box, self.boxes.getSelectRect())
