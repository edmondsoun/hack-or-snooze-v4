# hack-or-snooze-v4

# IMPORTANT CHANGES FROM PREVIOUS BACKEND!

- Token now must be sent in the _header_, not the body.
- `request.auth` stores the return value our ApiKey auth class (currently
  "username")

### Endpoints

Include:

- Login ✅
- Signup ✅
- User (get/patch/) ✅
- Favorite (post/delete) ✅
- Stories (get/post/patch/delete) ✅
- Story (get) ✅

Exclude:

- Users (all)
- User (delete) []

### DOCUMENTATION

- docstrings for all endpoints ✅ (except the favorites endpoints)
- Write Summary and descriptions for Open API Docs ❌

### TESTING

- Testing of util functions ❌
- Testing of endpoints ❌

### DEPLOYMENT

- application deployed
- created seed data

# AT CURRENT VELOCITY:

- Finishing endpoints: 1/2 day
- Docs: 1/2 day
- Testing: 2~3 days
- Deployment: ? (depends on platform and DB configuration considerations)
- this won't be super hard with AWS, but probably slap it up at render

### Questions For Clarity

- How should we implement reseting the db? Should it have the same functionality
  as it does now, where it resets every hour?
  - no strong opinion on automatically resetting this
- Should we enforce a UUID at the database level? This could cause more cryptic
  errors at the point of validation. Should we instead just make this a str
  field and manually generate a UUID?✅
  - changed model field to CharField and set default to a stringified version of
    a UUID

# Test Scaffolding

## AUTH

### Views

- POST /api/users/signup

  - signup success✅
  - signup failure (missing required data)✅
  - signup failure (extra fields included)✅
  - signup failure (username already exists)✅
  - signup failure (malformed username)✅

- POST /api/users/login
  - login success✅
  - login failure (missing required data)✅
  - login failure (extra fields included)✅
  - login failure (non-existant username)✅
  - login failure (username exists; wrong password)✅

### auth_utils (unit testing)

- check_token
- generate_hash
- generate_token

## USER

### Admin

### Model
- validation error on blank first_name ✅
- validation error on blank last_name ✅

#### SIGNUP
- ok
- fail on duplicate username ✅

#### LOGIN
- ok
- fail incorrect password ✅
- fail nonexistent username ✅

#### UPDATE
- ok, no password ✅
- ok, with password ✅

### API

#### GET /{username}

- works ok w/ user token ✅
- works ok w/ staff token ✅
- 401 unauthorized if no token header (authentication) ✅
- 401 unauthorized if token header blank (authentication) ✅
- 401 unauthorized if malformed token (authentication) ✅
- 401 unauthorized if invalid token (authentication) ✅
- 401 unauthorized if different non-staff user's token (authorization) ✅
- 404 if user not found w/ staff token ✅

#### PATCH /{username}

- works ok as self, all fields submitted ✅
- works ok as self, only some fields submitted ✅
- works ok as self, updating password re-hashes before storing ✅
- works ok as staff, all fields submitted ✅
- works ok as staff, only some fields submitted ✅
- 401 unauthorized if no token (authentication) ✅
- 401 unauthorized if malformed token (authentication) ✅``
- 401 unauthorized if invalid token (authentication) ✅
- 401 unauthorized if different non-staff user's token (authorization) ✅
- 404 if user not found w/ staff token ✅
- 422 if extra fields submitted✅
- error if no fields submitted ⚠️ - needs validator updates to pass
- error if fields contain blank strings as values ⚠️ - needs validator updates to pass

## FAVORITES

### API

#### POST /{username}/favorites

- works ok w/ user token ✅
- works ok w/ staff token ✅
- 401 unauthorized if no token (authentication) ✅
- 401 unauthorized if malformed token (authentication) ✅
- 401 unauthorized if invalid token (authentication) ✅
- 401 unauthorized if different non-staff user's token (authorization) ✅
- OTHER TESTS:
- favorite record is not duplicated when added twice ✅
- 400 user cannot add a story they posted to their favorites ✅
- 404 if {username} not found w/ staff token ✅
- 404 if story_id not found w/ valid user token ✅
- 404 if story_id not found w/ staff token ✅

#### DELETE /{username}/favorites

- works ok w/ user token ✅
- works ok w/ staff token ✅
- 401 unauthorized if no token (authentication) ✅
- 401 unauthorized if malformed token (authentication) ✅
- 401 unauthorized if invalid token (authentication) ✅
- 401 unauthorized if different non-staff user's token (authorization) ✅
- OTHER TESTS:
- works ok to DELETE same story_id twice ✅
- works ok to DELETE story not in favorites ✅
- 404 if {username} not found w/ staff token ✅
- 404 if story_id not found w/ valid user token ✅
- 404 if story_id not found w/ staff token ✅

- test this works with both same user and auth user

## STORY

### Admin

### Model
- smoke test ✅
- id is str ✅

### API

#### POST /

- works ok w/ user token ✅
- works ok w/ staff token ✅
- 401 unauthorized if no token (authentication)✅
- 401 unauthorized if malformed token (authentication)✅
- 401 unauthorized if invalid token (authentication)✅

###### OTHER TESTS:

- 422 missing data✅
- 422 extra data✅
- 422 no data✅
- 422 data wrong type✅

#### GET /

- works ok✅

##### GET /{story_id}

- works ok✅
- 404 if user not found✅

##### DELETE /stores/{story_id}

- works ok w/ user token✅
- works ok w/ staff token✅
- 401 unauthorized if no token (authentication)✅
- 401 unauthorized if malformed token (authentication)✅
- 401 unauthorized if invalid token (authentication)✅
- 401 unauthorized if different non-staff user's token (authorization)✅

###### OTHER TESTS:

- 404 if story_id not found✅

# INTERNAL RUNNING NOTES:

# TOP-LEVEL TODO:

- Seed data for production
- Set up admin to allow quick post/user deletes
- Way to handle dumping the DB (solved by Django-Ninja?)
- Write tests
  - Set up factories for testing

# DOCS TODO:

- Update PLACEHOLDER in all routes
- Clean up formatting of docstring insertion

<!-- # Learnings From Cupcakes
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
  default None established in the Schema -->
