from rest_framework import serializers
from apps.api.models import Poll, Question, Option, UserAnswer


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = 'id', 'name', 'started_at', 'ended_at', 'description', 'is_active', 'questions'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = 'id', 'description', 'poll', 'type', 'options'


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = 'id', 'description', 'question', 'answers'


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = 'id', 'user', 'option', 'text'

