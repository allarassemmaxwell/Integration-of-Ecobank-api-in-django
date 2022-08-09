from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.utils.translation import activate, gettext_lazy as _
from .forms import *
from .models import *
from django.contrib import messages

from datetime import date, timedelta
import random
from django.http import HttpResponse

from .serializers import *

from django.core.paginator import Paginator
from django.conf import settings

from django.db.models import Q

from decimal import Decimal

from django.views.decorators.csrf import csrf_exempt

from django.urls import reverse_lazy




import requests
import json
import hashlib




def generate_secure_hash():

	url = "https://developer.ecobank.com/corporateapi/merchant/securehash"

	payload = "{\n \"param1\":\"Aymard\",\n \"param2\":\"Gildas\",\n \"param3\":\"MILANDOU\",\n \"param4\":\"Ecobank\",\n \"param5\":\"Group\",\n \"secureHash\": \"5dfa1f87465133c388fe49be7db74c0b9ff4155cac2387efde9e34e9c654c5d642c10896285f1647b41d31e1302a26bf861399dd1010aeb8762fed75847377bc\"\n}"
	headers = {
	  'Origin': 'developer.ecobank.com'
	}

	response = requests.request("POST", url, headers=headers, data=payload)

	print(response.text)



    # secure_hash=hashlib.sha512(settings.ECOBANK_API_LAB_KEY.encode('utf-8')).hexdigest()
    # return secure_hash





def generate_token():
	url = "https://developer.ecobank.com/corporateapi/user/token"

	payload = json.dumps({
		"userId": settings.ECOBANK_API_USER_ID,
		"password": settings.ECOBANK_API_USER_PASSWORD
	})
	headers = {
		'Content-Type': 'application/json',
		'Accept': 'application/json',
		'Origin': settings.ECOBANK_API_ORIGIN_URL
	}
	response  = requests.request("POST", url, headers=headers, data=payload)
	json_resp = response.json()
	return json_resp['token']







# GENERATE RANDOM STRING WITH LENGTH 
def random_alpha_numeric(num):   
    res = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(num))  
    return str(res)





# LANDING FUNCTION
def home_view(request):
	payments = MonthlyPayment.objects.all()
	context  = {}
	template = "base.html"
	return render(request, template, context)






def payment_view(request):
	if request.method == 'POST':

		# =================================================
		# 					CARD PAYMENT
		# =================================================
		url = "https://developer.ecobank.com/corporateapi/merchant/Signature"
		payload = json.dumps({
			"paymentDetails": {
				"requestId": random_alpha_numeric(13),
				"productCode": "2310",
				"amount": "10",
				"currency": "USD",
				"locale": "en_AU",
				"orderInfo": "b5f7f31d-9a4e-4c5c-a948-ab7642f8ece4",
				"returnUrl": "https://www.ecobank.com/unified"
			},
		 	"merchantDetails": {
			    "accessCode": "31a95cc023dd35b88d4cad5e7f08fd9b",
			    "merchantID": "902412B0-39DA-494A-9BDB-89DE3C10D38B",
			    "secureSecret": "8c6509c21928433887afdacab29de9c55089cfad14304567a22544828e427e04c622a7010d7c4b5ab078f493b1be55de9637979a782d45b996ffe57dc41c2e9881b69b9141e142ea9329689de14b96ca0c4e6b9a5de043169b92e8a7fe6f2da2f4660b8fb19148beb4fdb6d909008a85225d5bf743a0477abed94ad73423f51d"
		  	},
		  	"secureHash": "1be4bf59f4917a306005fd8178b8ae9ac385b832a94b15c7a87945cf374edab099e9735379833a01053c33f0edae94ebd0ffa8beb5680871e78c3b7630582331"
		})
		headers = {
			'Authorization': 'Bearer '+access_token,
			'Content-Type': 'application/json',
			'Accept': 'application/json',
			'Origin': settings.ECOBANK_API_ORIGIN_URL
		}

		response  = requests.request("POST", url, headers=headers, data=payload)
		json_resp = response.json()
		print("====================================================")
		print(json_resp['response_code'])
		print("\n")
		print(json_resp['response_message'])
		print("\n")
		# print(json_resp['response_content'])
		print("\n")
		print(json_resp['response_timestamp'])
		print("====================================================")




		# =================================================
		# 			MERCHANT CATEGORY CODE (MMC)
		# =================================================
		# url = "https://developer.ecobank.com/corporateapi/merchant/getmcc"
		# payload = json.dumps({
		# 	"requestId": "123344",
		# 	"affiliateCode": "EGH",
		# 	"requestToken": "/4mZF42iofzo7BDu0YtbwY6swLwk46Z91xItybhYwQGFpaZNOpsznL/9fca5LkeV",
		# 	"sourceCode": "ECOBANK_QR_API",
		# 	"sourceChannelId": "KANZAN",
		# 	"requestType": "CREATE_MERCHANT"
		# })
		# headers = {
		# 	'Authorization': 'Bearer '+access_token,
		# 	'Content-Type': 'application/json',
		# 	'Accept': 'application/json',
		# 	'Origin': 'developer.ecobank.com'
		# }
		# response = requests.request("POST", url, headers=headers, data=payload)
		# print(response.text)






		# =================================================
		# 			PAYMENT(TRANSFER)
		# =================================================

		# url = "https://developer.ecobank.com/corporateapi/merchant/payment"

		# payload = json.dumps({
		# 	"paymentHeader": {
		# 		"clientid": "EGHTelc000043",
		# 		"batchsequence": "1",
		# 		"batchamount": 170,
		# 		"transactionamount": 170,
		# 		"batchid": "EG1593490",
		# 		"transactioncount": 3,
		# 		"batchcount": 3,
		# 		"transactionid": "E12T443308",
		# 		"debittype": "Multiple",
		# 		"affiliateCode": "EGH",
		# 		"totalbatches": "1",
		# 		"execution_date": "2020-06-01 00:00:00"
		# 	},
		#   	"extension": [
		# 	    {
		# 	      "request_id": "2323",
		# 	      "request_type": "domestic",
		# 	      "param_list": "[{\"key\":\"creditAccountNo\", \"value\":\"1441001996321\"},{\"key\":\"debitAccountBranch\", \"value\":\"ACCRA\"},{\"key\":\"debitAccountType\", \"value\":\"Corporate\"},{\"key\":\"creditAccountBranch\", \"Accra\":\"GHS\"},{\"key\":\"creditAccountType\", \"value\":\"Corporate\"},{\"key\":\"amount\", \"value\":\"10\"},{\"key\":\"ccy\", \"value\":\"GHS\"}]",
		# 	      "amount": 50,
		# 	      "currency": "GHS",
		# 	      "status": "",
		# 	      "rate_type": "spot"
		# 	    },
		# 	    {
		# 	      "request_id": "432",
		# 	      "request_type": "token",
		# 	      "param_list": "[{\"key\":\"transactionDescription\", \"value\":\"Service payment for electrical repairs.\"},{\"key\":\"secretCode\", \"value\":\"AWER1234\"},{\"key\":\"sourceAccount\",\"value\":\"1441000565307\"},{\"key\":\"sourceAccountCurrency\", \"value\":\"GHS\"},{\"key\":\"sourceAccountType\", \"value\":\"Corporate\"},{\"key\":\"senderName\", \"value\":\"Freeman Kay\"},{\"key\":\"ccy\", \"value\":\"GHS\"},{\"key\":\"senderMobileNo\", \"value\":\"0202205113\"},{\"key\":\"amount\", \"value\":\"40\"},{\"key\":\"senderId\", \"value\":\"QWE345Y4\"},{\"key\":\"beneficiaryName\", \"value\":\"Stephen Kojo\"},{\"key\":\"beneficiaryMobileNo\", \"value\":\"0233445566\"},{\"key\":\"withdrawalChannel\", \"value\":\"ATM\"}]",
		# 	      "amount": 50,
		# 	      "currency": "GHS",
		# 	      "status": "",
		# 	      "rate_type": "spot"
		# 	    },
		# 	    {
		# 	      "request_id": "2325",
		# 	      "request_type": "INTERBANK",
		# 	      "param_list": "[{\"key\":\"destinationBankCode\", \"value\":\"ASB\"},{\"key\":\"senderName\", \"value\":\"BEN\"},{\"key\":\"senderAddress\", \"value\":\"23 Accra Central\"},{\"key\":\"senderPhone\", \"value\":\"233263653712\"},{\"key\":\"beneficiaryAccountNo\",\"value\":\"110424812001\"},{\"key\":\"beneficiaryName\", \"value\":\"Owen\"},{\"key\":\"beneficiaryPhone\", \"value\":\"233543837123\"},{\"key\":\"transferReferenceNo\", \"value\":\"QWE345Y4\"},{\"key\":\"amount\", \"value\":\"10\"},{\"key\":\"ccy\", \"value\":\"GHS\"},{\"key\":\"transferType\", \"value\":\"spot\"}]",
		# 	      "amount": 70,
		# 	      "currency": "GHS",
		# 	      "status": "",
		# 	      "rate_type": "spot"
		# 	    }
		#   	],
		#   	"secureHash": "7f137705f4caa39dd691e771403430dd23d27aa53cefcb97217927312e77847bca6b8764f487ce5d1f6520fd7227e4d4c470c5d1e7455822c8ee95b10a0e9855"
		# })
		# headers = {
		# 	'Origin': 'developer.ecobank.com',
		# 	'Authorization': 'Bearer '+access_token,
		# 	'Accept': 'application/json',
		# 	'Content-Type': 'application/json'
		# }

		# response = requests.request("POST", url, headers=headers, data=payload)

		# print(response.text)


		return redirect('home')
	else :
		form = MonthlyPaymentForm()
	context  = {'form': form}
	template = "payment.html"
	return render(request, template, context)



