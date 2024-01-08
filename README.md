# hack-or-snooze-v4

# RUNNING IMPORTANT NOTES!

- Token now must be sent in the *header*, not the body.
- `request.auth` stores the return value our ApiKey auth class (currently "username")

# TOP-LEVEL TODO:
- Seed data for production ❌
- Set up admin to allow quick post/user deletes ✅ (done with django admin)
- Way to handle reseting the DB (solved by Django-Ninja?) ❌
- Write tests ❌
  - Set up factories for testing

# DOCS TODO:
- Update PLACEHOLDER in all routes
- Clean up formatting of docstring insertion



# CURRENT STATUS
### ENDPOINTS
- Login ✅
- Signup ✅
- User (get/patch/) ✅
- Favorite (post/delete) ❌
- Stories (get/post/patch/delete) ✅
- Story (get) ✅

### DOCUMENTATION
- docstrings for all endpoints ✅ (except the favorites endpoints)
- Write Summary and descriptions for Open API Docs ❌

### TESTING
- Testing of util functions ❌
- Testing of endpoints ❌

### DEPLOYMENT
- application deployed
- created seed data


Exclude:
- Users (all)
- User (delete) []

### Questions For Clarity
- How should we implement reseting the db? Should it have the same functionality as it does now, where it resets every hour?
- Do we want to implement a route to edit/patch user stories? This exists as a piece in the FS for this project currently
- Should we enforce a UUID at the database level? This could cause more cryptic errors at the point of validation. Should we instead just make this a str field and manually generate a UUID?

# Test Scaffolding

## AUTH
### Views
- POST /api/users/signup
  - signup success
  - signup failure (missing required data)
  - signup failure (extra fields included)
  - signup failure (username already exists)
  - signup failure (malformed username)

- POST /api/users/login
  - login success
  - login failure (missing required data)
  - login failure (extra fields included)
  - login failure (non-existant username)
  - login failure (username exists; wrong password)

### Utils (unit testing)
- check_token
- generate_hash
- generate_token


## USER
### Admin
### Model
### Views

## FAVORITE
### Admin
### Model
### Views

## STORY
### Admin
### Model
### Views


# Learnings From Cupcakes
- Schemas can have a class Config with attr exclude to allow or deny additional
  arguments in the payload
- setting response in the api decorator will type the response for Open API
  documentation. We'll need to do this for every route otherwise it will use
  "str" by default
- be mindful of naming for the schemas. These will be directly used on the
  generated documentation.
- using default values in the schemas (set to None) will allow us to have
  optional fields (for something like a patch request). However, the caveat is
  that we need to iterate over that payload using `exclude_unset=True`. Without
  this, we will get database errors when it tries to set Null values from that
  default None established in the Schema