import pygame
import itertools
from pygame.locals import *

import railsim
from railsim import maps


def init_screen(width, height):
    return pygame.display.set_mode((width, height), pygame.RESIZABLE)


BACKGROUND_COLOR = 122, 146, 158


class Game(object):
    def __init__(self):
        self.running = False
        self.view = None

    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((800, 800))
        screen.fill((0, 0, 0))
        pygame.display.flip()

        # SCAFFOLD
        data = railsim.maps.HexMap()
        for coords in itertools.product(range(20), range(20)):
            coords = maps.oddr_to_axial(coords)
            data.add_cell(coords, maps.Cell())
        self.view = railsim.views.HexMapView(data)

        _flip = pygame.display.flip

        self.running = True
        try:
            while self.running:
                td = clock.tick(60)
                self.handle_input()
                self.update(td)
                self.draw(screen)
                _flip()

        except KeyboardInterrupt:
            self.running = False

    def draw(self, surface):
        surface.fill(BACKGROUND_COLOR)
        self.view.render(surface, surface.get_rect())

    def update(self, td):
        #self.view.hex_radius += td / 100.
        pass

    def get_nearest_cell(self, coords):
        try:
            coords = maps.pixel_to_axial(
                self.view.point_from_surface(coords), self.view.hex_radius)
        except Exception:
            return None

        cell = None
        if coords:
            cell = self.view.data.get_nearest_cell(coords)

        return cell

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                break

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    break

            elif event.type == VIDEORESIZE:
                init_screen(event.w, event.h)

            elif event.type == MOUSEMOTION:
                cell = self.get_nearest_cell(event.pos)
                if cell:
                    self.view.highlight_cell(cell)

            elif event.type == MOUSEBUTTONUP:
                cell = self.get_nearest_cell(event.pos)
                if cell:
                    self.view.select_cell(cell)
