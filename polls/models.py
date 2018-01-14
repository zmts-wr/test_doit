from django.db import models


class QuestionGroup(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return '%s: %s' % (self.id, self.title, )


class Question(models.Model):
    group = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return '%s (%s): %s' % (self.id, self.group_id, self.text, )


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_right = models.BooleanField(default=False)

    def __str__(self):
        return '%s (%s): (%s) %s' % (self.id, self.question_id, self.is_right, self.text, )
