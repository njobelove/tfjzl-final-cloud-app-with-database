from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Question, Choice, Submission
from django.utils import timezone

def submit(request, question_id):
    """Handle question submission and save user's answer"""
    if request.method == 'POST':
        question = get_object_or_404(Question, id=question_id)
        selected_choice_id = request.POST.get('choice')
        
        if selected_choice_id:
            selected_choice = get_object_or_404(Choice, id=selected_choice_id)
            
            # Check if user already submitted this question
            submission, created = Submission.objects.get_or_create(
                user=request.user,
                question=question,
                defaults={'selected_choice': selected_choice}
            )
            
            if not created:
                # Update existing submission
                submission.selected_choice = selected_choice
                submission.submitted_at = timezone.now()
            
            submission.is_correct = selected_choice.is_correct
            submission.save()
            
            messages.success(request, "Your answer has been submitted!")
        else:
            messages.error(request, "Please select an answer.")
        
        return redirect('exam')

def show_exam_result(request):
    """Display exam results with score and congratulations message"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get all submissions for the user
    submissions = Submission.objects.filter(user=request.user)
    
    # Calculate score
    total_questions = Question.objects.count()
    correct_answers = submissions.filter(is_correct=True).count()
    
    if total_questions > 0:
        score_percentage = (correct_answers / total_questions) * 100
    else:
        score_percentage = 0
    
    # Determine if passed (e.g., 70% or higher)
    passed = score_percentage >= 70
    
    context = {
        'submissions': submissions,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'score_percentage': round(score_percentage, 2),
        'passed': passed,
        'congratulations': passed,
    }
    
    return render(request, 'exam_result.html', context)

def exam_view(request):
    """Display all questions for the exam"""
    questions = Question.objects.all()
    user_submissions = {sub.question_id: sub for sub in Submission.objects.filter(user=request.user)}
    
    context = {
        'questions': questions,
        'user_submissions': user_submissions,
    }
    return render(request, 'exam.html', context)