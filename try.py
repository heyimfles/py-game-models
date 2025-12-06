import init_django_orm  # noqa: F401
import json

from db.models import Race, Skill, Player, Guild


def create_race(players: dict) -> list:
    race_instances = []
    for player in players:
        if players.get(player).get("race"):
            race, created = Race.objects.get_or_create(
                name=players.get(player).get("race").get("name"),
                defaults={
                    "description": (
                        players.get(player).get("race").get("description")
                    )
                }
            )
            race_instances.append(race)
        else:
            raise Exception("Race not found")
    return race_instances


def create_skills(players: dict, races: list) -> None:
    for player in players:
        if players.get(player).get("race").get("skills"):
            for name_bonus in players.get(player).get("race").get("skills"):
                race_of_this_player = (
                    players.get(player).get("race").get("name")
                )
                race_obj = None
                for race in races:
                    if race.name == race_of_this_player:
                        race_obj = race
                if race_obj is None:
                    raise Exception("Race not found")
                skill, created = Skill.objects.get_or_create(
                    name=name_bonus.get("name"),
                    defaults={
                        "bonus": name_bonus.get("bonus"),
                        "race": race_obj
                    }
                )


def create_guild(players: dict) -> list:
    guild_instances = []
    for player in players:
        if players.get(player).get("guild"):
            guild, created = Guild.objects.get_or_create(
                name=players.get(player).get("guild").get("name"),
                defaults={
                    "description": (
                        players.get(player).get("guild").get("description")
                    )
                }
            )
            guild_instances.append(guild)
    return guild_instances


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

    races = create_race(players_file)
    create_skills(players_file, races)
    guilds = create_guild(players_file)
    create_player(players_file, races, guilds)


if __name__ == "__main__":
    main()