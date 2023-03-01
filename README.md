# TechCards
This is the final project of CS50W course of Harvard. 

* The youtube link: https://youtu.be/T4w0-Ttudvo

# Requirements
The final project is your opportunity to design and implement a dynamic website of your own. So long as your final project draws upon this course’s lessons, the nature of your website will be entirely up to you, albeit subject to the staff’s approval.

In this project, you are asked to build a web application of your own. The nature of the application is up to you, subject to a few requirements:

* Your web application must utilize at least two of Python, JavaScript, and SQL.
* Your web application must be mobile-responsive.
* In README.md, include a short writeup describing your project, what’s contained in each file you created or modified, and (optionally) any other additional information the staff should know about your project.

# Running the app
1. Download the code
2. In your terminal, cd into the directory where the project file exists.
3. Apply the migrations:  ``` python3 manage.py migrate ```
4. Then just run the server: ``` python3 manage.py runserver ```


# Distinctiveness and Complexity
This project is designed as a flashcard application tailored to tech students who are seeking to study for interviews or accelerate their learning process. It distinguishes itself from other projects in this course by leveraging the skills acquired throughout the course, such as pagination, JavaScript fetch calls, Django's admin interface, and Django forms.

The primary objective was to develop a user-friendly and mobile-responsive flashcard application, with a focus on providing a seamless user experience. Users are able to create, edit, and delete their own techcards, track their progress through scores, and study from mixed or specific topics. Each card has 3 difficulty level as easy, medium, hard to keep track a score for the user. Additionally, users can browse through other users' techcards and contribute to the growth of the application's database.

Having personally benefited from using flashcards to study for interviews, I was motivated to create a similar tool for tech students. With the collective effort of its users, the application's techcard database can expand and serve as a valuable resource for many.

The application is built using Django for its backend, featuring four models, and JavaScript for the frontend. It is mobile-responsive and implemented using the Bootstrap framework.

* A perspective from the desktop design

![desktop](https://user-images.githubusercontent.com/44849765/222134925-c9ed46ed-88a6-4e38-a166-a1ee01aba878.jpg)

* A perspective from the mobile design

![mobile](https://user-images.githubusercontent.com/44849765/222134976-b1a3620b-04db-4a92-89dc-155578423cd1.jpg)


# File structure description

* ``` final ``` - main application directory.
  - ``` static/final ``` - contains all static content. 
    * ``` styles.css ``` - contains compiled CSS file and its map. 
    * ``` card_operations.js ``` - all JavaScript functions used for the card operations.
  - ``` templates/final ``` - contains all application templates.
    * ``` cards.html ``` - cards page to show users own cards, all the cards made by different users, cards for the chosen topic, the users solved cards.
    * ``` createCard.html ``` - the page that allows to create a new techcard and edit an existing card created by the loged in user. 
    * ``` index.html ``` - The main page that shows the study topics with buttons and a link to another page (whyTechCards page) 
    * ``` layout.html ``` - The base templates.
    * ``` login.html ``` - The login page. 
    * ``` profile.html ``` - The profile page for the loged in user. The page shows the score of the user, the links for; users cards, users solved cards and create new card pages.
    * ``` register.html ``` - The register page. 
    * ``` whyTechCards.html ``` - An informative content about the benefits of studying with techCards.
   - ``` admin.py ``` - Admin classes.
   - ``` apps.py ``` - Apps file
   - ``` models.py ``` - Contains four models I used in the project. User model extends the standard User model and a scoreSum in addition to save the users score, Topics model is for the topics of the study cards, Cards model for the informations of a flashcards as owner, frontside, backside and topic, and UserChoice represents each users score for the cards they study. (There are 3 score for each card, Easy, Medium and Hard)
   - ``` urls.py ``` - url patterns
   - ``` views.py``` - respectively, contains all application views.
* ``` project4 ``` - project directory.
