import pygame
import data_handler


class Background:
    def __init__(self, surface, fps, image, coordinates, velocity, size):
        self.surface = surface
        self.fps = fps
        self.size = size
        self.coordinates = coordinates
        self.ori_coordinates = coordinates
        self.velocity = velocity
        self.relative_coordinates = (
            coordinates[0] % pygame.display.get_window_size()[0], coordinates[1] % pygame.display.get_window_size()[1])
        self.image = data_handler.get_image(image, self.size)
        if self.velocity[0] == 0:
            self.time_x = False
        else:
            self.time_x = (pygame.display.get_window_size()[0] / abs(self.velocity[0])) / self.fps
        if self.velocity[1] == 0:
            self.time = False
        else:
            self.time_y = (pygame.display.get_window_size()[1] / abs(self.velocity[1])) / self.fps

    def scroll_background(self):
        if self.velocity[1] > 0:
            self.surface.blit(self.image, (0, self.relative_coordinates[1] - self.size[1]))
            if self.relative_coordinates[1] < pygame.display.get_window_size()[1]:
                self.surface.blit(self.image, (0, self.relative_coordinates[1]))
            self.coordinates[1] += self.velocity[1]
        if self.velocity[1] < 0:
            self.surface.blit(self.image, (0, self.relative_coordinates[1] - self.size[1]))
            if self.relative_coordinates[1] < pygame.display.get_window_size()[1]:
                self.surface.blit(self.image, (0, self.relative_coordinates[1]))
            self.coordinates[1] -= self.velocity[1]
        if self.velocity[0] < 0:
            self.surface.blit(self.image, (self.relative_coordinates[0] - self.size[0], 0))
            if self.relative_coordinates[0] < pygame.display.get_window_size()[0]:
                self.surface.blit(self.image, (self.relative_coordinates[0], 0))
            self.coordinates[0] -= self.velocity[0]
        if self.velocity[0] > 0:
            self.surface.blit(self.image, (self.relative_coordinates[0] - self.size[0], 0))
            if self.relative_coordinates[0] < pygame.display.get_window_size()[0]:
                self.surface.blit(self.image, (self.relative_coordinates[0], 0))
            self.coordinates[0] += self.velocity[0]
        if self.coordinates[0] == self.size[0]:
            self.coordinates[0] = 0
        if self.coordinates[1] == self.size[1]:
            self.coordinates[1] = 0
        self.relative_coordinates = [self.coordinates[0], self.coordinates[1]]

    def scroll_object(self, delay):
        self.surface.blit(self.image, (self.coordinates[0], self.coordinates[1]))
        self.coordinates[0] += self.velocity[0]
        self.coordinates[1] += self.velocity[1]
        if self.time_x != 0:
            if self.coordinates[0] > (pygame.display.get_window_size()[0] + abs(self.ori_coordinates[0]) + (
                    pygame.display.get_window_size()[0] * (delay / self.time_x))) or self.coordinates[0] < (
                    0 - abs(self.ori_coordinates[0]) - (pygame.display.get_window_size()[0] * (delay / self.time_x))):
                self.coordinates = self.ori_coordinates
        if self.time_y != 0:
            if self.coordinates[1] > (pygame.display.get_window_size()[1] + abs(self.ori_coordinates[1]) + (
                    pygame.display.get_window_size()[1] * (delay / self.time_y))) or self.coordinates[1] < (
                    0 - abs(self.ori_coordinates[1]) - (pygame.display.get_window_size()[1] * (delay / self.time_y))):
                self.coordinates = self.ori_coordinates


class BackgroundHandler:
    def __init__(self, background_list, background_objects):
        self.background_list = background_list
        self.background_objects = background_objects

    def move_backgrounds(self):
        for background in self.background_list:
            background.scroll_background()


class Explosion:  # This class is not drawing explosions in the right locations, it is off by between 0 - 100 pixels
    def __init__(self, surface, enemy):
        self.size = (enemy.size[0] * 3, enemy.size[1] * 3)
        self.surface = surface
        self.coordinates = (enemy.coordinates[0] - 50, enemy.coordinates[1] - 50)
        self.stage = 0
        self.image = data_handler.get_image("Explosion0", self.size)

    def explode(self):
        if self.stage <= 11:
            self.stage += 1
            self.image = data_handler.get_image("Explosion"+str(self.stage), self.size)
