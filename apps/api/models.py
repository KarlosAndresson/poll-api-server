from enum import Enum
from django.contrib.auth.models import User
from django.db import models
from django.db.models import UniqueConstraint


class TimestampFields(models.Model):
    """Абстрактный класс прозрачно работающий в моделях, управляет датой создания и изменения записи"""
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


class Poll(TimestampFields):
    name = models.CharField(max_length=100)
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Poll'
        verbose_name_plural = 'Polls'

    def __str__(self):
        return f'{self.name}'


class QuestionType(Enum):
    TEXT = 'TEXT'
    RADIO = 'RADIO'
    CHECK = 'CHECK'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Question(TimestampFields):
    description = models.TextField()
    # вопрос должен быть привязан к одному, конкретному опросу, чтобы ответы в каждом опросе были свои
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')
    # тип привязываем ко всему вопросу, чтобы при необходимости можно было сменить radio box на check box
    type = models.CharField(max_length=10, choices=QuestionType.choices())

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return f'{self.description}'


class Option(TimestampFields):
    description = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')

    class Meta:
        verbose_name = 'Option'
        verbose_name_plural = 'Options'

    def __str__(self):
        return f'{self.description} [{self.question.description}]'


class UserAnswer(TimestampFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='answers')
    # опциональное поле text только для случаев ответа текстом
    text = models.CharField(max_length=100, blank=True, null=True)

    UniqueConstraint(
        name='user_option',
        fields=[user, option],
    )

    class Meta:
        verbose_name = 'User answer'
        verbose_name_plural = 'Users answers'

    def __str__(self):
        return f'{self.option.description} [{self.user.username}, {self.option.question.description}]'
