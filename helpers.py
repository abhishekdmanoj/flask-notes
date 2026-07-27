from flask import session, redirect
from functools import wraps

def login_required(func):
	
	@wraps(func)
	def wrapper(*args, **kwargs):
		if "user_id" not in session:
			return redirect("/")
		return fun(*args, **kwargs)

	return wrapper
