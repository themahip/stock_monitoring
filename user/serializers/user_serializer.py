from rest_framework import serializers

from user.models.user import User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email', 'name', 'password']
    email= serializers.EmailField()
    username=serializers.CharField(required=True)
    name=serializers.CharField(required=True)
    password= serializers.CharField(min_length=6)


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="User's password"
    )
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError({
                'email': 'Email and password are required' if not email else None,
                'password': 'Email and password are required' if not password else None
            })

        return attrs
    

class TokenSerializer(serializers.Serializer):
    class Meta:
        model=User
        fields=['username', 'email', 'name', 'password']