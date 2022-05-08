from pathlib import Path
from unittest.mock import patch
from django.test import TestCase, Client
from .models import Customer, Address, Bank


class CustomerCreateFromCSVTestCase(TestCase):
	"""
	Test Case for Customer create form CSV file.
	"""
	def setUp(self):
		self.client = Client()
		# Sample CSV file path
		self.sample1_file_path = Path(__file__).resolve().parent / 'sample_csv/sample1.csv'
		self.sample2_file_path = Path(__file__).resolve().parent / 'sample_csv/sample2.csv'


	def test_home_page(self):
		response = self.client.get("/")
		# Check home page
		self.assertEqual(response.status_code, 200)

	def test_customer_model(self):
		# Simple test for customer model
		customer_obj = Customer.objects.create(
			first_name="test",
			last_name="customer",
			phone="1111111111",
			email="test@test.com"
		)

		self.assertTrue(customer_obj)
		self.assertEqual(customer_obj.first_name, "test")


	def test_address_model(self):
		# Simple test for address model
		customer_obj = Customer.objects.create(
			first_name="test",
			last_name="customer",
			phone="1111111111",
			email="test@test.com"
		)
		address_obj = Address.objects.create(
			customer=customer_obj,
			street="abc",
			city="Dhaka",
			zipcode=1230,
			country='BD'
		)

		self.assertTrue(address_obj)
		self.assertEqual(address_obj.street, "abc")
		self.assertEqual(address_obj.customer.first_name, "test")

	def test_bank_model(self):
		# Simple test for bank model
		customer_obj = Customer.objects.create(
			first_name="test",
			last_name="customer",
			phone="1111111111",
			email="test@test.com"
		)
		bank_obj = Bank.objects.create(
			customer=customer_obj,
			name="DBBL",
			account_no="123456789"
		)

		self.assertTrue(bank_obj)
		self.assertEqual(bank_obj.name, "DBBL")
		self.assertEqual(bank_obj.customer.first_name, "test")

	@patch('customers.views.logger')
	def test_customer_create_success(self, logger):
		# Open the file form file path
		with open(self.sample1_file_path, 'rb') as csv_file:
			# Data dict for POST Request
			data = {
				'csv_file': [csv_file]
			}
			# Sending POST request to create customer.
			customer_response = self.client.post("/", data, format="multipart")

			# Queryset for Customer, Address and Bank
			customer_qs = Customer.objects.all()
			address_qs = Address.objects.all()
			bank_qs = Bank.objects.all()

			#Check Response code and number of row created in database.
			self.assertEqual(customer_response.status_code, 200)
			self.assertEqual(customer_qs.count(), 25)
			self.assertEqual(address_qs.count(), 29)
			self.assertEqual(bank_qs.count(), 4)

			# Check customer first name & last name
			self.assertEqual(customer_qs.first().first_name, "Zelmira")
			self.assertEqual(customer_qs.first().last_name, "Amojan")

			# Check Logger Message
			logger.debug.assert_called_with("CSV Execute Successfully.")


	@patch('customers.views.logger')
	def test_customer_create_without_csv_failed(self, logger):
		# Data dict for POST Request
		data = {}
		# Sending POST request with no csv file.
		customer_response = self.client.post("/", data, format="multipart")

		# Check Logger Message
		logger.debug.assert_called_with("Please select a valid csv file.")


	@patch('customers.views.logger')
	def test_customer_create_with_csv_failed(self, logger):
		# Open the file form file path
		with open(self.sample2_file_path, 'rb') as csv_file:
			# Data dict for POST Request
			data = {
				'csv_file': [csv_file]
			}
			# Sending POST request to create customer.
			customer_response = self.client.post("/", data, format="multipart")

			#Check Response code and number of row created in database.
			self.assertEqual(customer_response.status_code, 200)

			# Check Logger Message
			logger.debug.assert_called_with("Please select a valid csv file. or Check debug.info.log file for more details.")


