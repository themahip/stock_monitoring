from rest_framework import serializers
from rest_framework.serializers import ValidationError

from ramailo.models.feedback import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"

    def validate(self, attrs):
        if attrs['type'] == dict(Feedback.TYPE_CHOICES)["Others"] and not attrs.get("message"):
            raise ValidationError({"message": "Message is required for type others!"})
        return attrs


class RaiseTicketSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    issue_type = serializers.CharField()
    description = serializers.CharField(max_length=200)
