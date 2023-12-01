import data_handler as dh


def add_new_level(filename, level):
    enemy_dict = dh.get_dict(filename)
    if str(level) in enemy_dict:
        raise KeyError
    else:
        enemy_dict[str(level)] = {}
        dh.write_to_json(enemy_dict, filename)


def add_new_stage(filename, level, stage):
    enemy_dict = dh.get_dict(filename)
    if str(level) in enemy_dict:
        enemy_dict[str(level)].update({str(stage): {}})
        dh.write_to_json(enemy_dict, filename)
    else:
        raise KeyError


def add_new_enemy_pod(filename, level, stage, enemy_list, delay, size):
    enemy_dict = dh.get_dict(filename)
    if len(enemy_list) == 8:
        if str(level) in enemy_dict:
            if not enemy_dict[str(level)]:
                raise KeyError
            else:
                if str(stage) in enemy_dict[str(level)]:
                    enemy_dict[str(level)][str(stage)].update({"Enemy": enemy_list})
                    enemy_dict[str(level)][str(stage)].update({"Delay": delay})
                    enemy_dict[str(level)][str(stage)].update({"Size": size})
                    dh.write_to_json(enemy_dict, filename)
        else:
            raise KeyError
    else:
        raise AttributeError
