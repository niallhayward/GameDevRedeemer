import pygame

import data_handler as dh
import projectile_classes as prc


class Player:
    def __init__(self, fps, image, image_rotation, size, coordinates, velocity, health, immunity_delay):
        self.size = size
        self.coordinates = coordinates
        self.velocity = velocity
        self.health = health
        self.immunity_delay = immunity_delay * fps
        self.immunity_delay_remaining = immunity_delay * fps
        self.image = pygame.transform.rotate(dh.get_image(image, self.size), image_rotation)
        self.weapon = prc.Weapon(fps, ["redbullet", 0,
                                       [self.coordinates[0], self.coordinates[1]], [8, 24], (255, 0, 0), [0, -5], 1],
                                 0.1, -1)
        self.projectiles = []

    def get_hitbox(self):
        return pygame.Rect(self.coordinates, self.size)

    def move(self, keys_pressed):
        if keys_pressed[pygame.K_a] and self.coordinates[0] - self.velocity[0] > 0:  # LEFT
            self.coordinates[0] -= self.velocity[0]
        if keys_pressed[pygame.K_d] and self.coordinates[0] + self.size[0] + self.velocity[0] < \
                pygame.display.get_window_size()[
                    0]:  # RIGHT
            self.coordinates[0] += self.velocity[0]
        if keys_pressed[pygame.K_w] and self.coordinates[1] - self.velocity[1] > 0:  # UP
            self.coordinates[1] -= self.velocity[1]
        if keys_pressed[pygame.K_s] and self.coordinates[1] + self.size[1] + self.velocity[1] < \
                pygame.display.get_window_size()[
                    1]:  # DOWN
            self.coordinates[1] += self.velocity[1]

    def fire_projectile_primary(self, keys_pressed):
        if keys_pressed[pygame.K_SPACE]:
            return self.weapon.spawn_projectile([self.coordinates[0] + (self.size[0] / 2), self.coordinates[1]])

    def is_immune(self):
        if self.immunity_delay_remaining != 0:
            self.immunity_delay_remaining -= 1
            return True
        else:
            self.reset_immunity_delay()
            return False

    def reset_immunity_delay(self):
        self.immunity_delay_remaining = self.immunity_delay

    def update(self, keys_pressed):
        self.move(keys_pressed)
        self.update_projectiles(keys_pressed)

    def update_projectiles(self, keys_pressed):
        for projectile in self.projectiles:
            if not projectile.move():
                self.projectiles.remove(projectile)
        self.projectiles.append(self.fire_projectile_primary(keys_pressed))
        if self.projectiles[-1] is None:
            del self.projectiles[-1]
