from django.db.models import Model

import init_django_orm  # noqa: F401
import json

from db.models import Race, Skill, Player, Guild


def get_dict(
        initial_dict: dict,
        field_to_look_for: str
) -> dict:
    return {
        name: info.get(field_to_look_for)
        for name, info in initial_dict.items()
    }


def get_fk(
        info: dict,
        instance_list: list,
        player: str
) -> Model|None:
    if info.get(player):
        fk_name = info.get(player).get("name")
        for instance in instance_list:
            if instance.name == fk_name:
                return instance
        return None
    else:
        return None


def get_or_create(
        dict_to_table: dict,
        model: Model,
        info_races: dict = None,
        instance_list: list = None
) -> list:
    instances = []
    for player, info in dict_to_table.items():
        if info is None:
            continue
        if isinstance(info, dict):
            info = [info]
        for item in info:
            defaults = {}
            if not instance_list:
                defaults["description"] = item.get("description")
            else:
                defaults = {
                    "bonus": item.get("bonus"),
                    "race": get_fk(info_races, instance_list, player)
                }
            instance, created = model.objects.get_or_create(
                name=item["name"],
                defaults=defaults
            )
            instances.append(instance)
    return instances


def create_player(
        players: dict,
        race_info: dict,
        races_inst: list,
        guild_info: dict,
        guild_inst: list
) -> None:
    for player, info in players.items():
        instance, created = Player.objects.get_or_create(
            nickname=player,
            defaults={
                "email": info.get("email"),
                "bio": info.get("bio"),
                "race": get_fk(
                    race_info, races_inst, player
                ),
                "guild": get_fk(
                    guild_info, guild_inst, player
                )
            }
        )
    return

def main() -> None:
    Player.objects.all().delete()
    Skill.objects.all().delete()
    Guild.objects.all().delete()
    Race.objects.all().delete()

    with open("players.json") as f:
        players_file = json.load(f)

    races = get_dict(players_file, "race")
    guilds = get_dict(players_file, "guild")
    skills = get_dict(races, "skills")
    races_inst = get_or_create(races, Race)
    guild_inst = get_or_create(guilds, Guild)
    get_or_create(skills, Skill, races, races_inst)
    create_player(players_file, races, races_inst, guilds, guild_inst)


if __name__ == "__main__":
    main()
