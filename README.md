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

## USER MODEL
- Auth: check for built-in methods.
    - updated login logic to use `authenticate` from Django.✅
    - updated signup logic to now use `create_user` paired with `User.get.filter.exists`✅
    - removed existing `signup` and `login` model methods, logic for login/signup now lives in the route✅

## USERS ROUTES
### AUTH
- Add a test that shows a hyphen/underscore is valid in username.✅
- Rename global constant from ALPHANUMERIC... to SLUGIFIED...?
- Updated Signup validation to ensure minimum lengths for `first_name`, `last_name`,
  and `password`✅
  - NOTE: This validation is done at the Schema level.
- Added test for min_length validation on signup for `first_name`, `last_name`, `password`✅
  - NOTE: The user model is unchanged. No constraints at the model level.

### PATCH
- Remove validation for empty string and empty body entirely✅
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
