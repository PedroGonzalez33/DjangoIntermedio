import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question

class QuestionModelTests(TestCase):

    def setUp(self):
        self.question = Question(question_text = "Pregunta X?")

    def test_was_published_recently_with_future_questions(self):
        """was_published_recenly returns False for questions whose pub_data is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = self.question
        future_question.pub_date = time
        self.assertIs(future_question.was_published_recenly(), False)
        
    def test_was_published_recently_with_past_questions(self):
        """was_published_recenly returns False for questions whose pub_data is in the past"""
        time = timezone.now() - datetime.timedelta(days=1, minutes=1)
        past_question = self.question
        past_question.pub_date = time
        self.assertIs(past_question.was_published_recenly(), False)

    def test_was_published_recently_with_present_questions(self):
        """was_published_recenly returns True for questions whose pub_data is in the last 24 hours"""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59)
        present_question = self.question
        present_question.pub_date = time
        self.assertIs(present_question.was_published_recenly(), True)


def create_question(question_text, days):
    """ Create a question with the given "question text, and published
    the given number of days offset to now (negative for a questions published 
    in the past, positive for questions that have yet to be published)
    " """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text= question_text, pub_date= time) 

class QuestionIndexViewTests(TestCase):
    
    def test_no_questions(self):
        """ If no question exist, an apropiate message is displayed """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay encuestas disponibles")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
    
    def test_future_questions(self):
        " If the question is in the future, don't show in page"
        create_question("Future question", days=1)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay encuestas disponibles")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])       
        
    def test_past_questions(self):
        " If the question is in the past, show in page"
        question = create_question("Past question", days=-1)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_past_questions_and_future_question(self):
        " If two questions (one in the past and another in the future) are published, only show the question in the past"
        past_question = create_question("Past question", days=-1)
        future_question = create_question("Past question", days=1)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question]) 

    def test_two_past_questions(self):
        " If two questions in the past are published, show both questions in the past"
        past_question_1 = create_question("Past question", days=-1)
        past_question_2 = create_question("Past question", days=-2)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(past_question_1, response.context["latest_question_list"]) 
        self.assertIn(past_question_2, response.context["latest_question_list"])

    def test_two_future_questions(self):
        " If two questions in the future are published, don't show any questions"
        future_question_1 = create_question("Past question", days=1)
        future_question_2 = create_question("Past question", days=2)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(future_question_1, response.context["latest_question_list"]) 
        self.assertNotIn(future_question_2, response.context["latest_question_list"])  

class QuestionDetailViewsTests(TestCase):
    def test_future_question(self):
        """ The detail view of a question with a pub_date in the future
        returns a 404 error not found 
        """
        future_question = create_question(question_text= "Future question", days=30)
        url = reverse("polls:detail", args=(future_question.pk, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """ The detail view of a question with a pub_date in the past
        displays the question's text 
        """
        past_question = create_question(question_text= "Past question", days=-3)
        url = reverse("polls:detail", args=(past_question.pk, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)
