from django.contrib import admin
from .models import Question, Choice, Submission

# Imported 7 classes: admin.ModelAdmin, StackedInline, TabularInline, etc.

class ChoiceInline(admin.TabularInline):
    """Inline admin for Choice model"""
    model = Choice
    extra = 4

class QuestionInline(admin.StackedInline):
    """Stacked inline admin for Question model"""
    model = Question
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    """Admin configuration for Question model"""
    list_display = ['text', 'created_at', 'get_correct_answers']
    list_filter = ['created_at']
    search_fields = ['text']
    inlines = [ChoiceInline]
    
    def get_correct_answers(self, obj):
        return obj.choice_set.filter(is_correct=True).count()
    get_correct_answers.short_description = 'Correct Answers'

class LessonAdmin(admin.ModelAdmin):
    """Admin configuration for Lesson model"""
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    search_fields = ['title']

# Register models with admin site
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)