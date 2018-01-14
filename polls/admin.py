from django.contrib import admin
from django.core.exceptions import ValidationError
import nested_admin

from polls import models


class AnswerAdminFormSet(nested_admin.NestedInlineFormSet):
    def clean(self):
        errors = []
        data = [ item['is_right'] for item in self.cleaned_data if not item['DELETE'] ]
        right_ans = sum(data)
        all_ans = len(data)
        if right_ans < 1:
            errors.append('At least one right answer required')
        elif right_ans == all_ans:
            errors.append('At least one wrong answer required')

        if errors:
            raise ValidationError(errors)


class AnswerInline(nested_admin.NestedTabularInline):
    model = models.Answer
    extra = 0
    formset = AnswerAdminFormSet


class QuestionInline(nested_admin.NestedStackedInline):
    model = models.Question
    extra = 0
    inlines = [AnswerInline,]


@admin.register(models.QuestionGroup)
class QuestionGroupAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline,]
