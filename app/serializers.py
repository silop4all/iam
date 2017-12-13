from rest_framework import serializers
from app.models import *


class SubProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('mail', 'username',)


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

class ClientProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        exclude = ('id', 'activation', 'logo',)

class ProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        exclude = ('username',)

class RegistrationRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegistrationRequest
        fields = ('mail', 'uuid',)


class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        #fields = '__all__'
        exclude = ('client_access_token', )

class ApplicationUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        exclude = ('client_id','client_access_token', )

class ApplicationLimitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = ('client_id', 'name',)


class ApplicationOwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationOwner
        fields = '__all__'
        depth=1


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'

class RoleLimitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ('type', )


class ApplicationRoleSerializer(serializers.ModelSerializer):
    application = ApplicationLimitSerializer(read_only=True)
    role        = RoleLimitSerializer(read_only=True)
    
    class Meta:
        model = ApplicationRole
        fields = ('application', 'role',  )


class ApplicationMemberHasRoleSerializer(serializers.ModelSerializer):
    application_role = ApplicationRoleSerializer(read_only=True)

    class Meta:
        model = ApplicationMemberHasRole
        fields = ('application_role', )


class ApplicationMembershipSerializer(serializers.ModelSerializer):
    member_roles = ApplicationMemberHasRoleSerializer(many=True)
    
    class Meta:
        model = ApplicationMembership
        fields = ('member_roles', )





class UserProfileSerializer(serializers.Serializer):

    name        = serializers.CharField(min_length=2, max_length=127)
    surname     = serializers.CharField(min_length=2, max_length=127)
    gender      = serializers.CharField(max_length=1, allow_null=False)
    username    = serializers.CharField(min_length=4, max_length=255)
    userpassword = serializers.CharField(min_length=8, max_length=255)
    country     = serializers.CharField(max_length=255, required=True, allow_null=False)
    city        = serializers.CharField(max_length=255, required=False, allow_null=True)
    address     = serializers.CharField(max_length=255, required=False, allow_null=True)
    postcode    = serializers.CharField(max_length=20, required=False, allow_null=True)
    mail        = serializers.EmailField(max_length=255)
    phone       = serializers.CharField(min_length=10, max_length=20, required=True)
    skills      = serializers.CharField(max_length=10)
    #vat         = serializers.CharField(min_length=6, max_length=30, required=False, allow_null=True)
    crowd_fund_participation    = serializers.BooleanField(required=True)
    crowd_fund_notification     = serializers.BooleanField(required=True)

    def validate(self, attrs):

        # Check that the user password consists of at least 8 chars
        if Profile.objects.filter(username=attrs['username']).count():
            raise serializers.ValidationError("This username value has already taken")

        # Check that the user password consists of at least 8 chars
        if Profile.objects.filter(mail=attrs['mail']).count():
            raise serializers.ValidationError("This mail value has already taken")

        # Check that the user password consists of at least 8 chars
        if len(attrs['userpassword']) < 8 :
            raise serializers.ValidationError("userpassword field: at least 8 characters are required")

        # Check that the gender value belongs to a set of specific ones
        if attrs['gender'] not in ['M', 'W']:
            raise serializers.ValidationError("Ensure that gender field has value M for male or W for female")

        # Check that the skills value belongs to a set of specific ones
        if attrs['skills'] not in ['low', 'normal', 'high']:
            raise serializers.ValidationError("Ensure that the skills field has one of the values low, normal or high")

        # Check that the phone number is numeric
        try:
            int( attrs['phone'])
        except ValueError:
            raise serializers.ValidationError("Ensure that the phone number consists of digits")

        #if 'vat' in attrs and attrs['vat'] in [None, ""]:
        #    raise serializers.ValidationError("Ensure that the vat number consists of at least 6 digits")

        return attrs