from django.db import models


class Word(models.Model):
    pass


class Item(models.Model):
    text = models.TextField(default='')
    word = models.ForeignKey(Word,
                             on_delete=models.CASCADE,
                             default=None)
