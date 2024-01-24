# hack-or-snooze-v4

# IMPORTANT CHANGES FROM PREVIOUS BACKEND!

- Token now must be sent in the _header_, not the body.
- `request.auth` stores the return value our ApiKey auth class (currently
  "user")

# POST-CODE REVIEW NOTES
## DOCS
- Use docstrings for route descriptions (use RST for formatting)
- Update name from DjangoNinja at top✅
- Add summary of "how to use API" at top✅
  - Doesn't need to be a hand-holdy description; just "how to use API"
    - How do you register
    - How do you get a token
    - How do you use that token

## USER MODEL
- Auth: check for built-in methods.
  - Add contraint to password with minimum length.
  - Login: can we use the built in method?

## USERS ROUTES
### AUTH
- Add a test that shows a hyphen/underscore is valid.
  - Rename global constant from ALPHANUMERIC... to SLUGIFIED...?
- Need to test and make totally sure they cannot sign *up* with an empty
    fn/ln.

### PATCH
- Remove validation for empty string entirely
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
