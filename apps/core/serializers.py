from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Question, Answer


# Тут Сериализатор регистрации пользователя
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'email': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user


# Тут Сериализатор логина пользователя
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # authenticate должен получить request
            user = authenticate(
                request=self.context.get('request'),  # ← ВАЖНО: передаём request
                username=username,
                password=password
            )

            if not user:
                raise serializers.ValidationError(
                    'Неверное имя пользователя или пароль',  # лучше общее сообщение
                    code='authorization'
                )

            if not user.is_active:
                raise serializers.ValidationError(
                    'Учетная запись отключена',
                    code='authorization'
                )

            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                'Необходимо указать имя пользователя и пароль',
                code='authorization'
            )


# Тут Сериализатор ответа
class AnswerSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'question')


# Тут Сериализатор Вопроса
class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'created_at', 'answers')
        read_only_fields = ('id', 'created_at')

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Текст вопроса не может быть пустым")
        return value


