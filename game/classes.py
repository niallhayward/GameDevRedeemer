import pygame
import os
import math
import data_handler as dh


class Game:
    def __init__(self, screen, settings, level, background, background_extras, player, enemies, player_projectiles, enemy_projectiles):
        self.screen = screen
        self.settings = settings
        self.level = level
        self.stage = 0
        self.background = background
        self.background_extras = background_extras
        self.player = player
        self.enemies = enemies
        self.player_projectiles = player_projectiles
        self.enemy_projectiles = enemy_projectiles
        self.pod = EnemyPod(self.fps, Enemy(*self.enemies[str(self.level)][str(self.stage)]), 3, 5)

    def render(self):
        self.background.scroll_background()
        for enemy in self.enemies:  fps, enemy, delay, size)
            self.screen.blit(enemy.image, (enemy.x, enemy.y))
        self.screen.blit(self.player.image, (self.player.x, self.player.y))  # Render player from player object
        for projectile in self.player_projectiles:  # Render player projectile objects from list
            self.screen.blit(projectile.image, (projectile.x, projectile.y))
        for projectile in self.enemy_projectiles:  # Render player projectile objects from list
            self.screen.blit(projectile.image, (projectile.x, projectile.y))

    def update(self):
        if self.pod.size > 0:
        if not self.enemies[str(self.level)][str(self.stage)]:
            self.stage += 1
        for enemy in self.enemies[str(self.level)][str(self.stage)]:
            if not enemy.move():
                self.enemies.remove(enemy)
        for projectile in self.player_projectiles:
            projectile.move()
        raise NotImplementedError

    def handle_events(self):
        raise NotImplementedError


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

    def draw_screen_menu(self, background_handler):
        for background in background_handler.background_list:
            self.screen.blit(background.image, (background.x, background.y))

    def draw_screen_game(self, player, enemy_list, player_projectiles, enemy_projectiles, background_handler):
        for background in background_handler.background_list:
            self.screen.blit(background.image, (background.x, background.y))
        self.screen.blit(player.image, (player.x, player.y))
        for bullet in player_projectiles:
            pygame.draw.rect(self.screen, (255, 0, 0), bullet.hitbox)
        for bullet in enemy_projectiles:
            pygame.draw.circle(self.screen, (255, 20, 157),
                               (bullet.x + (bullet.width / 2), bullet.y + (bullet.height / 2)),
                               bullet.width / 2)
        for enemy in enemy_list:
            self.screen.blit(enemy.image, (enemy.x, enemy.y))
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(10, 10, 140, 40))
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(14, 14, (132 * (player.health / 100)), 32))

    def draw_text(self, text, font, colour, x, y, centred):
        textobj = font.render(text, 1, colour)
        textrect = textobj.get_rect()
        if centred:
            x -= textrect.width // 2
        textrect.topleft = (x, y)
        self.screen.blit(textobj, textrect)
        return textrect


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
        self.image = dh.get_image(image, self.width, self.height)

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


class Background:
    def __init__(self, surface, fps, image, x, y, x_velocity, y_velocity, resolution, level):
        self.surface = surface
        self.fps = fps
        self.width = resolution[0]
        self.height = resolution[1]
        self.x = x
        self.y = y
        self.ori_x = x
        self.ori_y = y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.level = level
        self.rel_x = x % pygame.display.get_window_size()[1]
        self.rel_y = y % pygame.display.get_window_size()[1]
        self.image = dh.get_image(image, self.width, self.height)

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

    def scroll_background(self):
        if self.y_velocity > 0:
            self.surface.blit(self.image, (0, self.rel_y - self.height))
            if self.rel_y < pygame.display.get_window_size()[1]:
                self.surface.blit(self.image, (0, self.rel_y))
            self.set_y(self.y + self.y_velocity)
        if self.y_velocity < 0:
            self.surface.blit(self.image, (0, self.rel_y - self.height))
            if self.rel_y < pygame.display.get_window_size()[1]:
                self.surface.blit(self.image, (0, self.rel_y))
            self.set_y(self.y - self.y_velocity)
        if self.x_velocity < 0:
            self.surface.blit(self.image, (self.rel_x - self.width, 0))
            if self.rel_x < pygame.display.get_window_size()[0]:
                self.surface.blit(self.image, (self.rel_x, 0))
            self.set_x(self.x - self.x_velocity)
        if self.x_velocity > 0:
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


class BackgroundHandler:
    def __init__(self, background_list, background_objects):
        self.background_list = background_list
        self.background_objects = background_objects

    def move_backgrounds(self):
        for background in self.background_list:
            background.scroll_background()


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


