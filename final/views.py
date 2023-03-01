from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User, Topics, Cards, UserChoice
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.http import JsonResponse

import ast

def index(request):
    topics = Topics.objects.all()
    return render(request, "final/index.html",{
        "topics" : topics 
    })

def why_tech_cards(request):
    return render(request, "final/whyTechCards.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "final/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "final/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "final/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "final/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "final/register.html")


def topic(request,id):

    selectedTopic = Topics.objects.get(pk=id)
    cards = Cards.objects.filter(topic=selectedTopic).order_by("id")
    all_card_count = len(cards)
    if len(cards) == 0:
        noCards = True
    else:
        noCards = False
    
    topics = Topics.objects.all()

    unsolvedCards = []
    solved_cards_count = 0
    if request.user.is_authenticated:
        for card in cards:
            try:
                solved = UserChoice.objects.get(user=request.user, card=card)
                if(card.topic == selectedTopic):
                    solved_cards_count +=1 
            except UserChoice.DoesNotExist:
                unsolvedCards.append(card)

        paginator = Paginator(unsolvedCards, 1)
    else:
        paginator = Paginator(cards, 1)

    current_page_number = request.GET.get('page')
    current_page = paginator.get_page(current_page_number)
    if solved_cards_count == all_card_count:
        all_solved = True
    else:
        all_solved = False

    return render(request, "final/cards.html",{
        "topic_name":selectedTopic,
        "topics" : topics,
        "cards": current_page,
        "mixed": False,
        "noCards": noCards,
        "user_cards_only": False,
        "solved_cards_only": False,
        "all_cards_count":all_card_count,
        "solved_cards_count": solved_cards_count,
        "all_solved": all_solved
    })
    

@login_required
def solved_cards(request):

    cards = Cards.objects.all().order_by("id")
    if len(cards) == 0:
        noCards = True
    else:
        noCards = False
    
    topics = Topics.objects.all()

    solvedCards = []

    for card in cards:
        try:
            solved = UserChoice.objects.get(user=request.user, card=card)
            solvedCards.append(card)
        except UserChoice.DoesNotExist:
            continue

    paginator = Paginator(solvedCards, 3)
    current_page_number = request.GET.get('page')
    current_page = paginator.get_page(current_page_number)
            
    return render(request, "final/cards.html",{
        "topics" : topics,
        "cards": current_page,
        "mixed": False,
        "noCards": noCards,
        "user_cards_only": False,
        "solved_cards_only": True
    })

def mixed_flashcards(request):
    cards = Cards.objects.all().order_by('?')
    if len(cards) == 0:
        noCards = True
    else:
        noCards = False

    all_card_count = len(cards)
    topics = Topics.objects.all()

    solved_cards_count = 0
    unsolvedCards = []
    if request.user.is_authenticated:
        for card in cards:
            try:
                solved = UserChoice.objects.get(user=request.user, card=card)
                solved_cards_count+=1
            except UserChoice.DoesNotExist:
                unsolvedCards.append(card)
                continue

        paginator = Paginator(unsolvedCards, 1)
    else:
        paginator = Paginator(cards, 1)
    current_page_number = request.GET.get('page')
    current_page = paginator.get_page(current_page_number)
    
    if solved_cards_count == all_card_count:
        all_solved = True
    else:
        all_solved = False
    return render(request, "final/cards.html",{
        "topics" : topics,
        "cards": current_page,
        "mixed": True,
        "noCards": noCards,
        "user_cards_only":False,
        "solved_cards_only": False,
        "all_cards_count": all_card_count,
        "solved_cards_count": solved_cards_count,
        "all_solved": all_solved
    })


@login_required
def mycards(request, user_id):
    
    user_profile = User.objects.get(pk=user_id)
    cards = Cards.objects.filter(owner=user_profile).order_by("id").reverse()

    if len(cards) == 0:
        noCards = True
    else:
        noCards = False
    paginator = Paginator(cards, 3)
    current_page_number = request.GET.get('page')
    current_page = paginator.get_page(current_page_number)
    topics = Topics.objects.all()

    return render(request, "final/cards.html",{
        "topics" : topics,
        "cards": current_page,
        "mixed": False,
        "noCards": noCards,
        "user_cards_only":True,
        "solved_cards_only": False
    })
    
@login_required
def profile(request, user_id):
    user_profile = User.objects.get(pk=user_id)
    cards = Cards.objects.all().order_by("id")

    paginator = Paginator(cards, 1)
    current_page_number = request.GET.get('page')
    current_page = paginator.get_page(current_page_number)

    topics = Topics.objects.all()
    userScore = UserChoice.objects.filter(user=request.user)
    
    return render(request, "final/profile.html",{
        "user_profile": user_profile,
        "topics" : topics,
        "cards": current_page,
        "userScore": userScore
    })

@login_required
def new_card(request, user_id):
    user_profile = User.objects.get(pk=user_id)
    cards = Cards.objects.all().order_by("id")

    paginator = Paginator(cards, 1)
    current_page_number = request.GET.get('page')
    current_page = paginator.get_page(current_page_number)

    topics = Topics.objects.all()
    userScore = UserChoice.objects.filter(user=request.user)
    
    return render(request, "final/createCard.html",{
        "user_profile": user_profile,
        "topics" : topics,
        "cards": current_page,
        "edit": False,
        "userScore": userScore
    })

@login_required
def create_flashcard(request):
    topics = Topics.objects.all()
    if request.method == "POST":
        owner = request.user
        front_side = request.POST['front_side']
        back_side = request.POST['back_side']
        topic_id = request.POST['topic_name']
        topic = Topics.objects.get(id=topic_id)
        newFlashcard = Cards(owner=owner, front_side=front_side, back_side=back_side, topic=topic)
        newFlashcard.save()
        return HttpResponseRedirect(reverse("mycards",  args=(request.user.id,)))
    else:
        return render(request, "flashcards/createCard.html")

@login_required
def edit_flashcard(request, card_id):
    if request.method == "POST":
        try:
            editCard = Cards.objects.get(pk=card_id)
        except Cards.DoesNotExist:
            # Handle invalid card ID
            return HttpResponseBadRequest("Invalid card ID")
        
        editCard.front_side = request.POST['front_side']
        editCard.back_side = request.POST['back_side']
        topic_id = request.POST['topic_name']
        editCard.topic = Topics.objects.get(id=topic_id)
        editCard.save()
        return HttpResponseRedirect(reverse("mycards", args=(request.user.id,)))
    else:
        # Handle non-POST requests
        return HttpResponseNotAllowed(["POST"])


@login_required
def select_score(request, card_id, score, mixed):
    is_mixed = ast.literal_eval(mixed)
    card = Cards.objects.get(pk=card_id)
    old_score = 0
    try:
        user_card_score = UserChoice.objects.get(user=request.user, card=card)
        old_score = user_card_score.score
        user_card_score.score = int(score)
        user_card_score.save()
        
    except UserChoice.DoesNotExist:
        user_card_score = UserChoice(user=request.user, card=card, score=int(score))
        user_card_score.save()
        # Update the user's score based on their choice
        
    user = User.objects.get(id=request.user.id)
    if old_score != 0:
        user.scoreSum -= old_score
    user.scoreSum += int(score)
    user.save()
    if is_mixed:
        current_url = reverse('mixed_flashcards')
    else:
        current_url = reverse('topic', kwargs={'id':card.topic.id})
    return JsonResponse({"message":"success like","data":user.scoreSum, "url": current_url})


@login_required
def delete_card(request, card_id):
    if request.method == "POST":
        deleteCard = Cards.objects.get(pk=card_id)
        deleteCard.delete()
        return HttpResponseRedirect(reverse("mycards", args=(request.user.id,)))

@login_required
def edit_card_page(request, card_id):
    user_profile = User.objects.get(pk=request.user.id)
    topics = Topics.objects.all()
    userScore = UserChoice.objects.filter(user=request.user)

    editCard = Cards.objects.get(pk=card_id)
    
    return render(request, "final/createCard.html",{
        "user_profile": user_profile,
        "topics" : topics,
        "userScore": userScore,
        "edit": True,
        "editCard": editCard
    })


@login_required
def set_not_solved(request, card_id):
    try:
        card = Cards.objects.get(pk=card_id)
    except Cards.DoesNotExist:
        # Handle invalid card ID
        return JsonResponse({"message": "Invalid card ID"}, status=400)

    try:
        setCard = UserChoice.objects.get(user=request.user, card=card)
        user = User.objects.get(id=request.user.id)
        user.scoreSum -= setCard.score
        user.save()
        setCard.delete()
        current_url=reverse('solved_cards')
        return JsonResponse({"message": "Card choice deleted","url": current_url}, status=200)
    except UserChoice.DoesNotExist:
        # Handle missing UserChoice object
        return JsonResponse({"message": "No UserChoice object found"}, status=400)



def solved_progress(request, card_id, mixed):
    is_mixed = ast.literal_eval(mixed)
    if(is_mixed):
        cards = Cards.objects.all()
        all_card_count = len(cards) 
        solved_cards_count = 0

        for card in cards:
            try:
                solved = UserChoice.objects.get(user=request.user, card=card)
                solved_cards_count+=1
            except UserChoice.DoesNotExist:
                continue
    else:
        solved_cards_count = 0
        selectedTopic = Topics.objects.get(pk=card_id)
        cards = Cards.objects.filter(topic=selectedTopic).order_by("id")
        all_card_count = len(cards) 
        for card in cards:
            try:
                solved = UserChoice.objects.get(user=request.user, card=card)
                if(card.topic == selectedTopic):
                    solved_cards_count +=1  
            except UserChoice.DoesNotExist:
                continue

    return JsonResponse({"message": "success", "data": {"solved_cards_count": solved_cards_count, "all_card_count": all_card_count}})
            