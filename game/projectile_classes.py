import copy
import pygame
import data_handler


class Projectile:
    def __init__(self, image, image_rotation, coordinates, size, colour, velocity, damage):
        self.coordinates = coordinates
        self.size = size
        self.colour = colour
        self.velocity = velocity
        self.last_coordinates = coordinates
        self.damage = damage
        self.image = pygame.transform.rotate(
            data_handler.get_image(image, self.size), image_rotation)

    def update_coordinates(self, coordinates):
        self.coordinates = coordinates

    def get_hitbox(self):
        return pygame.Rect(self.coordinates, self.size)

    def move(self):
        self.coordinates[0] += self.velocity[0]
        self.coordinates[1] += self.velocity[1]
        return self.is_on_screen()

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


class TrackingProjectile(Projectile):
    def __init__(self, image, image_rotation, coordinates, size, colour, velocity, target_object,
                 tracking_duration, damage, fps):
        Projectile.__init__(self, image, image_rotation, coordinates, size, colour, velocity, damage)
        self.target = target_object.coordinates
        self.tracking_duration = tracking_duration * fps

    def set_duration(self, duration):
        self.tracking_duration = duration

    def move(self):
        if self.tracking_duration <= 0:
            self.coordinates[0] += self.velocity[0]
            self.coordinates[1] += self.velocity[1]
        else:
            if self.coordinates[0] > self.target.coordinates[0]:
                self.coordinates -= self.velocity[0]
            if self.coordinates[0] < self.target.coordinates[0]:
                self.coordinates += self.velocity[0]
            if self.coordinates[0] > self.target.coordinates[0]:
                self.coordinates -= self.velocity[0]
            if self.coordinates[0] < self.target.coordinates[0]:
                self.coordinates += self.velocity[0]
        self.set_duration(self.tracking_duration - 1)
        return self.is_on_screen()

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


class Weapon:
    def __init__(self, fps, projectile, delay, quantity):
        self.fps = fps
        self.projectile = projectile
        self.delay = delay * fps
        self.time_since_last_spawn = delay * fps
        self.quantity = quantity

    def spawn_projectile(self, player_coordinates):
        if self.quantity < 0:
            if self.delay < self.time_since_last_spawn:
                self.time_since_last_spawn = 0
                self.projectile[2] = [player_coordinates[0], player_coordinates[1]]
                self.time_since_last_spawn += 1
                return Projectile(*copy.deepcopy(self.projectile))
        if self.quantity > 0:
            if self.delay < self.time_since_last_spawn:
                self.time_since_last_spawn = 0
                self.quantity -= 1
                self.time_since_last_spawn += 1
                return Projectile(*copy.deepcopy(self.projectile))
        self.time_since_last_spawn += 1
