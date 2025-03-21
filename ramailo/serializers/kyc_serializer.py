from rest_framework import serializers


class KycSerializer(serializers.Serializer):
    email = serializers.EmailField()
