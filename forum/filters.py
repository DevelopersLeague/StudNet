import django_filters
from django_filters import CharFilter
from .models import *


class QuestionFilter(django_filters.FilterSet):
    question_text = CharFilter(
        field_name="question_text", lookup_expr="icontains")

    class Meta:
        model = Question
        fields = "__all__"
        exclude = ["user_id", "created_on"]
