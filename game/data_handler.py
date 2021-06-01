import json
import pygame
import os
pygame.init()

def write_to_json(new_dict, file_name):
    with open(os.path.join(
            os.path.join(os.path.join(os.getcwd(), os.pardir, "data")), file_name + '.json'),
            'w') as outfile:
        json.dump(new_dict, outfile)


def get_dict(file_name):
    with open(os.path.join(
            os.path.join(os.path.join(os.getcwd(), os.pardir, "data")), file_name + '.json'),
            'r') as my_file:
        data = my_file.read()
    new_dict = json.loads(data)
    return new_dict


def get_image(file_name, width, height):
    image = pygame.transform.scale(pygame.image.load(os.path.abspath(
        os.path.join(os.path.join((os.path.join(os.getcwd(), os.pardir, "data")), "images"),
                     file_name + '.png'))).convert_alpha(),
                                   (width, height))
    return image


def get_sound(file_name, file_type):
    sound = pygame.mixer.Sound(os.path.abspath(
        os.path.join(os.path.join((os.path.join(os.getcwd(), os.pardir, "data")), "sounds"),
                     file_name + "." + file_type)))
    return sound


def get_music(file_name, file_type):
    return pygame.mixer.music.load(os.path.abspath(
        os.path.join(os.path.join((os.path.join(os.getcwd(), os.pardir, "data")), "music"),
                     file_name + "." + file_type)))


# total_enemies = []
# for level in enemy_dict.keys():
#     level_enemies = []
#     for pod in enemy_dict[level].keys():
#         new_enemies = []
#         pod_index = len(enemy_dict[level][pod])
#         while pod_index > 0:
#             for enemy in enemy_dict[level][pod]:
#                 enemy_index = len(enemy)
#                 new_enemy = [screen]
#                 while enemy_index > 0:
#                     for attribute in enemy:
#                         new_enemy.append(attribute)
#                         enemy_index -= 1
#                 new_enemies.append(Enemy(*new_enemy))
#                 pod_index -= 1
#         level_enemies.append(new_enemies)
#     total_enemies.append(level_enemies)
# return total_enemies
get_music("level1", "mp3")
