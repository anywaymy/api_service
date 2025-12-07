from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (QuestionSerializer, AnswerSerializer,
                          UserRegistrationSerializer, UserLoginSerializer)
from .permissions import IsUserOrReadOnly, IsAdminOrReadOnly

from .models import Question, Answer


# Вьюха для регистрации
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        login(request, user)

        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        }, status=status.HTTP_201_CREATED)


# Вьюха для логина
class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        login(request, user)

        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'message': 'Вход выполнен'
        }, status=status.HTTP_200_OK)


# Вьюха для выхода
class UserLogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        logout(request)
        return Response({'message': 'Выход выполнен'})


# Вьюха для просмотра профиля
class CurrentUserView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email
            })
        return Response({'user': None})


# Вьюха для ответа для конкретного вопроса
class AnswerCreateAPIView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        question_id = self.kwargs.get('question_pk')
        return Answer.objects.filter(question_id=question_id)

    def get(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=self.kwargs.get('question_pk'))

        # Получаем вопрос и ответы
        question_serializer = QuestionSerializer(question)
        answers = self.get_queryset()
        answer_serializer = self.get_serializer(answers, many=True)

        return Response({
            'question': question_serializer.data,
            'existing_answers': answer_serializer.data
        }, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        question_id = self.kwargs.get('question_pk')
        question = get_object_or_404(Question, pk=question_id)
        serializer.save(question=question)


class AnswerDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAdminOrReadOnly,)


# Вьюха для создания/просмотра вопроса
class QuestionListAPIView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


# Вьюха для просмотра/удаления конкретного вопроса
class QuestionDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminOrReadOnly,)
