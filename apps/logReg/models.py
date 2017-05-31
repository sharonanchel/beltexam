from __future__ import unicode_literals
# from Ipython import embed
from django.db import models
import bcrypt
import re

NAME_REGEX = re.compile(r'^[a-zA-Z.-]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def register(self, postData):

		errors = []

		# Validate first name
		if len(postData['first_name']) < 2:
			errors.append('First name cannot be less than 2 characters.')
		elif not NAME_REGEX.match(postData['first_name']):
			errors.append('First name cannot contain numbers.')
		# Validate last name
		if len(postData['last_name']) < 2:
			errors.append('Last name cannot be less than 2 characters,')
		elif not NAME_REGEX.match(postData['last_name']):
			errors.append('last name cannot contain numbers.')
		# Validate email
		if len(postData['email']) < 1:
			errors.append('Email cannot be empty.')
		elif not EMAIL_REGEX.match(postData['email']):
			errors.append('Email is invalid.')
		# Validate password
		if len(postData['password']) < 8:
			errors.append('Passwords must be at least 8 characters.')
		# Validate confirm password
		elif postData['password'] != postData['confirm_pw']:
			errors.append('password do not match.')

		# search for email in database
		if User.objects.filter(email=postData['email']):
			errors.append('Email already exists.')

		return errors

	def create_user(self, postData):
			hashed_pw = bcrypt.hashpw(postData['password'].encode('utf-8'), bcrypt.gensalt())

			new_user = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], hashed_pw=hashed_pw)
			return new_user.id

	def login(self, postData):

		errors = []

		if not User.objects.filter(email=postData['email']):
			errors.append('Username and/or password are invalid.')
		else:
			if bcrypt.hashpw(postData['password'].encode('utf-8'), User.objects.get(email=postData['email']).hashed_pw.encode('utf-8')) != User.objects.get(email=postData['email']).hashed_pw:
				errors.append('Username and/or password are invalid.')

		return errors

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	hashed_pw = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()
