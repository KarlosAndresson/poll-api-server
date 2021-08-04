from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.api.models import Option, Poll, Question, UserAnswer
from apps.api.v1.filters import PollFilterSet, QuestionFilterSet, OptionFilterSet, UserAnswerFilterSet
from apps.api.v1.lang_constants import ApiMessages, ApiMessage
from apps.api.v1.serializers import PollSerializer, QuestionSerializer, OptionSerializer, UserAnswerSerializer
from logger import AppLogger


def make_api_response(message, http_status: int) -> Response:
    response = Response()
    response.status_code = http_status
    response.status = response.status_code
    response.data = {'detail': message.message_en}
    return response


def alter_post_request(request: Request, update: dict = None, remove: list = None):
    if update is None:
        update = dict()
    if remove is None:
        remove = []
    if len(request.FILES) > 0:
        for key in remove:
            request._full_data.pop(key, None)
        request._full_data.update(update)
    elif request.POST:
        mutable_state = request.data._mutable
        request.data._mutable = True
        for key in remove:
            request.data.pop(key, None)
        request.data.update(update)
        request.data._mutable = mutable_state


def alter_get_request(request: Request, update: dict = None, remove: list = None):
    if update is None:
        update = dict()
    if remove is None:
        remove = []
    # канонический вариант с request.GET.copy() в Django 2.2 не работает (не обновляется query_params)
    # проверку hasattr(request.GET, '_mutable') не делаем, чтобы упасть в случае если меняется структура данных
    mutable_state = request.GET._mutable
    request.GET._mutable = True
    for key in remove:
        request.GET.pop(key, None)
    request.GET.update(update)
    request.GET._mutable = mutable_state


class PollViewSet(ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PollFilterSet
    http_method_names = ['get', 'post', 'patch', 'delete']
    logger = AppLogger(filename='poll_view.log')
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.logger.debug(f'List started: {request.data}')

        # если передан параметр user то делаем выборку с учетом ID пользователя
        user_id = request.GET.get('user', None)
        if user_id is not None:
            user = User.objects.filter(pk=user_id).first()
            if not user:
                self.logger.info(f'{ApiMessages.UserDoesNotExist.detail}')
                return make_api_response(ApiMessages.UserDoesNotExist, status.HTTP_404_NOT_FOUND)
            polls = Poll.objects.filter(questions__options__answers__in=user.answers.all()).distinct()
            return JsonResponse(data=list(polls.values()), safe=False)

        response = super(PollViewSet, self).list(request, *args, **kwargs)
        return response

    def create(self, request, *args, **kwargs):
        self.logger.debug(f'Create started: {request.data}')

        # предполагаем что для запроса юзер должен иметь права админа
        if not self.request.user.is_superuser:
            self.logger.info(f'{ApiMessages.UserHasNoPermission.detail}')
            return make_api_response(ApiMessages.UserHasNoPermission, status.HTTP_403_FORBIDDEN)

        response = super(PollViewSet, self).create(request, *args, **kwargs)
        return response

    def destroy(self, request, pk=None, *args, **kwargs):
        self.logger.debug(f'Delete started: {request.data}')

        if not self.request.user.is_superuser:
            self.logger.info(f'{ApiMessages.UserHasNoPermission.detail}')
            return make_api_response(ApiMessages.UserHasNoPermission, status.HTTP_403_FORBIDDEN)

        response = super(PollViewSet, self).destroy(request, *args, **kwargs)
        return response

    def partial_update(self, request, pk=None, *args, **kwargs):
        self.logger.debug(f'Update started: {request.data}')

        if not self.request.user.is_superuser:
            self.logger.info(f'{ApiMessages.UserHasNoPermission.detail}')
            return make_api_response(ApiMessages.UserHasNoPermission, status.HTTP_403_FORBIDDEN)

        # запрещаем менять дату старта опроса, если он уже установлен
        if request.POST.get('started_at', None):
            poll = Poll.objects.filter(pk=pk).first()
            if poll and poll.started_at:
                alter_post_request(request=request, remove=['started_at'])

        response = super(PollViewSet, self).partial_update(request, *args, **kwargs)
        return response


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.select_related('poll')
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuestionFilterSet
    http_method_names = ['get', 'post', 'patch', 'delete']
    logger = AppLogger(filename='question_view.log')
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        self.logger.debug(f'Create started: {request.data}')

        if not self.request.user.is_superuser:
            self.logger.info(f'{ApiMessages.UserHasNoPermission.detail}')
            return make_api_response(ApiMessages.UserHasNoPermission, status.HTTP_403_FORBIDDEN)

        response = super(QuestionViewSet, self).create(request, *args, **kwargs)
        return response

    def destroy(self, request, pk=None, *args, **kwargs):
        self.logger.debug(f'Delete started: {request.data}')

        if not self.request.user.is_superuser:
            self.logger.info(f'{ApiMessages.UserHasNoPermission.detail}')
            return make_api_response(ApiMessages.UserHasNoPermission, status.HTTP_403_FORBIDDEN)

        response = super(QuestionViewSet, self).destroy(request, *args, **kwargs)
        return response

    def partial_update(self, request, pk=None, *args, **kwargs):
        self.logger.debug(f'Update started: {request.data}')

        if not self.request.user.is_superuser:
            self.logger.info(f'{ApiMessages.UserHasNoPermission.detail}')
            return make_api_response(ApiMessages.UserHasNoPermission, status.HTTP_403_FORBIDDEN)

        response = super(QuestionViewSet, self).partial_update(request, *args, **kwargs)
        return response


class OptionViewSet(ModelViewSet):
    queryset = Option.objects.select_related('question')
    serializer_class = OptionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OptionFilterSet
    http_method_names = ['get', 'post', 'patch', 'delete']
    logger = AppLogger(filename='option_view.log')
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        self.logger.debug(f'Create started: {request.data}')

        if not self.request.user.is_superuser:
            self.logger.info(f'{ApiMessages.UserHasNoPermission.detail}')
            return make_api_response(ApiMessages.UserHasNoPermission, status.HTTP_403_FORBIDDEN)

        response = super(OptionViewSet, self).create(request, *args, **kwargs)
        return response

    def destroy(self, request, pk=None, *args, **kwargs):
        self.logger.debug(f'Delete started: {request.data}')

        if not self.request.user.is_superuser:
            self.logger.info(f'{ApiMessages.UserHasNoPermission.detail}')
            return make_api_response(ApiMessages.UserHasNoPermission, status.HTTP_403_FORBIDDEN)

        response = super(OptionViewSet, self).destroy(request, *args, **kwargs)
        return response

    def partial_update(self, request, pk=None, *args, **kwargs):
        self.logger.debug(f'Update started: {request.data}')

        if not self.request.user.is_superuser:
            self.logger.info(f'{ApiMessages.UserHasNoPermission.detail}')
            return make_api_response(ApiMessages.UserHasNoPermission, status.HTTP_403_FORBIDDEN)

        response = super(OptionViewSet, self).partial_update(request, *args, **kwargs)
        return response


class UserAnswerViewSet(ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserAnswerFilterSet
    http_method_names = ['get', 'post', 'patch', 'delete']
    logger = AppLogger(filename='user_answer_view.log')
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.logger.debug(f'List started: {request.data}')

        response = super(UserAnswerViewSet, self).list(request, *args, **kwargs)
        return response

    def create(self, request, *args, **kwargs):
        self.logger.debug(f'Create started: {request.data}')

        response = super(UserAnswerViewSet, self).create(request, *args, **kwargs)
        return response

    def destroy(self, request, pk=None, *args, **kwargs):
        self.logger.debug(f'Delete started: {request.data}')

        if not self.request.user.is_superuser:
            self.logger.info(f'{ApiMessages.UserHasNoPermission.detail}')
            return make_api_response(ApiMessages.UserHasNoPermission, status.HTTP_403_FORBIDDEN)

        response = super(UserAnswerViewSet, self).destroy(request, *args, **kwargs)
        return response

    def partial_update(self, request, pk=None, *args, **kwargs):
        self.logger.debug(f'Update started: {request.data}')

        if not self.request.user.is_superuser:
            self.logger.info(f'{ApiMessages.UserHasNoPermission.detail}')
            return make_api_response(ApiMessages.UserHasNoPermission, status.HTTP_403_FORBIDDEN)

        response = super(UserAnswerViewSet, self).partial_update(request, *args, **kwargs)
        return response
