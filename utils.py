import pygame
from settings import *


def get_rel_mouse(mouse, offset):
    rel_mouse = (mouse[0]-offset[0], mouse[1]-offset[1])
    return rel_mouse


def draw_text(screen, text, size, color=WHITE, alignment='topleft', x=0, y=0, bold=False, italic=False):
    font = pygame.font.SysFont(FONT, size, bold, italic)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    setattr(text_rect, alignment, (x, y))
    screen.blit(text_surface, text_rect)
    return text_rect


# def draw_healthbar(game, health, max_health):
#     pct = health / max_health
#
#     if pct > .5:
#         col = GREEN
#     elif pct > .25:
#         col = YELLOW
#     else:
#         col = RED
#
#     mid_right = draw_text(game, 'Channel Health:', 15, WHITE, 'topleft', 5, 5).midright
#
#     if health > 0:
#         pygame.draw.rect(game.screen, col, (mid_right[0] + 5, mid_right[1] - 3, health, 10))
#     pygame.draw.rect(game.screen, WHITE, (mid_right[0] + 5, mid_right[1] - 3, max_health, 10), 1)


def text_objects(text, size, color=BLACK, bold=False, italic=False, bg=None):
    text_surface = pygame.font.SysFont(FONT, size, bold, italic).render(text, True, color, bg)
    return text_surface, text_surface.get_rect()


class TextLine:
    def __init__(self, string, color=BLACK, size=20, bold=False, italic=False, bg=None, return_val=None):
        self.string = string
        self.color = color
        self.size = size
        self.bold = bold
        self.italic = italic
        self.bg = bg
        self.return_val = return_val
        self.__image, self.rect = text_objects(self.string, self.size, self.color, self.bold, self.italic, self.bg)
        self.tooltip = None

    @property
    def image(self):
        if self.__image is None:
            self.__image, _ = text_objects(self.string, self.size, self.color, self.bold, self.italic, self.bg)
        return self.__image

    def clean(self):
        self.__image = None
        self.tooltip = None


class ToolTip:
    def __init__(self, text_list, o_color=None):
        # text_list is a list of TextLines
        self.text_list = text_list
        self.o_color = o_color
        self.w = 0
        self.h = 0
        for line in text_list:
            self.w = max(self.w, line.rect.w+2*2)  # pixel buffer of 2 on each side
            self.h += line.rect.h
        self.h += 2
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(WHITE)
        self.image.set_alpha(220)
        self.make()

    def make(self):
        y = 2
        for line in self.text_list:
            self.image.blit(line.image, (2, y, line.rect.w, line.rect.h))  # pixel buffer of 2
            y += line.rect.h
        if self.o_color:
            pygame.draw.rect(self, self.o_color, self.image.get_rect(), 1)

    def draw(self, surface, pos):
        new_pos = (min(pos[0]+10, surface.get_width()-self.w-1), max(1, pos[1]-self.h-10))
        surface.blit(self.image, new_pos)


class Log:
    def __init__(self, game):
        self.game = game
        self.text_list = []

    def add_text(self, text):
        self.text_list.append(text)
        if len(self.text_list) > LOG_MAX_LINES:
            del self.text_list[0]

    def draw(self):
        y = LOG_Y
        for text in self.text_list:
            draw_text(self.game.window, text, LOG_TEXT_SIZE, x=LOG_X, y=y)
            y += LOG_TEXT_SIZE + LOG_LINE_MARGIN


class Button:
    def __init__(self, textlines=None, text_color=BLACK, o_color=BLACK, bg_img=None,
                 bg_color=WHITE, auto_size=True, rect=None, w=0, h=0, return_value=True):
        self.textlines = textlines
        self.text_color = text_color
        self.o_color = o_color
        self.bg_img = bg_img
        self.bg_color = bg_color
        self.return_value = return_value
        self.text_width = 0
        self.text_height = 1
        if textlines:
            for textline in textlines:
                self.text_width = max(self.text_width, textline.rect.w + 2)
                self.text_height += textline.rect.h + 1

        self.image = None
        self.tooltip = None
        if not auto_size or bg_img:
            if rect:
                self.rect = pygame.Rect(rect)
            else:
                if bg_img:
                    self.rect = bg_img.get_rect()
                else:
                    self.rect = pygame.Rect(0, 0, w, h)
        else:
            self.make_rect()
        self.make_image()

    def change(self, attribute, val):
        self.__setattr__(attribute, val)
        self.make_image()

    def make_rect(self):
        self.rect = pygame.Rect(0, 0, self.text_width + 2, self.text_height + 2)

    def make_image(self):
        self.image = pygame.Surface((self.rect.w, self.rect.h))
        self.image.fill(self.bg_color)
        if self.bg_img:
            self.image.blit(self.bg_img, (0, 0))
        pygame.draw.rect(self.image, self.o_color, self.image.get_rect(), 1)
        y = (self.rect.h - self.text_height) / 2
        if self.textlines:
            for textline in self.textlines:
                draw_text(self.image, textline.string, textline.size, textline.color, 'midtop',
                          int(self.rect.w/2), y, textline.bold, textline.italic)
                y += textline.rect.h + 1
