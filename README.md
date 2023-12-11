# hack-or-snooze-v4

- Only the API endpoints we use
- Well-documented (solved by Django-Ninja?)
- Way to handle dumping the DB (solved by Django-Ninja?)

Step 0: Figure out our API design
Step 1: Make Flask-cupcakes in Django-ninja (no auth to start)
Step 2: Add auth (Django-knox? Default?)

### Endpoints
Include (main):
- Login
- Signup
- Favorite (post/delete)
- Stories (get/post)
- Story (get)

Include (FS):
- User (get/update)
- Story (update/delete)

Exclude:
- Users (all)
- User (delete)

### Data Model

Users
- username < PK
- name
- createdat
- modifiedat

Stories
- story_id < PK: UUID auto-generated in PSQL
- username < FK: user who posted
- author
- title
- url
- createdat
- modifiedat

Favorites
[compound primary key]
- username
- story_id

Tokens (MD5 hash username and use first 12 characters)
[unique together]
- token < PK
- username < FK