import pygame
import data_handler as dh
import math


class Enemy:
    def __init__(self, image, health, coordinates, velocity, size, image_rotation, move_type,
                 attack_type):
        self.health = health
        self.coordinates = coordinates  # List [x, y]
        self.ori_coordinates = coordinates
        self.velocity = velocity  # Vector List [x, y]
        self.size = size  # List indicating width and height [x, y]
        self.value = health * 100  # Points awarded to player for destroying
        self.move_type = move_type
        self.attack_type = attack_type
        self.image = pygame.transform.rotate(
            dh.get_image(image, self.size), image_rotation)

    def get_hitbox(self):
        return pygame.Rect(self.coordinates, self.size)

    def move_linear(self):
        self.coordinates[0] += self.velocity[0]
        self.coordinates[1] += self.velocity[1]

    def move_up_or_down_wave(self, wave_range):
        boundaries = (self.ori_coordinates[0], self.coordinates[0] + wave_range)
        self.coordinates[1] += self.velocity[1]  # Update y coordinate
        self.coordinates[0] = (((math.sin(self.coordinates[1] / 50) + 1) * (boundaries[1] - boundaries[0]) / 2) + boundaries[0])

    def move_side_to_side_wave(self, wave_range):
        boundaries = (self.ori_coordinates[1], self.ori_coordinates[1] + wave_range)
        self.coordinates[0] += self.velocity[0]
        self.coordinates[1] = (((math.sin(self.coordinates[0] / 50) + 1) * (boundaries[0] - boundaries[1]) / 2) + boundaries[1])

    def move_boss(self):
        raise NotImplementedError
        # if self.y < 10:
        #     self.y += self.y_velocity
        # else:
        #     if self.x < 10:
        #         self.x_velocity = -self.x_velocity
        #     if self.x > (pygame.display.get_window_size()[0] - (self.width + 10)):
        #         self.x_velocity = - self.x_velocity
        #     self.x += self.x_velocity
        # self.move_hitbox(self.x, self.y)

    def move(self):
        if self.move_type == "Linear":
            self.move_linear()
            return self.is_on_screen()
        if self.move_type == "Vertical Wave":
            self.move_up_or_down_wave(pygame.display.get_window_size()[0] / 2)
            return self.is_on_screen()
        if self.move_type == "Horizontal Wave":
            self.move_side_to_side_wave(pygame.display.get_window_size()[1] / 4)
            return self.is_on_screen()
        if self.move_type == "First Boss":
            self.move_boss()
            return True

    def fire_projectile_primary(self, enemy_projectiles_primary):
        if self.x % (pygame.display.get_window_size()[0] / 10) == 0:
            raise NotImplementedError

    def fire_projectile_tracking(self, enemy_projectiles_primary, target):
        if self.y % (pygame.display.get_window_size()[1] / 5) == 0:
            raise NotImplementedError

    def is_on_screen(self):
        if self.coordinates[0] + self.size[0] < 0:
            return False
        if self.coordinates[1] + self.size[1] < 0:
            return False
        if self.coordinates[0] > pygame.display.get_window_size()[0]:
            return False
        if self.coordinates[1] > pygame.display.get_window_size()[1]:
            return False
        else:
            return True


class EnemyPod:
    def __init__(self, fps, enemy, delay, size):
        self.fps = fps
        self.enemy = enemy
        self.delay = delay * fps  # Converts delay in seconds into delay in frames
        self.size = size
        self.time_since_last_spawn = delay
        self.pod = []

    def spawn(self):  # Returns enemy if size not 0 and delay time has passed since last spawn
        if self.size > 0 and self.delay == self.time_since_last_spawn:
            self.time_since_last_spawn = 0
            self.size -= 1
            return self.enemy
        else:
            self.time_since_last_spawn += 1