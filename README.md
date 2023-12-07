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

# Learnings From Cupcakes
- Schemas can have a class Config with attr exclude to allow or deny additional arguments in the payload
- setting response in the api decorator will type the response for Open API documentation. We'll need to do this for every route otherwise it will use "str" by default
- be mindful of naming for the schemas. These will be directly used on the generated documentation.
- using default values in the schemas (set to None) will allow us to have optional fields (for something like a patch request). However, the caveat is that we need to iterate over that payload using `exclude_unset=True`. Without this, 
  we will get database errors when it tries to set Null values from that default None established in the Schema
