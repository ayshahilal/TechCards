
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("why_tech_cards", views.why_tech_cards, name="why_tech_cards"),
    path("topic/<int:id>", views.topic, name="topic"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("new_card/<int:user_id>", views.new_card, name="new_card"),
    path("create_flashcard", views.create_flashcard, name="create_flashcard"),
    path("mixed_flashcards", views.mixed_flashcards, name="mixed_flashcards"),
    path("mycards/<int:user_id>", views.mycards, name="mycards"),
    path("select_score/<int:card_id>/<int:score>/<str:mixed>", views.select_score, name="select_score"),
    path("delete_card/<int:card_id>", views.delete_card, name="delete_card"),
    path("edit_card_page/<int:card_id>", views.edit_card_page, name="edit_card_page"),
    path("edit_flashcard/<int:card_id>", views.edit_flashcard, name="edit_flashcard"),
    path("solved_cards", views.solved_cards, name="solved_cards"),
    path("set_not_solved/<int:card_id>", views.set_not_solved, name="set_not_solved"),
    path("solved_progress/<int:card_id>/<str:mixed>", views.solved_progress, name="solved_progress")
]