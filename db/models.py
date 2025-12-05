from django.db import models


class Race(models.Model):
    races = [
        ("elf", "Elegant forest people"),
        ("dwarf", "Dwellers of the underground"),
        ("human", "Most populated race yet the most simple"),
        ("ork", "Mightiest fighters")
    ]

    name = models.CharField(max_length=255, choices=races, unique=True)
    description = models.TextField(blank=True, default="")


class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    bonus = models.CharField(max_length=255)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)


class Guild(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True, default="")


class Player(models.Model):
    nickname = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255)
    bio = models.CharField(max_length=255)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    guild = (
        models.ForeignKey(
            Guild, on_delete=models.SET_NULL, null=True
        )
    )
    created_at = models.DateTimeField(auto_now_add=True)
