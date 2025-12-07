from django.urls import path
from .views import (QuestionListAPIView, QuestionDetailAPIView,
                    AnswerCreateAPIView, AnswerDetailAPIView,
                    UserRegistrationView, UserLoginView,
                    UserLogoutView, CurrentUserView)

app_name = "core"

urlpatterns = [
# Аутентификация
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', UserLoginView.as_view(), name='login'),
    path('auth/logout/', UserLogoutView.as_view(), name='logout'),
    path('auth/me/', CurrentUserView.as_view(), name='current-user'),

    # for Questions
    path('questions/', QuestionListAPIView.as_view(), name='questions-list'),
    path('questions/<int:pk>/',
         QuestionDetailAPIView.as_view(),
         name='question-detail'),

    # for Answers
    path('questions/<int:question_pk>/answers/',
         AnswerCreateAPIView.as_view(),
         name='answer-create'),
    path('answers/<int:pk>/',
         AnswerDetailAPIView.as_view(),
         name='answer-detail')
]