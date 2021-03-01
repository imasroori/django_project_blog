
# Blog :: Django Project

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info

This project is 3rd project in MaktabSharif Bootcamp that Python [+django framework], HTML, CSS, JS [+Bootstrap framework] used.
This project is a Blog that on users can write post and like or dislike posts and write comment for each post.

There are two type of users in this site:
* Anonymous users
* Authenticated users

Authenticated users in this site are divided into 4 groups with special permissions. this groups are:

* Simple group: Permissions for this group >>> can view posts, comments, like, dislike and star posts.[default authenticated users]
* Writer group: In addition to the previous group permissions, this group is allowed to write posts in site categories and add tags.
* Editor group: In addition to the previous group permissions, this group can edit, verify and activate posts and comments. 
* Manager group: this group of users have all permissions.[similar to superuser]
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
To run this project, install all requirements:
```
pip install requirements.txt
```
After install all packages you can run server and visit the site and signup!

Go to maktablog directory and in terminal:

```
...\maktablog> python manage.py runserver
```


<img src="maktablog/media/default/main_page.png" width="425" height="425"> <img src="maktablog/media/default/main_page.png" width="425" height="425">
<img src="maktablog/media/default/main_page.png" width="425" height="425"> <img src="maktablog/media/default/main_page.png" width="425" height="425">

##### Good Luck!



