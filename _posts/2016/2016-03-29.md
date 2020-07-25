+++
date = "2016-03-29T23:05:04Z"
title = "Contribution streak: Working on a project without learning the framework"
type = "journal"
+++

Only one commit tonight, sorry. I've bungled my way through the routes file
and submitting a form, but am not yet creating a model to add to the user.
What I think I have left:

* Add an API key when you're asked to in the UI
* Create a default API key for new users
* Add seeds for API keys to allow tests
* Create a migration which adds `ApiKey` models to match existing users'
  `api_key` fields.
* Fix up the login checks to actually authenticate API requests against the
  new model (oh yeah, that!)

Bonus round:

* Maybe add some tests around adding and revoking keys
