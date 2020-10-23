from django.db import models
from django.conf import settings

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    question_text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)


class Update(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    update_text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
