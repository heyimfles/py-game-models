from django.db.models import Model

import init_django_orm  # noqa: F401
import json

from db.models import Race, Skill, Player, Guild


def find_the_dict(initial_dict: dict, lookup_name: str) -> dict:
    result_dict = {}
    for item in initial_dict:
        if initial_dict.get(item).get(lookup_name):
            result_dict[item] = initial_dict.get(item).get(lookup_name)
    return result_dict


def get_or_create_race_guild(
        players: dict,
        key_to_find_the_dict: str,
        model: Model,
        description: str = "description"
) -> list:
    result_list = []
    our_dict = find_the_dict(players, key_to_find_the_dict)
    for player in our_dict:
        if our_dict.get(player) is not None:
            instance, created = model.objects.get_or_create(
                name=our_dict.get(player).get("name"),
                defaults={
                    description: our_dict.get(player).get(description)
                }
            )
            result_list.append(instance)
    return result_list


def create_skill(players: dict, races: list) -> None:
    race_dict = find_the_dict(players, "race")
    skill_dict = find_the_dict(race_dict, "skills")
    for player, skills in skill_dict.items():
        race_name = race_dict[player].get("name")
        race_obj = next((r for r in races if r.name == race_name), None)
        if not race_obj:
            raise Exception("Race not found")
        if skills:
            for skill in skills:
                instance, created = Skill.objects.get_or_create(
                    name=skill["name"],
                    defaults={
                        "bonus": skill["bonus"],
                        "race": race_obj
                    }
                )


def create_player(players: dict, races: list, guilds: list) -> None:
    for player in players:
        race_obj = None
        guild_obj = None
        race_of_this_player = players.get(player).get("race").get("name")
        for race in races:
            if race.name == race_of_this_player:
                race_obj = race
        if race_obj is None:
            raise Exception("Race not found")
        if players.get(player).get("guild"):
            guild_of_this_player = players.get(player).get("guild").get("name")
            for guild in guilds:
                if guild.name == guild_of_this_player:
                    guild_obj = guild
        name, created = Player.objects.get_or_create(
            nickname=player,
            defaults={
                "email": players.get(player).get("email"),
                "bio": players.get(player).get("bio"),
                "race": race_obj,
                "guild": guild_obj
            }
        )


def main() -> None:
    with open("players.json") as f:
        players_file = json.load(f)

    races = get_or_create_race_guild(players_file, "race", Race)
    guilds = get_or_create_race_guild(players_file, "guild", Guild)
    create_skill(players_file, races)
    create_player(players_file, races, guilds)


if __name__ == "__main__":
    main()
