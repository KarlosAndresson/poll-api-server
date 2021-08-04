import django_filters
from django_filters import rest_framework as filters


class PollFilterSet(django_filters.FilterSet):
    id = filters.NumberFilter()
    name = filters.CharFilter(lookup_expr='icontains')
    started_at = filters.DateTimeFromToRangeFilter()
    ended_at = filters.DateTimeFromToRangeFilter()
    description = filters.CharFilter(lookup_expr='icontains')
    is_active = filters.BooleanFilter()


class QuestionFilterSet(filters.FilterSet):
    id = filters.NumberFilter()
    description = filters.CharFilter(lookup_expr='icontains')
    poll = filters.NumberFilter()
    type = filters.CharFilter(lookup_expr='iexact')


class OptionFilterSet(filters.FilterSet):
    id = filters.NumberFilter()
    description = filters.CharFilter(lookup_expr='icontains')
    question = filters.NumberFilter()


class UserAnswerFilterSet(filters.FilterSet):
    id = filters.NumberFilter()
    user = filters.NumberFilter()
    option = filters.NumberFilter()
    text = filters.CharFilter(lookup_expr='icontains')
