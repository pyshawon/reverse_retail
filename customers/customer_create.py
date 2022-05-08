import csv
import logging
from django.db import transaction
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from .models import Customer, Address, Bank

logger = logging.getLogger(__name__)

class CustomerCreateFromCSV:
	def __init__(self, file):
		self.file = file

	def create_customer(self):
		# Create Temporary Storage Location
		fs = FileSystemStorage(location='tmp/')

		content = self.file.read()
		# Save the CSV file into Temporary Location from In Memory.
		file_content = ContentFile(content)
		file_name = fs.save("_tmp.csv", file_content)
		tmp_file = fs.path(file_name)
		csv_file = open(tmp_file, errors="ignore")
		reader = csv.reader(csv_file)

		# Ignore CSV Header
		next(reader) 

		with transaction.atomic():
			# Max id form database or 0
			max_id = int(Customer.objects.last().id if Customer.objects.last() else 0)
			id_count = max_id

			customers_data_list = [] # Customer Bulk Data Holder
			customers_data_dict = {} # Customer Data Hash Map

			for id_, row in enumerate(reader):
				(
					last_name, 
					first_name, 
					address_street, 
					phone, 
					address_zipcode, 
					address_city,
					address_country,
					bank_account_no,
					bank_name,
					email
				) = row

				# Unique customer_key is consist of 'first_name'_'last_name'
				customer_key = f"{first_name}_{last_name}"

				# check if customer is already in hashmap, Just append the address.
				if customers_data_dict.get(customer_key):
					customers_data_dict.get(customer_key)["address"].append(
						{
							"street": address_street,
							"zipcode": address_zipcode,
							"country": address_country,
							"city": address_city,
						}
					)
				else:
					# Increase the id counter
					id_count += 1
					# Append Customer into hasmap
					customers_data_dict[customer_key] = {
						"first_name": first_name,
						"last_name": last_name,
						"phone": phone,
						"email": email,
						"address": [
							{
								"street": address_street,
								"zipcode": address_zipcode,
								"country": address_country,
								"city": address_city,
							}
						],
						"bank": {
							"bank_name": bank_name,
							"bank_account_no": bank_account_no
						}

					}

					# Append customer for Bulk Create
					customers_data_list.append(
						Customer(
							id=id_count,
							last_name=last_name,
							first_name=first_name,
							phone=phone,
							email=email
						)
					)

			# Customer Bulk Create 
			customer_objects = Customer.objects.bulk_create(customers_data_list)
			logger.debug("Customer created successfully from CSV.")

			address_data_list = [] # Address Bulk Data Holder
			bank_account_data_list = [] # Bank Bulk Data Holder

			# Loop over all the customer is created and assign customer ref. to address and bank
			for customer in customer_objects:

				# Unique customer_key is consist of 'first_name'_'last_name'
				customer_key = f"{customer.first_name}_{customer.last_name}"
				
				# check if customer is already in hashmap.
				if customers_data_dict.get(customer_key):
					for address in customers_data_dict.get(customer_key)['address']:
						# Append address for Bulk Create
						address_data_list.append(
							Address(
								customer=customer,
								street=address["street"],
								city=address["city"],
								zipcode=address["zipcode"],
								country=address["country"]
							)
						)

					if not customers_data_dict.get(customer_key)['bank']['bank_name'] == "":
						# Append Bank account for Bulk Create
						bank_account_data_list.append(
							Bank(
								customer=customer,
								name=customers_data_dict.get(customer_key)['bank']['bank_name'],
								account_no=customers_data_dict.get(customer_key)['bank']['bank_account_no']
							)
						)
				else:
					logger.debug(f"Customer with the key '{customer_key}' not found")

			# Address & Bank Bulk Create 
			Address.objects.bulk_create(address_data_list)
			logger.debug("Address created successfully from CSV.")

			Bank.objects.bulk_create(bank_account_data_list)
			logger.debug("Bank created successfully from CSV.")

		# Delete Temporary File 
		fs.delete(tmp_file)

		return True