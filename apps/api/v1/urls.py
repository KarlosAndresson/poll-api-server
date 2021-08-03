from rest_framework.routers import DefaultRouter
from apps.api.v1.views import PollViewSet, QuestionViewSet, OptionViewSet, UserAnswerViewSet

router = DefaultRouter()
router.root_view_name = 'root'
router.register('polls', PollViewSet)
router.register('questions', QuestionViewSet)
router.register('options', OptionViewSet)
router.register('answers', UserAnswerViewSet)
urlpatterns = [] + router.urls
