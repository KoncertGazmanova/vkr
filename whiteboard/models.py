# whiteboard/models.py
from django.db import models

class Note(models.Model):
    x = models.FloatField(default=0.0)
    y = models.FloatField(default=0.0)
    text = models.TextField(blank=True)
    # Можно добавить поля: ширина/высота, цвет, форма и т.д.

    def __str__(self):
        return f"Note {self.id}: {self.text[:20]}"

class Connection(models.Model):
    source = models.ForeignKey(Note, related_name="outgoing", on_delete=models.CASCADE)
    target = models.ForeignKey(Note, related_name="incoming", on_delete=models.CASCADE)
    # Можно хранить тип линии, направленность и др.
    def __str__(self):
        return f"Connection from Note {self.source.id} to {self.target.id}"
