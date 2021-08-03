from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from apps.api.models import Option, Poll, Question, UserAnswer
from apps.api.v1.filters import PollFilterSet, QuestionFilterSet, OptionFilterSet, UserAnswerFilterSet
from apps.api.v1.serializers import PollSerializer, QuestionSerializer, OptionSerializer, UserAnswerSerializer


class PollViewSet(ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PollFilterSet
    # permission_classes = [IsAuthenticated]


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.select_related('poll')
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuestionFilterSet
    # permission_classes = [IsAuthenticated]


class OptionViewSet(ModelViewSet):
    queryset = Option.objects.select_related('question')
    serializer_class = OptionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OptionFilterSet
    # permission_classes = [IsAuthenticated]


class UserAnswerViewSet(ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserAnswerFilterSet
    # permission_classes = [IsAuthenticated]


