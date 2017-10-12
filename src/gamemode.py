import pygame

class GameMode(object):
    """This is an abstract object for game modes.
    Children of this should implement _input, update, and draw.
    """
    shared = {}
    def __init__(self):
        """All game modes must know when they are done, and set the next mode."""
        self.next_mode = None
        self.__pressed_keys = set()

    def _input(self, event):
        raise NotImplementedError(
            self.__class__.__name__ + "._input(self, event)"
        )

    def __trackPressedKeys(self, event):
        if event.type == pygame.KEYDOWN:
            self.__pressed_keys.add(event.key)
        elif event.type == pygame.KEYUP:
            self.__pressed_keys.discard(event.key)

    def _keyStatus(self, key):
        return key in self.__pressed_keys

    def input_list(self, event_list):
        """All game modes can take in events."""
        for event in event_list:
            self.__trackPressedKeys(event)
            self._input(event)

    def update(self):
        """All game modes can update and can optionally return True to halt the game."""
        raise NotImplementedError(
            self.__class__.__name__ + ".update(self)"
        )

    def draw(self, screen):
        """All game modes can draw to the screen"""
        raise NotImplementedError(
            self.__class__.__name__ + ".draw(self, screen)"
        )
