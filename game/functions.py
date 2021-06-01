import pygame
import os
import json


def is_on_surface(entity, surface):  # Takes a class object with (x, y) parameters and returns True if within surface
    if entity.y <= -entity.height:
        return False
    if entity.y >= surface.get_height():
        return False
    if entity.x <= -entity.width:
        return False
    if entity.x >= surface.get_width():
        return False
    else:
        return True


