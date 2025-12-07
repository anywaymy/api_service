from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    text = models.TextField(help_text="текст вопроса")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50] + "..." if len(self.text) > 50 else self.text

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ('-created_at',)


class Answer(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="answers",
        help_text="Пользователь"
    )

    text = models.TextField(help_text="текст ответа")
    created_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(to=Question,
                                 on_delete=models.CASCADE,
                                 related_name="answers")

    def __str__(self):
        return f"{self.user_id}: {self.text[:50]}..."

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        ordering = ('-created_at',)
