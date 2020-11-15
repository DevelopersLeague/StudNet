from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Update)
admin.site.register(QuestionReport)
admin.site.register(AnswerReport)
admin.site.register(flaggedQuestion)
admin.site.register(flaggedAnswer)
