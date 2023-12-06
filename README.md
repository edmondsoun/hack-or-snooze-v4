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
