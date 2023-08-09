# Django imports
from django.db import models
from django.conf import settings

# Module imports
from . import BaseModel

class Book(BaseModel):
    name = models.CharField(max_length=80, verbose_name="Book Name")
    desc = models.CharField(max_length=200, verbose_name="Book Desc")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owner_workspace",
    )

    def __str__(self):
        """Return name of the Book"""
        return self.name

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        db_table = "books"
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"], name="unique_user_book"
            )
        ]