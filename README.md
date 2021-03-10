
# Blog :: Django Project
![Django](https://img.shields.io/badge/django-blog-green) ![HTML](https://img.shields.io/badge/HTML-blog-red) ![CSS](https://img.shields.io/badge/CSS-blog-blue)
![JS](https://img.shields.io/badge/JS-blog-orange) ![BOOTSTRAP](https://img.shields.io/badge/Bootstrap-blog-purple)
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info

This project is 3rd project in MaktabSharif Bootcamp that Python [+django framework], HTML, CSS, JS [+Bootstrap framework] used.
This project is a Blog that on users can write post and like or dislike posts and write comment for each post.

There are two type of users in this site:
* _Anonymous users_
* _Authenticated users_

Authenticated users in this site are divided into 4 groups with special permissions. this groups are:

* __Simple group__: Permissions for this group >>> can view posts, comments, like, dislike and star posts.[default authenticated users]
* __Writer group__: In addition to the previous group permissions, this group is allowed to write posts in site categories and add tags.
* __Editor group__: In addition to the previous group permissions, this group can edit, verify and activate posts and comments. 
* __Manager group__: this group of users have all permissions.[similar to superuser]


Some examples of photos from the blog site are displayed below:


<img src="maktablog/media/default/main_page.png"> <img src="maktablog/media/default/categories.png">
<img src="maktablog/media/default/post1.png"> <img src="maktablog/media/default/tagsLike.png"> <img src="maktablog/media/default/comment.png"> 

## Technologies
Project is created with:
* Python: 3.8
* Django: 3.1.4
* HTML
* CSS
* JavaScript
* Bootstrap


For more information go to requirements.txt file in repository.

	
## Setup

In first to start this project you have to create a virtual enviroment, so:
```
...\django_project_blog>python -m venv venv
```
After create venv, you should activate your venv, so:
```
...\django_project_blog>venv\Scripts\activate   <note:in windows command prompt>
```
Then, install all requirements on your venv:
```
...\django_project_blog\maktablog>pip install -r requirements.txt
```
After install all packages you should delete all files in folder migrations except \_\_init__.py that there is in this address:
```
...\django_project_blog\maktablog\blog\migrations
```
In next step, you should set your database and add local_settings.py like local_settings.py.sample file to project.
Then, you shoud use this commands for set superuser and database settings:
```
...\django_project_blog\maktablog>python manage.py createsuperuser
...\django_project_blog\maktablog>python manage.py makemigrations
...\django_project_blog\maktablog>python manage.py migrate

```
In final, for run default server django,go to maktablog directory and in terminal:

```
...\django_project_blog\maktablog>python manage.py runserver
```


##### Good Luck! :v::sunglasses:



