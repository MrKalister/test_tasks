import secrets

from django.core.validators import (MaxValueValidator, MinLengthValidator,
                                    MinValueValidator)
from django.db import models


def generate_unique_string():
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    while True:
        gen_string = ''.join(secrets.choice(alphabet) for _ in range(10))
        if not UniqueLogin.objects.filter(
                unique_string=gen_string).exists():
            break
    return gen_string


class UniqueLogin(models.Model):
    unique_string = models.CharField(
        max_length=10,
        unique=True,
        default=generate_unique_string
    )


class IQTestResult(models.Model):
    login = models.OneToOneField(
        UniqueLogin,
        on_delete=models.CASCADE,
        related_name='iq_test',
    )
    points = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(50)])
    timestamp = models.DateTimeField(auto_now_add=True)


class EQTestResult(models.Model):
    login = models.OneToOneField(
        UniqueLogin,
        on_delete=models.CASCADE,
        related_name='eq_test',
    )
    letters = models.JSONField(
        max_length=5,
        validators=[MinLengthValidator(5)]
    )
    timestamp = models.DateTimeField(auto_now_add=True)
