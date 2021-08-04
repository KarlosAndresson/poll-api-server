from rest_framework import serializers
from apps.api.models import Poll, Question, Option, UserAnswer
from django.conf import settings


class PollSerializer(serializers.ModelSerializer):
    started_at = serializers.DateTimeField(input_formats=[settings.INPUT_DATE_TIME_FORMAT, 'input_dt'], required=False)

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

