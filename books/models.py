from django.db import models

class Category(models.Model):
  name = models.CharField(max_length=255)

class Author(models.Model):
  name = models.CharField(max_length=255)

class Book(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
      indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['author']),
          ]
