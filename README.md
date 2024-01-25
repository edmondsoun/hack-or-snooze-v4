# hack-or-snooze-v4

# IMPORTANT CHANGES FROM PREVIOUS BACKEND!

- Token now must be sent in the _header_, not the body.
- `request.auth` stores the return value our ApiKey auth class (currently
  "user")

# POST-CODE REVIEW NOTES
## DOCS✅
- Use docstrings for route descriptions (use RST for formatting)✅
- Update name from DjangoNinja at top✅
- Add summary of "how to use API" at top✅
  - Doesn't need to be a hand-holdy description; just "how to use API"
    - How do you register
    - How do you get a token
    - How do you use that token

## USER MODEL
- Auth: check for built-in methods.
  - Add contraint to password with minimum length.❌
    - no action needed. App does *not* need to be secure per Joel
  - Login: can we use the built in method?❌
    - `login()` in Django will allow us to create a session with the user. We
      don't need or want to save a session, and as far as I can tell doesn't actually
      authenticate the user anyways.
    - same ideas here. Django has a built in `authenticate` method that does much of the
      same work as what we have in our model method.
  - Signup: can we use the built in `create_user`❌
    - after testing, it seems that create_user will not be a great choice since it 
    does not check if a user already exists before running. In fact, the method will
    mutate an existing user in this application if one already exists. We could use 
    `User.objects.get()` and then catch the `ObjectDoesNotExist` error, but this feels
    very gross to instantiate a new user. The way we have is working and doing mostly
    the same thing with a more understandable pattern.
    - Follow Up with Joel: don't take the responsibility of handling the password away from Django.
      Another issue to consider is race conditions when creating a user. We can use `@transaction.atomic`
      decorator to ensure that a username is not duplicated in the middle of a transaction.

## USERS ROUTES
### AUTH
- Add a test that shows a hyphen/underscore is valid.
  - Rename global constant from ALPHANUMERIC... to SLUGIFIED...?
- Need to test and make totally sure they cannot sign *up* with an empty
    fn/ln.

### PATCH
- Remove validation for empty string entirely✅
  - if they really want an empty string it can be an empty string

## FAVORITES
- Create "Favorites" application
- Create "Favorites" model and pass this model to User in ManyToManyField?
  - Need to research this.

- Restructure favorites endpoints. (Don't spend more than a day on this.)
  - POST /favorites/{username}/{story_id}/favorite
  - POST /favorites/{username}/{story_id}/unfavorite
    - Throw bad request error if trying to add an existing favorite
    - Throw bad request error if trying to delete a favorite that doesn't exist
      (look in the actual favorites table for the relationship)



# NICETOHAVE for deployed version:
- Set DB to automatically purge and reset to seed data periodically
- Seed data for production
