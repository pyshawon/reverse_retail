from django.db import models

# Create your models here.

class Customer(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	phone = models.CharField(max_length=20, null=True, blank=True)
	email = models.CharField(max_length=50, null=True, blank=True)

	def __str__(self):
		return f"{self.first_name} {self.last_name}"

class Address(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	street = models.CharField(max_length=100, null=True, blank=True)
	city = models.CharField(max_length=50, null=True, blank=True)
	zipcode = models.CharField(max_length=50, null=True, blank=True)
	country = models.CharField(max_length=50, null=True, blank=True)

	def __str__(self):
		return f"{self.customer}: {self.street}, {self.city}, {self.zipcode}, {self.zipcode}"

class Bank(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	account_no = models.CharField(max_length=50)

	def __str__(self):
		return f"{self.customer}: {self.name} {self.account_no}"