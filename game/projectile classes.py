import pygame
import data_handler as dh


class Projectile:
    def __init__(self, image, image_rotation, coordinates, size, colour, velocity, damage):
        self.image = pygame.transform.rotate(
            dh.get_image(image, self.size), image_rotation)
        self.coordinates = coordinates
        self.size = size
        self.colour = colour
        self.velocity = velocity
        self.last_coordinates = coordinates
        self.damage = damage

    def update_coordinates(self, coordinates):
        self.coordinates = coordinates

    def get_hitbox(self):
        return pygame.Rect(self.coordinates, self.size)

    def move(self):
        self.coordinates[0] += self.velocity[0]
        self.coordinates[1] += self.velocity[1]


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


class AmmoBox:
    def __init__(self, fps, projectile, delay, size):
        self.fps = fps
        self.projectile = projectile
        self.delay = delay * fps
        self.time_since_last_spawn = delay
        self.size = size
        self.current_projectiles = []

    def spawn_projectile(self):
        if self.size < 0:
            if self.delay == self.time_since_last_spawn:
                self.time_since_last_spawn = 0
                self.current_projectiles.append(self.projectile)
        if self.size > 0:
            if self.delay == self.time_since_last_spawn:
                self.time_since_last_spawn = 0
                self.size -= 1
                self.current_projectiles.append(self.projectile)
        self.time_since_last_spawn += 1

    def get_projectiles(self):
        return self.current_projectiles

    def remove_projectile(self, projectile):
        self.current_projectiles.remove(projectile)


