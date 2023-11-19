"""
Script to convert the settings for Matching Pair questions from Structural to 
MCQ.
"""

from phobos.models import Question, MCQQuestionSettings, QuestionChoices

def run():
    # Get all the matching pair questions
    mp_questions = Question.objects.filter(answer_type=QuestionChoices.MATCHING_PAIRS)
    for mp_q in mp_questions:
        # Getting the attributes 
        num_points = mp_q.struct_settings.num_points
        max_attempts = mp_q.struct_settings.max_num_attempts
        deduct_per_attempt = mp_q.struct_settings.deduct_per_attempt
        # deleting the structural settings
        mp_q.struct_settings.delete()

        # creating the mcq settings
        mcq_settings, created = MCQQuestionSettings.objects.get_or_create(question=mp_q)
        if created:
            mcq_settings.num_points = num_points
            mcq_settings.mcq_max_num_attempts = max_attempts
            mcq_settings.mcq_deduct_per_attempt = deduct_per_attempt
        mcq_settings.save()
        mp_q.save()
