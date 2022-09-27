from models import User
def get_user_by_id(id: int) -> User.Model:
	user = User.Model(
		id = id,
		username = "umutaev",
		email = "max@umutaev.ru",
		hashed_password = "$2b$12$h0HEeJkRlK.J3JtnoipyQOstVLLozCjq3n4zNOE4JwCFfEA0k9kw6"
		)
	return user
def get_user_by_username(username: str) -> User.Model:
	user = User.Model(
		id = 1,
		username = "umutaev",
		email = "max@umutaev.ru",
		hashed_password = "$2b$12$h0HEeJkRlK.J3JtnoipyQOstVLLozCjq3n4zNOE4JwCFfEA0k9kw6"
		)
	return user