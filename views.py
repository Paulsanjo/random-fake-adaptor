from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
import jwt
from .models import User, Airport, Address, City, Customer, HotelDetails, HotelSearchRequest, HotelSearchResponse, RoomType, Traveler, PaymentCardParameters
import datetime
from django.contrib import auth
from django.conf import settings
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import UserSerializer, LoginSerializer, AirportSerializer, AddressSerializer, CitySerializer, CustomerSerializer, HotelDetailsSerializer, HotelSearchRequestSerializer, HotelSearchResponseSerializer, RoomTypeSerializer, TravelerSerializer, PaymentCardParametersSerializer
import pytz
from rest_framework import permissions
import requests
from django.http import JsonResponse
import redis
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
# Create your views here.
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
								  port=settings.REDIS_PORT, db=0)


class RegisterView(GenericAPIView):
	serializer_class = UserSerializer

	def post(self, request):
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(GenericAPIView):
	serializer_class = LoginSerializer

	def post(self, request):
		data = request.data
		email = data.get('email', '')
		password = data.get('password', '')
		user = auth.authenticate(email=email, password=password)

		if user:
			payload = {
			"email": email,
			'exp': datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE)) + datetime.timedelta(days=300)
			}
			auth_token = jwt.encode(payload, settings.JWT_SECRET_KEY, 'HS256')
			serializer = UserSerializer(user)
			data = {'user': serializer.data, 'token': auth_token}
			return Response(data, status=status.HTTP_200_OK)# SEND RES
		return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

##############   AIRPORT VIEW ##################

class AirportView(ListCreateAPIView):
	serializer_class = AirportSerializer
	permission_classes = [permissions.IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save()

	def get_queryset(self):
		return Airport.objects.all()
	

	@method_decorator(vary_on_cookie)
	@method_decorator(cache_page(60*60))
	def dispatch(self, *args, **kwargs):
		return super(AirportView, self).dispatch(*args, **kwargs)


class AirportDetailView(RetrieveUpdateDestroyAPIView):
	queryset = Airport.objects.all()
	serializer_class = AirportSerializer
	permission_classes = [permissions.IsAuthenticated,]
	lookup_field = "id"


##############   ADDRESS VIEW ##################

class AddressView(ListCreateAPIView):
	serializer_class = AddressSerializer
	permission_classes = [permissions.IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save()

	def get_queryset(self):
		return Address.objects.all()


class AddressDetailView(RetrieveUpdateDestroyAPIView):
	queryset = Address.objects.all()
	serializer_class = AddressSerializer
	permission_classes = [permissions.IsAuthenticated,]
	lookup_field = "id"


##############   CITY VIEW ##################

class CityView(ListCreateAPIView):
	serializer_class = CitySerializer
	permission_classes = [permissions.IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save()

	def get_queryset(self):
		return City.objects.all()

	
	@method_decorator(vary_on_cookie)
	@method_decorator(cache_page(60*60))
	def dispatch(self, *args, **kwargs):
		return super(CityView, self).dispatch(*args, **kwargs)




class CityDetailView(RetrieveUpdateDestroyAPIView):
	queryset = City.objects.all()
	serializer_class = CitySerializer
	permission_classes = [permissions.IsAuthenticated,]
	lookup_field = "id"


##############   CUSTOMER VIEW ##################

class CustomerView(ListCreateAPIView):
	serializer_class = CustomerSerializer
	permission_classes = [permissions.IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save()

	def get_queryset(self):
		return Customer.objects.all()

	@method_decorator(vary_on_cookie)
	@method_decorator(cache_page(60*60))
	def dispatch(self, *args, **kwargs):
		return super(AirportView, self).dispatch(*args, **kwargs)




class CustomerDetailView(RetrieveUpdateDestroyAPIView):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer
	permission_classes = [permissions.IsAuthenticated,]
	lookup_field = "id"


##############   HOTELDETAILS VIEW ##################

class HotelDetailsView(ListCreateAPIView):
	serializer_class = HotelDetailsSerializer
	permission_classes = [permissions.IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save()

	def get_queryset(self):
		return HotelDetails.objects.all()


class HotelDetailsDetailView(RetrieveUpdateDestroyAPIView):
	queryset = HotelDetails.objects.all()
	serializer_class = HotelDetailsSerializer
	permission_classes = [permissions.IsAuthenticated,]
	lookup_field = "id"


##############   HOTELSEARCHREQUEST VIEW ##################

class HotelSearchRequestView(ListCreateAPIView):
	serializer_class = HotelSearchRequestSerializer
	permission_classes = [permissions.IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save()

	def get_queryset(self):
		return HotelSearchRequest.objects.all()


class HotelSearchRequestDetailView(RetrieveUpdateDestroyAPIView):
	queryset = HotelSearchRequest.objects.all()
	serializer_class = HotelSearchRequestSerializer
	permission_classes = [permissions.IsAuthenticated,]
	lookup_field = "id"


##############   HOTELSEARCHRESPONSE VIEW ##################

class HotelSearchResponseView(ListCreateAPIView):
	serializer_class = HotelSearchResponseSerializer
	permission_classes = [permissions.IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save()

	def get_queryset(self):
		return HotelSearchResponse.objects.all()


class HotelSearchResponseDetailView(RetrieveUpdateDestroyAPIView):
	queryset = HotelSearchResponse.objects.all()
	serializer_class = HotelSearchResponseSerializer
	permission_classes = [permissions.IsAuthenticated,]
	lookup_field = "id"


##############   ROOMTYPE VIEW ##################

class RoomTypeView(ListCreateAPIView):
	serializer_class = RoomTypeSerializer
	permission_classes = [permissions.IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save()

	def get_queryset(self):
		return RoomType.objects.all()


class RoomTypeDetailView(RetrieveUpdateDestroyAPIView):
	queryset = RoomType.objects.all()
	serializer_class = RoomTypeSerializer
	permission_classes = [permissions.IsAuthenticated,]
	lookup_field = "id"


##############   TRAVELER VIEW ##################

class TravelerView(ListCreateAPIView):
	serializer_class = TravelerSerializer
	permission_classes = [permissions.IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save()

	def get_queryset(self):
		return Traveler.objects.all()


class TravelerDetailView(RetrieveUpdateDestroyAPIView):
	queryset = Traveler.objects.all()
	serializer_class = TravelerSerializer
	permission_classes = [permissions.IsAuthenticated,]
	lookup_field = "id"


##############   PAYMENTCARDPARAMETERS VIEW ##################

class PaymentCardParametersView(ListCreateAPIView):
	serializer_class = PaymentCardParametersSerializer
	permission_classes = [permissions.IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save()

	def get_queryset(self):
		return PaymentCardParameters.objects.all()


class PaymentCardParametersDetailView(RetrieveUpdateDestroyAPIView):
	queryset = PaymentCardParameters.objects.all()
	serializer_class = PaymentCardParametersSerializer
	permission_classes = [permissions.IsAuthenticated,]
	lookup_field = "id"



##############   REDIS IMPLEMENTATION VIEW ##################

# def rapidHotelAPIView(request):
# 	if 'content' in cache:
# 		context = cache.get('content') # REDIS CACHE CHECKING / GETTING
# 		return JsonResponse(context)
# 	else:
# 		url = "https://hotels4.p.rapidapi.com/properties/list"
# 		querystring = {"destinationId":"1506246","pageNumber":"1","checkIn":"2020-01-08","checkOut":"2020-01-15","pageSize":"25","adults1":"1","currency":"USD","locale":"en_US","sortOrder":"PRICE"}
			
# 		headers = {
# 			'x-rapidapi-key': "e4c5dd977dmsh036bed42bf4cecdp1d83bajsn111b272376e6",
# 			'x-rapidapi-host': "hotels4.p.rapidapi.com"
# 			}
# 		response = requests.request("GET", url, headers=headers, params=querystring)
# 		response = response.json()
# 		total = response['data']['body']['searchResults']['totalCount']
# 		data = response['data']['body']['searchResults']['results']
# 		data2 = []
# 		for info in data:
# 			content = {
# 				'id' : info['id'],
# 				'name' : info['name'],
# 				'starRating' : info['starRating'],
# 				'address' : info['address'],
# 				'landmarks' : info['landmarks'],
# 				'price' : info['ratePlan']['price'],
# 				'latitude' : info['coordinate']['lat'],
# 				'longitude' : info['coordinate']['lon'],
# 				}
# 			data2.append(content)

# 		context = {
# 			'totalCount' : total,
# 			'data' : data2

# 		}
# 		cache.set('content', context, timeout=CACHE_TTL) # REDIS CACHE SETTING
# 		return JsonResponse(context)



##############  CLASS view IMPLEMENTED BUT NOT WORKING GETTING SOME KEYERROR NEED TO FIX THAT ##################


class MyView(APIView):
	url = "https://hotels4.p.rapidapi.com/properties/list"
	url_city_search =  "https://hotels4.p.rapidapi.com/locations/search"
	headers = {
			'x-rapidapi-key': "e4c5dd977dmsh036bed42bf4cecdp1d83bajsn111b272376e6",
			'x-rapidapi-host': "hotels4.p.rapidapi.com"
			}

	def post(self, request, format=None):
		if request.method == 'POST':
			city_name = request.data.get('city_name')
			if city_name is not None:
				if city_name in cache:
					context = cache.get(city_name) # REDIS CACHE CHECKING / GETTING
					return Response(context)
				querystring = {"query":city_name,"locale":"en_US"}
				response = requests.request("GET", self.url_city_search, headers=self.headers, params=querystring)
				response = response.json()
				data = response['suggestions'][0]['entities']
				for info in data:
					if city_name.lower() == info['name'].lower():
						destinationId = info['destinationId']
						querystring1 = {"destinationId":destinationId,"pageNumber":"1","checkIn":"2020-01-08","checkOut":"2020-01-15","pageSize":"25","adults1":"1","currency":"USD","locale":"en_US","sortOrder":"PRICE"}
						response = requests.request("GET", self.url, headers=self.headers, params=querystring1)
						response = response.json()
						total = response['data']['body']['searchResults']['totalCount']
						data1 = response['data']['body']['searchResults']['results']
						data2 = []
						for i in data1:
							content = {
								'id' : i['id'],
								'name' : i['name'],
								'starRating' : i['starRating'],
								'address' : i['address'],
								'guestReviews': i['guestReviews'],
								'landmarks' : i['landmarks'],
								'price' : i['ratePlan']['price'],
								'latitude' : i['coordinate']['lat'],
								'longitude' : i['coordinate']['lon'],
								}
							data2.append(content)

						context = {
							'totalCount' : total,
							'data' : data2

						}
						cache.set('content', context, timeout=CACHE_TTL)
						return Response(context)




		else:
			return Response('enter proper details')
















##############  SIMPLE API TO DO MINIMUM PART OF ADAPTOR VIEW ##################



@api_view(['GET','POST'])
@authentication_classes([]) 	# DISABLING THE BEARER TOKEN AUTHENTICATION
@permission_classes([])			# DISABLING THE PERMISSION CLASSES ALSO
def rapidHotelAPIView(request):
	if request.method == 'POST':
		url = "https://hotels4.p.rapidapi.com/properties/list"						# INITIALIZING THE THIRD PARTY API FOR OBTAINING THE HOTEL LIST
		url_city_search =  "https://hotels4.p.rapidapi.com/locations/search"		# INITIALIZING THE THIRD PARTY API FOR OBTAINING THE DESTINATION ID BY SENDING THE LOCATION NAME OR CITY NAME
		headers = {
			'x-rapidapi-key': "e4c5dd977dmsh036bed42bf4cecdp1d83bajsn111b272376e6",
			'x-rapidapi-host': "hotels4.p.rapidapi.com"
			}
		city_name = request.data.get('city_name')			# GETTING THE CITY NAME FROM THE POST REQUEST THROUGH JSON LIKE {"city_name" : "new york"}
		if city_name is not None:
			if city_name in cache: 				#	CHECKING THE DATA IN CACHE
				context = cache.get(city_name) # REDIS CACHE CHECKING / GETTING
				return JsonResponse(context)
			querystring = {"query":city_name,"locale":"en_US"}			# SETTING THE QUERYSET AS PER THE THIRD PARTY API
			response = requests.request("GET", url_city_search, headers=headers, params=querystring)
			response = response.json()
			data = response['suggestions'][0]['entities'] 			# FILTERING THE DATA FOR PERFORMING ITERATION
			for info in data:
				if city_name.lower() == info['name'].lower():		#	CHECKING IN ORDER TO GET THE DESTINATION ID OF THE CITY FROM THE THIRD PARTY API
					destinationId = info['destinationId']
					querystring1 = {"destinationId":destinationId,"pageNumber":"1","checkIn":"2020-01-08","checkOut":"2020-01-15","pageSize":"25","adults1":"1","currency":"USD","locale":"en_US","sortOrder":"PRICE"}
					response = requests.request("GET", url, headers=headers, params=querystring1)
					response = response.json()
					total = response['data']['body']['searchResults']['totalCount']		#	SETTING THE DATA OF HOTEL LIST  FROM SEARCHING BY CITY NAME
					data1 = response['data']['body']['searchResults']['results']
					data2 = []
					for i in data1:
						content = {
								'id' : i['id'],
								'name' : i['name'],
								'starRating' : i['starRating'],				# SERIALIZING THE DATA AS SIMPLE FORMAT ALONG WITH FILTERING
								'address' : i['address'],
								'guestReviews': i['guestReviews'],
								'landmarks' : i['landmarks'],
								'price' : i['ratePlan']['price'],
								'latitude' : i['coordinate']['lat'],
								'longitude' : i['coordinate']['lon'],
								}
						data2.append(content)

					context = {
							'totalCount' : total,
							'data' : data2

						}
					cache.set(city_name, context, timeout=CACHE_TTL)		# SETTING THE DATA IN CACHE IN ORDER TO REDUCE THE RESPONSE TIME OF THAT PARTICULAR CITY OR OTHER SEARCH PARAMETERS
					return JsonResponse(context)




	else:
		context = {
			'errors' : 'enter proper details in POST request'
		}
		return JsonResponse(context)










