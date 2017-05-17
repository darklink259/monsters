import pygame, os, cPickle
from constants import *
from gamemode import *

class GameMenuMode(GameMode):
    class State(object):
        Menu, Save, Load = range(3)
    def __init__(self, previous_mode):
        super(GameMenuMode, self).__init__()
        self.state = GameMenuMode.State.Menu
        self.old_screen = False
        self.previous_mode = previous_mode
        self.end_the_game = False

    def _resetCursorBlink(self):
        self.cursor_switch = True
        self.cursor_timer = 0

    def _clearSaveStuff(self):
        self.save_name = ''
        self.cursor_position = 0
        self._resetCursorBlink()

    def _saveGame(self):
        """Save the game."""
        objects = ['asd', (1,2,3), 123]
        if not os.path.exists(SAVE_DIRECTORY):
            os.makedirs(SAVE_DIRECTORY)
        with open(os.path.join(SAVE_DIRECTORY, self.save_name + '.sav'), 'wb') as f:
            cPickle.dump(objects, f, cPickle.HIGHEST_PROTOCOL)

    def _inputMenu(self, event):
        if event.type == pygame.QUIT:
            self.end_the_game = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_mode = self.previous_mode
            elif event.key == pygame.K_F1:
                self._clearSaveStuff()
                self.state = GameMenuMode.State.Save
            elif event.key == pygame.K_F2:
                self._clearSaveStuff()
                self.state = GameMenuMode.State.Load
            elif event.key == pygame.K_F3:
                self.end_the_game = True

    def _inputSave(self, event):
        if event.type == pygame.QUIT:
            self.state = GameMenuMode.State.Menu
        elif event.type == pygame.KEYDOWN:
            char = event.unicode
            length = len(self.save_name)
            if event.key == pygame.K_ESCAPE:
                self.state = GameMenuMode.State.Menu
            elif event.key == pygame.K_RETURN:# also call on a button press
                if self.save_name:
                    self._saveGame()
                    self.state = GameMenuMode.State.Menu
            elif event.key == pygame.K_LEFT:
                self.cursor_position = max(self.cursor_position-1, 0)
                self._resetCursorBlink()
            elif event.key == pygame.K_RIGHT:
                self.cursor_position = min(self.cursor_position+1, length)
                self._resetCursorBlink()
            elif event.key in (pygame.K_UP, pygame.K_HOME):
                self.cursor_position = 0
                self._resetCursorBlink()
            elif event.key in (pygame.K_DOWN, pygame.K_END):
                self.cursor_position = length
                self._resetCursorBlink()
            elif event.key == pygame.K_DELETE:
                self.save_name = self.save_name[:self.cursor_position] + self.save_name[self.cursor_position+1:]
                self._resetCursorBlink()
            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_position > 0:
                    self.save_name = self.save_name[:self.cursor_position-1] + self.save_name[self.cursor_position:]
                    self.cursor_position -= 1
                self._resetCursorBlink()
            elif length < 16 and ((char >= '0' and char <= '9' ) or (event.key > 96 and event.key < 123)):# numbers and letters
                self.save_name = self.save_name[:self.cursor_position] + char + self.save_name[self.cursor_position:]
                self.cursor_position += 1
                self._resetCursorBlink()

    def _inputLoad(self, event):
        if event.type == pygame.QUIT:
            self.state = GameMenuMode.State.Menu
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = GameMenuMode.State.Menu
            # put in scrolling to select save file? maybe typing too? alphebatized list...

    def input(self, event_list):
        if self.state is GameMenuMode.State.Menu:
            for event in event_list:
                self._inputMenu(event)
        elif self.state is GameMenuMode.State.Save:
            for event in event_list:
                self._inputSave(event)
        elif self.state is GameMenuMode.State.Load:
            for event in event_list:
                self._inputLoad(event)
        else:
            raise RuntimeError("incorrect: self.state = " + str(self.state))

    def update(self):
        if self.state is GameMenuMode.State.Menu:
            pass
        elif self.state is GameMenuMode.State.Save:
            if self.cursor_timer >= CURSOR_TIME:
                self.cursor_switch = not self.cursor_switch
                self.cursor_timer = 0
            self.cursor_timer += 1
        elif self.state is GameMenuMode.State.Load:
            pass
        else:
            raise RuntimeError("incorrect: self.state = " + str(self.state))
        return self.end_the_game

    def draw(self, screen):
        if not self.old_screen:
            self.old_screen = screen.copy()
        screen.blit(self.old_screen, (0,0))
        if self.state is GameMenuMode.State.Menu:
            disp_text = "Options:\n_Go Back (ESC)\n_Save (F1)\n_Load (F2)\n_Quit (F3)"
            self.shared['font_wrap'].renderToInside(screen, (0,0), 20 * FONT_SIZE, disp_text, False, WHITE, BLACK)
            # center this, make bigger and buttons... maybe
            # more to come
        elif self.state is GameMenuMode.State.Save:
            disp_text = "Options:\n_Go Back (ESC)\n_Save (ENTER)\nType a file name:\n"
            if self.save_name:
                disp_text += self.save_name
            disp_text += ".sav"
            self.shared['font_wrap'].renderToInside(screen, (0,0), 20 * FONT_SIZE, disp_text, False, WHITE, BLACK)
            if self.cursor_switch:
                screen.fill(WHITE, ((self.cursor_position * FONT_SIZE, 40), (1, 10)))
            # display prompt for file to save
            # display save_name in there
        elif self.state is GameMenuMode.State.Load:
            disp_text = "Options:\n_Go Back (ESC)\n_Load (ENTER)\nSelect a file name:\n"
            disp_text += ".sav"
            self.shared['font_wrap'].renderToInside(screen, (0,0), 20 * FONT_SIZE, disp_text, False, WHITE, BLACK)
            # draw load thingy
            pass
        else:
            raise RuntimeError("incorrect: self.state = " + str(self.state))
