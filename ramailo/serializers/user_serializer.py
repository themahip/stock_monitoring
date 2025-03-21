from django.core.validators import MinLengthValidator, RegexValidator
from rest_framework import serializers

from ramailo.models.user import Kyc, ProfileImage, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['idx', 'mobile']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['idx', 'name', 'age', 'dob', 'validated_on',
                  'image', 'total_rewards', 'mobile', 'is_new_user', 'pin_code']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'age', 'pin_code', "image"]

    image = serializers.FileField(required=False)
    name = serializers.CharField(validators=[MinLengthValidator(3)])
    age = serializers.IntegerField(min_value=10, max_value=100)
    pin_code = serializers.CharField(validators=[RegexValidator(
        regex="^[1-9]{1}[0-9]{2}[0-9]{3}$",
        message='Invalid Pin code.')
    ])

    def update(self, obj, data):
        image = data.pop("image", None)
        if image:
            ProfileImage.objects.create(user=obj, image=image)
        User.objects.filter(id=obj.id).update(**data)
        return obj


class KycSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kyc
        fields = ["dob", "file"]
        read_only_fields = ['name']


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EmailValidationSerializer(EmailSerializer):
    otp = serializers.IntegerField(min_value=100000, max_value=999999)
