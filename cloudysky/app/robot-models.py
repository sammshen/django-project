"""
Prompt to ChatGPT:


HW 3. Data Model (due 5th week, Apr 25)
A relational data model is a way of structuring data in a database using tables, where each table represents a specific entity or concept. The data in a relational database is organized into tables that have rows and columns. Each row in a table represents a single record or instance of the entity being modeled, while each column represents an attribute or characteristic of that entity.

The relational data model is based on the principles of mathematical set theory and emphasizes the relationships between tables. In a relational database, these relationships are established through the use of foreign keys, which link records in one table to records in another table.

The main advantages of the relational data model are its simplicity, flexibility, and scalability. It allows for efficient storage and retrieval of large amounts of data and supports complex queries and transactions. The relational model is also widely used in industry and has become a standard for managing data in many applications, from simple spreadsheets to complex enterprise systems.

Reading
Before you begin, you should read up on Django Models [https://docs.djangoproject.com/en/5.0/topics/db/models/], and Django Model Forms [https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/]. Django models define the basic data model which is then compiled to the database. Django Model Forms allow the front end to populate such a database.

Application Summary
CloudySky: An Ideologically Consonant Chat Environment
We want to implement a (web-based) chat app, not unlike Ed, that permits site moderators to remove and hide user-created content.

Users will see a feed of user-created content, will have a form to submit new posts and a form to attach new comments to existing posts. While you can imagine rooms, channels, and follower relationships, for this class we need only implement a single feed (we'll have to decide how to order the posts; chronological by original posting date is the simplest, but clearly prioritizes recent over highly engaging content). The feed should display an abbreviated version of the post; a page dedicated to the post should display all of the (non-suppressed) comments attached to the post.

While users see a feed of posts and attached comments, administrators have the responsibility to police the site for non-ideologically conforming content. Administrators have the ability to hide posts, which will remove them and their comments from all of the feeds except their creator, and the ability to hide comments, which replace the comments with a placeholder that says that content has been removed. The administrators can still see blocked content in their feeds, it is just displayed with a different color.

Users whose content has been blocked should see a message attached to each piece of blocked content an explanation (chosen from a list of reasons) of the reason that their content was suppressed.

Design Requirement 1. Simple and Easy to Use
Feed pages should have a green button to create a new post. Post pages should have a blank form field and a green button to post a comment. Admin pages should have a red button to remove content with a pull-down menu of vetted reasons.

Design Requirement 2. Accessible via API
Since many of the users on this site are expected to be bots, we would like to make it convenient for them to participate. There should be an API endpoint to allow a user to make a new post, add a comment to an existing post, and API endpoints to suppress posts (if logged in with administrator credentials).

Design Requirement 3. Dashboard
There should be an administration panel that lists the users, the number and volumne (in bytes) of their comments over the past 1, 7, and 30 days, and the number and volumen of their content that have been suppressed. (We will use this to re-program the bots that are not generating content consistent with our values).

Design Requirement 4. Embedding media
We should allow at least image uploads for user avatars.

Maybe we will include media in posts and display (certain types) of image files along with comments or posts. There's a pretty big design question here: how do you restrain user-created content to prevent it from taking over the entire screen?

Application Functionality (in English)
An important part of data engineering development is to interpret and understand application specifications. Here we spec out what the attendance chip application needs to support.

User Management There will be two classes of users: serfs and administrators. a. Serfs can see the main feed, the non-suppressed post pages and the non-suppressed contents. Serfs can see their own posts (and comments to those posts) even if the posts have been suppressed; similarly, serfs can see their own comments, even if their comments have been suppressed. b. Administrators can see the same pages but with more the moderation functionality. Administrators can also see the suppressed content. c. There is a user page with a user-editable user bio and a user-replaceable or user-deletable avatar image. d. The application should be able to add new serfs and administrators.

Moderation For simplicity, we will not have keep track of relationships between users, administrators, and sub-boards. There is one class of users, and one class of administrators, and the only relevant permissions scopes are user-can-see-users-content and administrator-can-see-everything.

Analytics All of the content, posts, comments, and media should be stored in the database. a. A report of each user's recent contributions and the numbers and fraction of comments and posts that have been censored should be available to administrators.

Data Model
Don't worry about implementing the full functionality yet. Instead we want you to think about the data model, what data needs to be stored and how it needs to be linked. You will edit the file models.py to have your data model.

At a high level here are all the entities that you have:

Users (of type either administrator or serf)
Posts
Comments
Avatars
Media
Implementing the Data Model
Your data model should implement these associations between these entities. Complete models.py with this data model. After completion run:

(venv) $ python manage.py makemigrations app
(venv) $ python manage.py migrate
This should run with no errors if your model is consistent.

Sometimes the database will end up in a weird state if you make contradictory changes. In this assignment, it is safe to just remove the database file and re-run the code above.

rm -Rf migrations db.sqlite
While this is an open-ended assignment, here are some things to think about.

Before you write any code, draw out the ER diagram. Note, you may have to create helper tables to implement certain types of relationships.
Start with the UserType tables and specify those in Django. Writing user creation and login pages will be your next homework.
Then, think about Posts and Comments and moderation. You may need multiple tables here.
Finally think about Media, both how they will be created and uploaded.
Save your ER diagram in app/docs/my-data-model.png. It's fine if it's hand-drawn! This will be useful for you and us to understand what you are doing.

Please generate a models.py
"""

from django.db import models
from django.contrib.auth.models import User

class UserType(models.Model):
    USER_TYPES = (
        ('serf', 'Serf'),
        ('admin', 'Administrator'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_TYPES)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_suppressed = models.BooleanField(default=False)
    suppression_reason = models.TextField(blank=True, null=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_suppressed = models.BooleanField(default=False)
    suppression_reason = models.TextField(blank=True, null=True)

class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/')
    bio = models.TextField(blank=True)

class Media(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
