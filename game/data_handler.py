import json
import os
import pygame


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


def get_image(file_name, size):
    image = pygame.transform.scale(pygame.image.load(os.path.abspath(
        os.path.join(os.path.join((os.path.join(os.getcwd(), os.pardir, "data")), "images"),
                     file_name + '.png'))).convert_alpha(),
                                   size)
    return image


def get_sound(file_name, file_type):
    sound = pygame.mixer.Sound(os.path.abspath(
        os.path.join(os.path.join((os.path.join(os.getcwd(), os.pardir, "data")), "sounds"),
                     file_name + "." + file_type)))
    return sound


def get_music(file_name, file_type):
    music = os.path.abspath(
        os.path.join(os.path.join((os.path.join(os.getcwd(), os.pardir, "data")), "music"),
                     file_name + "." + file_type))
    return music


def create_enemy_pods(new_dict):  # THIS DOES NOT WORK BEYOND TWO NESTED DICTS
    all_enemy_pods = []
    for key in new_dict.keys():
        all_enemy_pods.append(new_dict[key])
    for element in all_enemy_pods:
        if type(element) is dict:
            new_list = []
            for key in element.keys():
                new_list.append(element[key])
            all_enemy_pods.append(new_list)
            all_enemy_pods.remove(element)
    return all_enemy_pods
