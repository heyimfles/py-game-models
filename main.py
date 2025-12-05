import init_django_orm  # noqa: F401
import json

from db.models import Race, Skill, Player, Guild


def create_race(players: dict) -> list:
    race_instances = []
    for player in players:
        race, created = Race.objects.get_or_create(
            name=players.get(player).get("race")["name"],
            defaults={
                "description": players.get(player).get("race")["description"]
            }
        )
        race_instances.append(race)
    return race_instances


def create_skills(players: dict, races: list) -> None:
    for player in players:
        for name_bonus in players.get(player).get("race").get("skills"):
            race_of_this_player = players.get(player).get("race")["name"]
            for race in races:
                if race.name == race_of_this_player:
                    race_obj = race
            skill, created = Skill.objects.get_or_create(
                name=name_bonus["name"],
                defaults={
                    "bonus": name_bonus["bonus"],
                    "race": race_obj
                }
            )


def create_guild(players: dict) -> list:
    guild_instances = []
    for player in players:
        if players.get(player).get("guild"):
            guild, created = Guild.objects.get_or_create(
                name=players.get(player).get("guild")["name"],
                defaults={
                    "description": (
                        players.get(player).get("guild")["description"]
                    )
                }
            )
        guild_instances.append(guild)
    return guild_instances


def create_player(players: dict, races: list, guilds: list) -> None:
    for player in players:
        race_of_this_player = players.get(player).get("race")["name"]
        for race in races:
            if race.name == race_of_this_player:
                race_obj = race
        if players.get(player).get("guild"):
            guild_of_this_player = players.get(player).get("guild")["name"]
            for guild in guilds:
                if guild.name == guild_of_this_player:
                    guild_obj = guild
        else:
            guild_obj = None
        name, created = Player.objects.get_or_create(
            nickname=player,
            defaults={
                "email": players.get(player)["email"],
                "bio": players.get(player)["bio"],
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
