from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.generics import CreateAPIView ,RetrieveAPIView 
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q
from .models import User
from .serializers import UserSerializer
import random
import string
import io
import jwt
from django.contrib.auth.hashers import make_password
from pamps_ga_admin_api.settings import SECRET_KEY


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistration(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            pythonData = JSONParser().parse(io.BytesIO(request.body))
            
            # Extracting the necessary fields
            profileImage = pythonData.get('profileImage', None)
            fullName = pythonData.get('fullName', None)
            email = pythonData.get('email', None)
            phoneNumberCountryCode = pythonData.get("phoneNumberCountryCode", None)
            mobileNo = pythonData.get('mobileNo', None)
            deviceType = pythonData.get('deviceType', None)
            deviceToken = pythonData.get('deviceToken', None)
            userType = pythonData.get("userType", 1)
            gender = pythonData.get("gender", None)
            tnc = pythonData.get('tnc', None)
            password = pythonData.get("password", False)


            if not fullName or not mobileNo:
                response = {
                    "error": {
                        "errorCode": 502,
                        "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "errorMessage": "Some Required Field is missing"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            if email and User.objects.filter(Q(email=email, userType=userType)).exists():
                response = {
                    "error": {
                        "errorCode": 502,
                        "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "errorMessage": "This Email already exists"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            if mobileNo and User.objects.filter(Q(mobileNo=mobileNo, userType=userType)).exists():
                response = {
                    "error": {
                        "errorCode": 502,
                        "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "errorMessage": "This Mobile No. already exists"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            if deviceType not in [1, 2, 3]:
                response = {
                    "error": {
                        "errorCode": 504,
                        "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "errorMessage": "Invalid deviceType"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


            serializer = self.serializer_class(data=pythonData)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

                user = User.objects.filter(mobileNo=mobileNo, userType=userType).first()
              
                response = {
                    "error": None,
                    "response": {
                        "data": {
                            'userId': user.id,
                            'fullName': user.fullName,
                            'mobileNo': user.mobileNo,
                            'email': user.email,
                            'deviceType': user.deviceType,
                            'gender': user.gender,
                            'profileImage': user.profileImage,
                            "createdAt": user.createdAt.date(),
                            'token': get_tokens_for_user(user)
                        },
                        "message": {
                            'success': True,
                            "successCode": 201,
                            "statusCode": status.HTTP_201_CREATED,
                            "successMessage": "Registration Successful, You have successfully registered to Rapicue."
                        }
                    }
                }
                return Response(response, status=status.HTTP_201_CREATED)

            response = {
                "error": {
                    "errorCode": 510,
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errorMessage": "Failed to register user"
                },
                "response": None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "error": {
                    "errorCode": 522,
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errorMessage": str(e)
                },
                "response": None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


        
class UserLogin(RetrieveAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            pythonData = JSONParser().parse(io.BytesIO(request.body))
            mobileNo = pythonData.get('mobileNo', None)
            email = pythonData.get('email', None)
            deviceType = pythonData.get('deviceType', False)
            deviceToken = pythonData.get('deviceToken', False)
            password = pythonData.get('password', False)
            
                
            if not deviceType:
                response = {
                    "error": {
                        "errorCode": 503,
                        "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "errorMessage": "device type is required to login"
                    },
                    "response": None
                }
                return Response(response, status.HTTP_422_UNPROCESSABLE_ENTITY)
            
            if not password:
                response = {
                    "error": {
                        "errorCode": 504,
                        "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "errorMessage": "password field is required to login"
                    },
                    "response": None
                }
                return Response(response, status.HTTP_422_UNPROCESSABLE_ENTITY)
            if email is None:
                user = User.objects.filter(Q(mobileNo=mobileNo)).first()
            else:
                user = User.objects.filter(Q(email=email)).first()
                
            if user is None:
                response = {
                    "error": {
                        "errorCode": 505,
                        "statusCode": status.HTTP_404_NOT_FOUND,
                        "errorMessage": "User Not Found"
                    }
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            if not user.check_password(password):
                response = {
                    "error": {
                        "errorCode": 506,
                        "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "errorMessage": "Please enter your correct password"
                    },
                    "response": None
                }
                return Response(response, status.HTTP_422_UNPROCESSABLE_ENTITY)
            if user.isActive == 0:
                response = {
                    "error": {
                        "errorCode": 507,
                        "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "errorMessage": "Your Account is blocked by administration. For more information please contact to Admin."
                    },
                    "response": None
                }
                return Response(response, status.HTTP_422_UNPROCESSABLE_ENTITY)
          
  
            if deviceToken:
                
                
                User.objects.filter(id=user.id).update(
                    deviceToken=deviceToken)

            User.objects.filter(id=user.id).update(
                deviceType=deviceType)
            
            
            data = {
                'userId': user.id,
                'fullName': user.fullName,
                'mobileNo': user.mobileNo,
                'email': user.email,
                'deviceType': user.deviceType,
                'gender': user.gender,
                'profileImage': user.profileImage,
                "createdAt": user.createdAt.date(),
                'token': get_tokens_for_user(user)
        
            }
            response = {
                "error": None,
                "response": {
                    "data": data,
                    "message": {
                        'success': True,
                        "successCode": 102,
                        "statusCode": status.HTTP_200_OK,
                        "successMessage": "Logged in successfully."
                    }
                }
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "error": {
                    "errorCode": 522,
                    "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "errorMessage": str(e)
                },
                "response": None
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
 

        
class UserLogout(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
        
            pythonData = JSONParser().parse(io.BytesIO(request.body))
            refreshToken = pythonData.get('refresh', False)
            
            if not refreshToken:
                response = {
                    "error": {
                        "errorCode": 501,
                        "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "errorMessage": "Token is required to logout!"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            # if not userType:
            #     response = {
            #         "error": {
            #             "errorCode": 501,
            #             "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
            #             "errorMessage": "user type is required to logout!"
            #         },
            #         "response": None
            #     }
            #     return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            

            user = jwt.decode(refreshToken, key=SECRET_KEY,
                              algorithms=['HS256', ])
            
            
            userr = User.objects.filter(
                Q(id=user['user_id'])).first()
            
            
            if userr is None:
                response = {
                    "error": {
                        "errorCode": 501,
                        "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "errorMessage": "User not found invalid access token!"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
            RefreshToken(refreshToken).blacklist()
            
            
            userr.deviceToken = None
            userr.save()
            response = {
                "error": None,
                "response": {
                    "message": {
                        'success': True,
                        "successCode": 102,
                        "statusCode": status.HTTP_200_OK,
                        "successMessage": "Logout successfully."
                    }
                }
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as exception:
            response = {
                "error": {
                    "errorCode": 511,
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errorMessage": str(exception)
                },
                "response": None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
   


