from rest_framework import serializers

from ramailo.models.user import User


class FCMSerializer(serializers.Serializer):
    fcm_token = serializers.CharField(max_length=350)


class OnboardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mobile', 'device_signature', 'referrer_id', 'force_new_device', 'device_details']

    mobile = serializers.CharField(min_length=10, max_length=10)
    device_signature = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    referrer_id = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    force_new_device = serializers.BooleanField(default=False)
    device_details = serializers.JSONField(default={})


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["mobile", "otp"]

    mobile = serializers.CharField(min_length=10, max_length=10)
    otp = serializers.CharField(min_length=6, max_length=6)


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()

    def to_representation(self, instance):
        return {
            'access': str(instance.access_token),
            'refresh': str(instance),
        }
        
