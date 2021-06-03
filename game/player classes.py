import pygame
import data_handler as dh
import math
import 

class Player:
    def __init__(self, image, image_rotation, size, coordinates, velocity, health, immunity_delay):
        self.size = size
        self.coordinates = coordinates
        self.velocity = velocity
        self.health = health
        self.immunity_delay = immunity_delay
        self.immunity_delay_remaining = immunity_delay
        self.image = pygame.transform.rotate(dh.get_image(image, self.size), image_rotation)
        self.ammo_box =

    def get_hitbox(self):
        return pygame.Rect(self.coordinates, self.size)

    def move(self, keys_pressed):
        if keys_pressed[pygame.K_a] and self.coordinates[0] - self.velocity[0] > 0:  # LEFT
            self.coordinates[0] -= self.velocity[0]
        if keys_pressed[pygame.K_d] and self.coordinates[0] + self.size[0] + self.velocity[0] < pygame.display.get_window_size()[
                0]:  # RIGHT
            self.coordinates[0] += self.velocity[0]
        if keys_pressed[pygame.K_w] and self.coordinates[1] - self.velocity[1] > 0:  # UP
            self.coordinates[1] -= self.velocity[1]
        if keys_pressed[pygame.K_s] and self.coordinates[1] + self.size[1] + self.velocity[1] < pygame.display.get_window_size()[
                1]:  # DOWN
            self.coordinates[1] += self.velocity[1]

    def fire_projectile_primary(self, keys_pressed, player_projectiles_primary):
        if not player_projectiles_primary:
            if keys_pressed[pygame.K_SPACE]:
                projectile = Projectile(self.surface, self.x + (self.width / 2), self.y - (self.height / 10), 5, 10,
                                        (255, 0, 0), 0,
                                        6, self.fps, 1)
                player_projectiles_primary.append(projectile)
                pass
        else:
            if keys_pressed[pygame.K_SPACE] and 100 < self.y - player_projectiles_primary[-1].y:
                projectile = Projectile(self.surface, self.x + (self.width / 2), self.y - (self.height / 10), 5, 10,
                                        (255, 0, 0), 0,
                                        6, self.fps, 1)
                player_projectiles_primary.append(projectile)
        return player_projectiles_primary

    def reset_immunity_delay(self):
        self.immunity_delay_remaining = self.immunity_delay