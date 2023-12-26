from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from polls.models import Question

# Usualmente se testean modelos y vistas

def create_question(question_text, days):
    """
    Create a question with the given question_text, and published
    the given number of days offset to now 
    """
    time = timezone.now() + timedelta(days=days)
    return Question.objects.create(question_text = question_text, pub_date = time)


class QuestionMNodelTest(TestCase):

    def test_was_published_recently_with_future_questions(self):
        """If the date is in future the methos should return False"""

        time = timezone.now() + timedelta(30)
        future_question =  Question(question_text="Quien es quien", pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)


class QuestionIndexViewTests(TestCase):

    def test_no_question(self):
        """If no question exist, and appropiate message is displayed"""
        
        response = self.client.get(reverse('polls:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
    
    def test_future_question(self):
        """"""
        create_question('Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_Questions(self):
        """pass"""
        question = create_question('Past question', days=-10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])

    def test_future_question_and_past_question(self):
        """"""
        past_question = create_question(question_text='Past question', days=-30)
        future_question = create_question(question_text='Future question', days=30)
        respoonse = self.client.get(reverse('polls:index'))
        
        self.assertQuerysetEqual(
            respoonse.context['latest_question_list'],
            [past_question]
            )

    def two_past_questions(self):
        """"""
        past_question1 = create_question(question_text='Past question 1', days=-30)
        past_question2 = create_question(question_text='Future question 2', days=40)
        respoonse = self.client.get(reverse('polls:index'))
        
        self.assertQuerysetEqual(
            respoonse.context['latest_question_list'],
            [past_question1, past_question2]
            )

    def two_future_questions(self):
        """"""
        create_question(question_text='Future question 1', days=30)
        create_question(question_text='Future question 2', days=40)
        respoonse = self.client.get(reverse('polls:index'))
        
        self.assertQuerysetEqual(
            respoonse.context['latest_question_list'],
            []
            )


class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        
        future_question = create_question(question_text='Future question', days=30)
        url = reverse('polls:detail', args=(future_question.id,)) 
        
        response = self.client.get(
            url
        )

        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        
        past_question = create_question(question_text='Past question', days=-30)
        url = reverse('polls:detail', args=(past_question.id, )) 
        
        response = self.client.get(
            url
        )
        
        self.assertContains(response, past_question.question_text)