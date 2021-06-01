import pygame
import os
import math
import data_handler as dh

class MainScreen:
    def __init__(self, settings_dict):
        self.resolution = tuple(settings_dict["Resolution"])
        self.fullscreen = settings_dict["FullScreen"]
        self.borderless = settings_dict["Borderless"]
        self.fps = settings_dict["FPS"]
        self.screen = None

    def start(self):
        if self.borderless:
            self.screen = pygame.display.set_mode(self.resolution, pygame.NOFRAME)
        else:
            self.screen = pygame.display.set_mode(self.resolution)

    def draw_screen(self, player, enemy_list, player_projectiles, enemy_projectiles):
        self.screen.blit(player.image, (player.x, player.y))
        for bullet in player_projectiles:
            pygame.draw.rect(self.screen, (255, 0, 0), bullet.hitbox)
        for bullet in enemy_projectiles:
            pygame.draw.circle(self.screen, (255, 20, 157),
                               (bullet.x + (bullet.width / 2), bullet.y + (bullet.height / 2)),
                               bullet.width / 2)
        for enemy in enemy_list:
            self.surface.blit(enemy.image, (enemy.x, enemy.y))
        pygame.draw.rect(self.surface, (0, 0, 0), pygame.Rect(10, 10, 140, 40))
        pygame.draw.rect(self.surface, (255, 0, 0), pygame.Rect(14, 14, (132 * (player.health / 100)), 32))
        pygame.display.update()


class Player:
    def __init__(self, surface, fps, image, width, height, x, y, x_velocity, y_velocity, health, immunity_delay):
        self.surface = surface
        self.fps = fps
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.health = health
        self.hitbox = pygame.Rect(x, y, self.width, self.height)
        self.immunity_delay = immunity_delay
        self.immunity_delay_remaining = immunity_delay
        self.image = dh.get_image(image, (self.width, self.height))

    def set_xy(self, x, y):
        self.x = x
        self.y = y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def move_hitbox(self, x, y):
        self.hitbox = pygame.Rect(x, y, self.width, self.height)

    def debug_hitbox(self):
        pygame.draw.rect(self.surface, (255, 0, 0), self.hitbox)

    def handle_movement(self, keys_pressed):
        if keys_pressed[pygame.K_a] and self.x - self.x_velocity > 0:  # LEFT
            self.x -= self.x_velocity
        if keys_pressed[pygame.K_d] and self.x + self.width + self.x_velocity < pygame.display.get_window_size()[
                0]:  # RIGHT
            self.x += self.x_velocity
        if keys_pressed[pygame.K_w] and self.y - self.y_velocity > 0:  # UP
            self.y -= self.y_velocity
        if keys_pressed[pygame.K_s] and self.y + self.height + self.y_velocity < pygame.display.get_window_size()[
                1]:  # DOWN
            self.y += self.y_velocity
        self.move_hitbox(self.x, self.y)

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


class Enemy:

    def __init__(self, surface, fps, name, health, x, y, x_velocity, y_velocity, width, height, rotation, move_type,
                 attack_type):
        self.surface = surface
        self.fps = fps
        self.name = name
        self.health = health
        self.x = x
        self.y = y
        self.ori_x = x
        self.ori_y = y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(x, y, width, height)
        self.value = health * 100
        self.move_type = move_type
        self.attack_type = attack_type
        self.image = pygame.transform.rotate(
            pygame.transform.scale(pygame.image.load(os.path.join("Assets", name)).convert_alpha(),
                                   (width, height)), rotation)

    def move_hitbox(self, x, y):
        self.hitbox = pygame.Rect(x, y, self.width, self.height)

    def debug_hitbox(self):
        pygame.draw.rect(self.surface, (255, 0, 0), self.hitbox)

    def move_linear(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.move_hitbox(self.x, self.y)

    def move_up_or_down_line(self, direction):
        if direction == "Down":
            self.y += self.y_velocity
        if direction == "Up":
            self.y -= self.y_velocity
        self.move_hitbox(self.x, self.y)

    def move_up_or_down_wave(self, direction, wave_range):
        boundary_left = self.ori_x
        boundary_right = self.ori_x + wave_range
        if direction == "Down":
            self.y += self.y_velocity
        if direction == "Up":
            self.y -= self.y_velocity
        self.x = (((math.sin(self.y / 50) + 1) * (boundary_right - boundary_left) / 2) + boundary_left)
        self.move_hitbox(self.x, self.y)

    def move_side_to_side_wave(self, wave_range):
        boundary_top = self.ori_y
        boundary_bottom = self.ori_y + wave_range
        if self.ori_x <= 0:
            self.x += self.x_velocity
        if self.ori_x > pygame.display.get_window_size()[0]:
            self.x -= self.x_velocity
        self.y = (((math.sin(self.x / 50) + 1) * (boundary_bottom - boundary_top) / 2) + boundary_top)
        self.move_hitbox(self.x, self.y)

    def move_boss(self):
        if self.y < 10:
            self.y += self.y_velocity
        else:
            if self.x < 10:
                self.x_velocity = -self.x_velocity
            if self.x > (pygame.display.get_window_size()[0] - (self.width + 10)):
                self.x_velocity = - self.x_velocity
            self.x += self.x_velocity
        self.move_hitbox(self.x, self.y)

    def move(self):
        if self.move_type == "Linear":
            self.move_linear()
            if self.x_velocity >= 0 and self.x > pygame.display.get_window_size()[0]:
                return False
            if self.x_velocity <= 0 and self.x < 0:
                return False
            if self.y_velocity >= 0 and self.y > pygame.display.get_window_size()[1]:
                return False
            if self.y_velocity <= 0 and self.y < 0:
                return False
            return True
        if self.move_type == "Down Line":
            self.move_up_or_down_line("Down")
            if self.y > pygame.display.get_window_size()[1]:
                return False
            else:
                return True
        if self.move_type == "Up Line":
            self.move_up_or_down_line("Up")
            if self.y + self.height < 0:
                return False
            else:
                return True
        if self.move_type == "Down Wave":
            self.move_up_or_down_wave("Down", pygame.display.get_window_size()[0] / 2)
            if self.y > pygame.display.get_window_size()[1]:
                return False
            else:
                return True
        if self.move_type == "Up Wave":
            self.move_up_or_down_wave("Up", pygame.display.get_window_size()[0] / 2)
            if self.y + self.height < 0:
                return False
            else:
                return True
        if self.move_type == "Right Wave":
            self.move_side_to_side_wave(pygame.display.get_window_size()[1] / 4)
            if self.x > pygame.display.get_window_size()[0]:
                return False
            else:
                return True
        if self.move_type == "Left Wave":
            self.move_side_to_side_wave(pygame.display.get_window_size()[1] / 4)
            if self.x + self.width < 0:
                return False
            else:
                return True
        if self.move_type == "First Boss":
            self.move_boss()
            return True

    def fire_projectile_primary(self, enemy_projectiles_primary):
        if self.x % (pygame.display.get_window_size()[0] / 10) == 0:
            projectile = Projectile(self.surface, self.x + (self.width / 2), self.y, 10, 10, (255, 20, 147), 0,
                                    10, self.fps, 1)
            enemy_projectiles_primary.append(projectile)
        return enemy_projectiles_primary

    def fire_projectile_tracking(self, enemy_projectiles_primary, target):
        if self.y % (pygame.display.get_window_size()[1] / 5) == 0:
            projectile = TrackingProjectile(self.surface, self.x + (self.width / 2), self.y, 10, 10,
                                            (255, 20, 147), 10, 10, target, 240, self.fps, 1)
            enemy_projectiles_primary.append(projectile)
        return enemy_projectiles_primary


class Projectile:
    def __init__(self, surface, x, y, width, height, colour, x_velocity, y_velocity, fps, damage):
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.hitbox = pygame.Rect(x, y, width, height)
        self.image = pygame.draw.rect(surface, colour, self.hitbox)
        self.last_x = 0
        self.last_y = 0
        self.x_accel = x_velocity
        self.y_accel = y_velocity
        self.fps = fps
        self.damage = damage

    def set_xy(self, x, y):
        self.x = x
        self.y = y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def move_hitbox(self, x, y):
        self.hitbox = pygame.Rect(x, y, self.width, self.height)

    def move(self, target):
        self.x += self.x_accel
        self.y += self.y_accel
        self.move_hitbox(self.x, self.y)


class TrackingProjectile(Projectile):
    def __init__(self, surface, x, y, width, height, colour, x_velocity, y_velocity, target_object,
                 tracking_duration, fps, damage):
        Projectile.__init__(self, surface, x, y, width, height, colour, x_velocity, y_velocity, fps, damage)
        self.target = (target_object.x, target_object.y)
        self.tracking_duration = tracking_duration

    def set_duration(self, duration):
        self.tracking_duration = duration

    def move(self, target):
        if self.tracking_duration <= 0:
            self.x += self.x_accel
            self.y += self.y_accel
        else:
            distance = (target.x - self.x, target.y - self.y)
            self.x += (distance[0] / (self.fps / (self.x_velocity / 16)))
            self.y += (distance[1] / (self.fps / (self.y_velocity / 16)))
            if self.tracking_duration == 10:
                self.last_x = self.x
                self.last_y = self.y
            if self.tracking_duration == 2:
                self.x_accel = (self.x - self.last_x) / 8
                self.y_accel = (self.y - self.last_y) / 8
        self.move_hitbox(self.x, self.y)
        self.set_duration(self.tracking_duration - 1)


class Background:
    def __init__(self, surface, fps, image, x, y, x_velocity, y_velocity, width, height, level):
        self.surface = surface
        self.fps = fps
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", image + ".png")).convert_alpha(),
                                            (width, height))
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.ori_x = x
        self.ori_y = y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.level = level
        self.rel_x = x % pygame.display.get_window_size()[1]
        self.rel_y = y % pygame.display.get_window_size()[1]
        if self.x_velocity == 0:
            self.time_x = False
        else:
            self.time_x = (pygame.display.get_window_size()[0] / abs(self.x_velocity)) / self.fps
        if self.y_velocity == 0:
            self.time = False
        else:
            self.time_y = (pygame.display.get_window_size()[1] / abs(self.y_velocity)) / self.fps

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_rel_x(self, x):
        self.rel_x = x % self.width

    def set_rel_y(self, y):
        self.rel_y = y % self.height

    def scroll_background(self, direction):
        if direction == "Down":
            self.surface.blit(self.image, (0, self.rel_y - self.height))
            if self.rel_y < pygame.display.get_window_size()[1]:
                self.surface.blit(self.image, (0, self.rel_y))
            self.set_y(self.y + self.y_velocity)
        if direction == "Up":
            self.surface.blit(self.image, (0, self.rel_y - self.height))
            if self.rel_y < pygame.display.get_window_size()[1]:
                self.surface.blit(self.image, (0, self.rel_y))
            self.set_y(self.y - self.y_velocity)
        if direction == "Left":
            self.surface.blit(self.image, (self.rel_x - self.width, 0))
            if self.rel_x < pygame.display.get_window_size()[0]:
                self.surface.blit(self.image, (self.rel_x, 0))
            self.set_x(self.x - self.x_velocity)
        if direction == "Right":
            self.surface.blit(self.image, (self.rel_x - self.width, 0))
            if self.rel_x < pygame.display.get_window_size()[0]:
                self.surface.blit(self.image, (self.rel_x, 0))
            self.set_x(self.x + self.x_velocity)
        self.set_rel_x(self.x)
        self.set_rel_y(self.y)
        if self.x == self.width:
            self.set_x(0)
        if self.y == self.height:
            self.set_y(0)

    def scroll_object(self, delay):
        self.surface.blit(self.image, (self.x, self.y))
        self.set_x(self.x + self.x_velocity)
        self.set_y(self.y + self.y_velocity)
        if self.time_x != 0:
            if self.x > (pygame.display.get_window_size()[0] + abs(self.ori_x) + (
                    pygame.display.get_window_size()[0] * (delay / self.time_x))) or self.x < (
                    0 - abs(self.ori_x) - (pygame.display.get_window_size()[0] * (delay / self.time_x))):
                self.set_x(self.ori_x)
                self.set_y(self.ori_y)
        if self.time_y != 0:
            if self.y > (pygame.display.get_window_size()[1] + abs(self.ori_y) + (
                    pygame.display.get_window_size()[1] * (delay / self.time_y))) or self.y < (
                    0 - abs(self.ori_y) - (pygame.display.get_window_size()[1] * (delay / self.time_y))):
                self.set_x(self.ori_x)
                self.set_y(self.ori_y)


class PodHandler:
    def __init__(self, enemy_list, pod_duration):
        self.enemy_list = enemy_list
        self.pod_duration = pod_duration
        self.timer = 0
        self.complete = False


class StateHandler:
    def __init__(self, player, enemy_list, player_projectiles, enemy_projectiles, surface):
        self.player = player
        self.enemy_list = enemy_list
        self.player_projectiles = player_projectiles
        self.enemy_projectiles = enemy_projectiles
        self.enemy_destroyed_list = []
        self.surface = surface
        self.enemy_contact_damage = 10

    def on_surface(self, entity):  # Takes a class object with (x, y) parameters and returns True if within surface
        if entity.y <= -entity.height:
            return False
        if entity.y >= self.surface.get_height():
            return False
        if entity.x <= -entity.width:
            return False
        if entity.x >= self.surface.get_width():
            return False
        else:
            return True

    def move_entities(self):
        for bullet in self.player_projectiles:
            bullet.set_y(bullet.y + bullet.y_velocity)
            bullet.move_hitbox(bullet.x, bullet.y)
        for bullet in self.enemy_projectiles:
            bullet.move(self.player)
        for enemy in self.enemy_list:
            if not enemy.move():
                self.enemy_list.remove(enemy)

    def check_enemy_collisions(self):
        for enemy in self.enemy_list:
            if enemy.hitbox.colliderect(self.player.hitbox):
                if self.player.immunity_delay_remaining <= 0:
                    self.player.health -= self.enemy_contact_damage
                    self.player.reset_immunity_delay()
            for projectile in self.player_projectiles:
                projectile_on_surface = self.on_surface(projectile)
                if projectile.hitbox.colliderect(enemy.hitbox):
                    projectile_on_surface = False
                    enemy.health -= projectile.damage
                    if enemy.health == 0:
                        self.enemy_destroyed_list.append(enemy)
                        self.enemy_list.remove(enemy)
                if not projectile_on_surface:
                    self.player_projectiles.remove(projectile)
        self.player.immunity_delay_remaining -= 1  # PLACEHOLDER NEEDS VARIABLING

    def check_player_collisions(self):
        for projectile in self.enemy_projectiles:
            projectile_on_surface = self.on_surface(projectile)
            if self.player.hitbox.colliderect(projectile.hitbox):
                self.player.health -= 1  # PLACEHOLDER NEEDS VARIABLING
                projectile_on_surface = False
            if not projectile_on_surface:
                self.enemy_projectiles.remove(projectile)

    def check_all_collisions(self):
        self.check_player_collisions()
        self.check_enemy_collisions()
        return self.player, self.enemy_list, self.player_projectiles, self.enemy_projectiles

# class HitboxDebugger:
#     def __init__(self, player, enemy):
#         self.player = player
#         self.enemy = enemy
#
#     def get_player(self):
#         return self.player
#
#     def set_player(self, new_bool):
#         self.player = new_bool
#
#     def get_enemy(self):
#         return self.enemy
#
#     def set_enemy(self, new_bool):
#         self.enemy = new_bool
#
#     def enable_debug(self):
#         self.set_player(True)
#         self.set_enemy(True)
#
#     def disable_debug(self):
#         self.set_player(False)
#         self.set_enemy(False)
