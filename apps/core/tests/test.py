import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Question, Answer

# Реализация минимального теста
class MinimalTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_create(self):
        question = Question.objects.create(text='Вопрос?')
        self.assertEqual(Question.objects.count(), 1)

        answer = Answer.objects.create(
            question=question,
            text='Ответ',
            user=self.user
        )
        self.assertEqual(Answer.objects.count(), 1)

        question.delete()
        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(Answer.objects.count(), 0)