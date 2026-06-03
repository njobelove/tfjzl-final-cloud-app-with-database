from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    """Model for storing course information"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Duration in weeks")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Lesson(models.Model):
    """Model for storing lesson information"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.IntegerField(default=0)
    duration = models.IntegerField(help_text="Duration in minutes", default=30)
    
    def __str__(self):
        return f"{self.course.name} - {self.title}"

class Instructor(models.Model):
    """Model for storing instructor information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    expertise = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.user.username

class Learner(models.Model):
    """Model for storing learner information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrolled_courses = models.ManyToManyField(Course, blank=True, related_name='learners')
    
    def __str__(self):
        return self.user.username

class Question(models.Model):
    """Model for storing exam questions"""
    text = models.TextField()
    grade = models.IntegerField(default=1, help_text="Points for this question")  # REQUIRED FIELD
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.text[:50]
    
    def get_correct_choices(self):
        """Return all correct choices for this question"""
        return self.choice_set.filter(is_correct=True)
    
    def is_get_score(self, selected_choices):
        """Calculate score for this question based on selected choices"""
        correct_choices = self.get_correct_choices()
        if selected_choices.count() == correct_choices.count():
            # Check if all selected choices are correct
            for choice in selected_choices.all():
                if not choice.is_correct:
                    return 0
            return self.grade
        return 0

class Choice(models.Model):
    """Model for storing answer choices for questions"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text

class Enrollment(models.Model):
    """Model for tracking student enrollment in courses"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'course']
    
    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.name}"

class Submission(models.Model):
    """Model for storing student exam submissions"""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)  # REQUIRED: ManyToManyField to Choice
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['enrollment', 'question']
    
    def __str__(self):
        return f"{self.enrollment.user.username} - {self.question.text[:30]}"
    
    def is_get_score(self):
        """Calculate score for this submission"""
        selected_choices = self.choices.all()
        return self.question.is_get_score(selected_choices)
