import copy
import math
import random
import pygame
import data_handler
import projectile_classes


class Enemy:
    def __init__(self, fps, image, health, coordinates, velocity, size, image_rotation, move_type,
                 attack_type):
        self.health = health
        self.coordinates = tuple(coordinates)  # List [x, y]
        self.ori_coordinates = tuple(copy.deepcopy(coordinates))
        self.velocity = tuple(velocity)  # Vector List [x, y]
        self.size = tuple(size)  # List indicating width and height [x, y]
        self.points_value = health * 100  # Points awarded to player for destroying
        self.move_type = move_type
        self.attack_type = attack_type
        self.image = pygame.transform.rotate(
            data_handler.get_image(image, self.size), image_rotation)
        self.weapon = projectile_classes.Weapon(fps, ["redbullet", 0,
                                       (self.coordinates[0] + (self.size[0] / 2), self.coordinates[1]), (6, 18),
                                       (255, 0, 0), (0, 4), 1], 1.5, -1)

    def set_health(self, health):
        if health is int:
            self.health = health
        else:
            raise TypeError

    def get_health(self):
        return self.health

    def set_coordinates(self, coordinates):
        self.set_coordinate_x(coordinates[0])
        self.set_coordinate_y(coordinates[1])

    def get_coordinates(self):
        return self.coordinates

    def set_coordinate_x(self, new_coordinate_x):
        if new_coordinate_x is int or float:
            self.coordinates = (new_coordinate_x, self.coordinates[1])
        else:
            raise TypeError

    def get_coordinate_x(self):
        return self.coordinates[0]

    def set_coordinate_y(self, new_coordinate_y):
        if new_coordinate_y is int or float:
            self.coordinates = (self.coordinates[0], new_coordinate_y)
        else:
            raise TypeError

    def get_coordinate_y(self):
        return self.coordinates[1]

    def set_velocity(self, velocity):
        if velocity is tuple:
            self.velocity = velocity
        else:
            raise TypeError

    def get_velocity(self):
        return self.velocity

    def set_velocity_x(self, new_velocity_x):
        if new_velocity_x is int or float:
            self.velocity = (new_velocity_x, self.velocity[1])
        else:
            raise TypeError

    def get_velocity_x(self):
        return self.velocity[0]

    def set_velocity_y(self, new_velocity_y):
        if new_velocity_y is int or float:
            self.velocity = (self.velocity[0], new_velocity_y)
        else:
            raise TypeError

    def get_velocity_y(self):
        return self.velocity[1]

    def set_size(self, new_size):
        if new_size is tuple:
            self.size = new_size
        else:
            return TypeError

    def get_size(self):
        return self.size

    def get_width(self):
        return self.size[0]

    def get_height(self):
        return self.size[1]

    def set_points_value(self, points_value):
        if points_value is int:
            self.points_value = points_value
        else:
            raise TypeError

    def get_points_value(self):
        return self.points_value

    def get_hitbox(self):
        return pygame.Rect(self.coordinates, self.size)

    def move_linear(self):
        self.set_coordinates((self.coordinates[0] + self.velocity[0], self.coordinates[1] + self.velocity[1]))

    def move_vertical_wave(self, wave_range):
        boundaries = (self.ori_coordinates[0], self.ori_coordinates[0] + wave_range)
        self.set_coordinate_y(self.coordinates[1] + self.velocity[1])
        self.set_coordinate_x((((math.sin(self.coordinates[1] / 50) + 1) * (wave_range / 2)) + boundaries[0]))

    def move_horizontal_wave(self, wave_range):
        boundaries = (self.ori_coordinates[1], self.ori_coordinates[1] + wave_range)
        self.set_coordinate_x(self.coordinates[0] + self.velocity[0])
        self.set_coordinate_y((((math.sin(self.coordinates[0] / 50) + 1) * (wave_range / 2)) + boundaries[1]))

    def move_arc(self):  # Needs cleaning up
        if self.get_coordinate_x() < pygame.display.get_window_size()[0] - 200:
            self.set_coordinate_y(self.coordinates[1] + self.velocity[1])
            self.set_coordinate_x((130000 / self.coordinates[1]) - 100)
        else:
            self.set_coordinate_y(self.coordinates[1] - self.velocity[1])

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
        if self.move_type == "Arc":
            self.move_arc()
            return self.is_on_screen()
        if self.move_type == "Vertical Wave":
            self.move_vertical_wave(pygame.display.get_window_size()[0] / 4)
            return self.is_on_screen()
        if self.move_type == "Horizontal Wave":
            self.move_horizontal_wave(pygame.display.get_window_size()[1] / 8)
            return self.is_on_screen()
        if self.move_type == "First Boss":
            self.move_boss()
            return True

    def is_on_screen(self):
        if self.coordinates[0] + self.size[0] + 10 < 0:
            return False
        if self.coordinates[1] + self.size[1] + 10 < 0:
            return False
        if self.coordinates[0] > pygame.display.get_window_size()[0] + 100:
            return False
        if self.coordinates[1] > pygame.display.get_window_size()[1] + 100:
            return False
        else:
            return True

    def fire_projectile_primary(self):
        if self.attack_type == "Projectile":
            return self.weapon.spawn_projectile(
                [self.coordinates[0] + (self.size[0] / 2), self.coordinates[1] + self.size[1]])

    def fire_projectile_tracking(self, enemy_projectiles_primary, target):
        # if self.y % (pygame.display.get_window_size()[1] / 5) == 0:
        raise NotImplementedError


class EnemyPod:
    def __init__(self, fps, enemy, delay, size, spawn_type):
        self.fps = fps
        self.enemy = enemy
        self.delay = delay * fps  # Converts delay in seconds into delay in frames
        self.size = size
        self.time_since_last_spawn = delay
        self.pod = []
        self.projectiles = []
        self.spawn_type = spawn_type

    def spawn(self):  # Returns enemy if size not 0 and delay time has passed since last spawn
        if self.spawn_type == "Scatter":
            self.scatter_spawn()
        else:
            if self.size > 0 and self.delay < self.time_since_last_spawn:
                self.time_since_last_spawn = 0
                self.size -= 1
                self.pod.append(Enemy(*copy.deepcopy(self.enemy)))
            else:
                self.time_since_last_spawn += 1

    def scatter_spawn(self):
        if self.size > 0 and self.delay < self.time_since_last_spawn:
            self.time_since_last_spawn = 0
            self.size -= 1
            new_enemy = Enemy(*copy.deepcopy(self.enemy))
            new_enemy.set_coordinate_x(random.randrange(new_enemy.coordinates[0] - 200, new_enemy.coordinates[0] + 200))
            new_enemy.ori_coordinates = new_enemy.coordinates
            self.pod.append(new_enemy)
        else:
            self.time_since_last_spawn += 1

    def move_all(self):
        for enemy in self.pod:
            if not enemy.move():
                self.pod.remove(enemy)

    def update_projectiles(self):
        for projectile in self.projectiles:
            if not projectile.move():
                self.projectiles.remove(projectile)
        for enemy in self.pod:
            self.projectiles.append(enemy.fire_projectile_primary())
            if not self.projectiles[-1]:
                del self.projectiles[-1]
