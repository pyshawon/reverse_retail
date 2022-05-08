import logging
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import CreateView
from .customer_create import CustomerCreateFromCSV
# Create your views here.

logger = logging.getLogger(__name__)

class CustomerCreateView(CreateView):
	"""
	A simple View for Create Customer form csv file.
	"""
	template_name = "home.html"

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, {})

	def post(self, request, *args, **kwargs):
		# Get File form Request
		file = request.FILES.get("csv_file")
		# Check if the file file exists then call the CustomerCreateFromCSV class.
		if file:
			# Try block for catch not valid .csv file
			try:
				customer_csv = CustomerCreateFromCSV(file)
				customer_csv.create_customer()
				logger.debug("CSV Execute Successfully.")
				messages.success(request, "Customer created successfully from CSV.")
			except Exception as e:
				logger.debug(e)
				logger.debug("Please select a valid csv file. or Check debug.info.log file for more details.")
				messages.error(request, "Please select a valid csv file. or Check debug.info.log file for more details.")
		else:
			logger.debug("Please select a valid csv file.")
			messages.error(request, "Please select a valid csv file.")

		return render(request, self.template_name, {})
