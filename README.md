# hack-or-snooze-v4

# IMPORTANT CHANGES FROM PREVIOUS BACKEND!

- Token now must be sent in the _header_, not the body.
- `request.auth` stores the return value our ApiKey auth class (currently
  "user")

# Final cleanup TODO:
- normalize all tests to "fails_" instead of "fail_"
- set up admin to allow quick post/user deletes
- trailing commas :)

# NICETOHAVE:
- custom error messages for endpoints where user or story could raise 404
- set DB to automatically purge and reset to seed data periodically
- Seed data for production

# DOCS TODO:

- Update PLACEHOLDER in all routes
- Clean up formatting of docstring insertion