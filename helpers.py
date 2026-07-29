from flask import session, redirect
from functools import wraps

def login_required(func):
	
	@wraps(func)
	def wrapper(*args, **kwargs):
		if "user_id" not in session:
			return redirect("/")
		return func(*args, **kwargs)

	return wrapper


def isEmpty(note):

	note = note.strip()
	
	if not note:
		
		return True

	return False
