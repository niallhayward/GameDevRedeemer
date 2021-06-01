import json
import pygame
import os


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


def convert_dict_to_list(new_dict):  # THIS DOES NOT WORK BEYOND TWO NESTED DICTS
    total_enemies = []
    for key in new_dict.keys():
        total_enemies.append(new_dict[key])
    for element in total_enemies:
        if type(element) is dict:
            new_list = []
            for key in element.keys():
                new_list.append(element[key])
            total_enemies.append(new_list)
            total_enemies.remove(element)
    return total_enemies

