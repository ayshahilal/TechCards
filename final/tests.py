from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Topics, Cards, UserChoice

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a user
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )

        # Create some topics
        self.topic1 = Topics.objects.create(
            name="Topic 1"
        )

        self.topic2 = Topics.objects.create(
            name="Topic 2"
        )

        # Create some cards
        self.card1 = Cards.objects.create(
            question="Question 1",
            answer="Answer 1",
            topic=self.topic1
        )

        self.card2 = Cards.objects.create(
            question="Question 2",
            answer="Answer 2",
            topic=self.topic1
        )

        self.card3 = Cards.objects.create(
            question="Question 3",
            answer="Answer 3",
            topic=self.topic2
        )

        # Create a UserChoice object to simulate a solved card
        self.user_choice = UserChoice.objects.create(
            user=self.user,
            card=self.card1,
            correct=True
        )

    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "final/index.html")

    def test_why_tech_cards_view(self):
        response = self.client.get(reverse("why_tech_cards"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "final/whyTechCards.html")

    def test_login_view(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "final/login.html")

        # Test successful login
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "testpassword"
        })
        self.assertRedirects(response, reverse("index"))

        # Test unsuccessful login
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "final/login.html")
        self.assertContains(response, "Invalid username and/or password.")

    def test_logout_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("index"))
