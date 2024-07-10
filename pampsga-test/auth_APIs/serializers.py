from rest_framework import serializers
from .models import User  # Adjust the import as per your project structure

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'fullName', 'email', 'mobileNo', 'gender', 'deviceType', 
            'deviceToken', 'profileImage', 'tnc', 'authServiceProviderId', 
            'authServiceProviderType', 'userType', 'referralCode', 
            'invitedCode', 'phoneNumberCountryCode', 'password'
        ]
    
    def create(self, validated_data):
        gender = validated_data.get('gender', None)
        deviceToken = validated_data.get('deviceToken', None)
        email = validated_data.get('email', None)
        profileImage = validated_data.get('profileImage', None)
        authServiceProviderId = validated_data.get('authServiceProviderId', None)
        authServiceProviderType = validated_data.get('authServiceProviderType', None)
        referralCode = validated_data.get('referralCode', None)
        invitedCode = validated_data.get('invitedCode', None)

        user = User.objects.create(
            fullName=validated_data['fullName'],
            email=email,
            mobileNo=validated_data['mobileNo'],
            profileImage=profileImage,
            deviceToken=deviceToken,
            deviceType=validated_data['deviceType'],
            gender=gender,
            tnc=validated_data['tnc'],
            authServiceProviderId=authServiceProviderId,
            authServiceProviderType=authServiceProviderType,
            referralCode=referralCode,
            invitedCode=invitedCode,
            phoneNumberCountryCode=validated_data['phoneNumberCountryCode']
        )

        # Use set_password to hash the password before saving
        user.set_password(validated_data['password'])
        user.save()

        return user
