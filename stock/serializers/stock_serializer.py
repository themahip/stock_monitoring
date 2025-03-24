from rest_framework import serializers

from stock.models.stock import Stock
from stock.models.userstock import UserStock
from stock.services.stock_service import StockService
from shared.helpers.logging_helper import logger
from user.models.user import User

class StockSerializer(serializers.ModelSerializer):
    """Serializer for Stock model"""
    current_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Stock
        fields = ['id', 'symbol', 'name', 'created_at', 'current_price']

    def get_current_price(self, obj):
        """Get current price from StockService"""
        try:
            price = StockService.get_or_fetch_stock_price(obj.symbol)
            return price
        except Exception as e:
            logger.error(f"Error fetching price for {obj.symbol}: {str(e)}")
            return None

class UserStockSerializer(serializers.ModelSerializer):
    """Serializer for UserStock model"""
    stock = StockSerializer(read_only=True)
    stock_id = serializers.PrimaryKeyRelatedField(
        queryset=Stock.objects.all(),
        source='stock',
        write_only=True,
        help_text="ID of the stock to monitor"
    )
    current_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserStock
        fields = ['id', 'stock', 'stock_id', 'upper_limit', 'lower_limit', 'created_at', 'current_price']
        extra_kwargs = {
            'upper_limit': {'required': False, 'allow_null': True},
            'lower_limit': {'required': False, 'allow_null': True}
        }

    def validate(self, attrs):
        token_user = self.context['request'].user
        if not token_user.is_authenticated:
            raise serializers.ValidationError({"auth": "User not authenticated"})
        username = getattr(token_user, 'username', None)
        if not username:
            raise serializers.ValidationError({"auth": "Username not in token"})
        user = User.objects.get(username=username)  # Fetch user manually
        stock = attrs.get('stock')
        if UserStock.objects.filter(user=user, stock=stock).exists():
            raise serializers.ValidationError({
            'stock_id': 'This stock is already selected by the user'
            })
        attrs['user'] = user  # Add user to validated data
        return attrs
        
        # Ensure stock exists (handled by stock_id field, but adding explicit check)
        stock = attrs.get('stock')
        if not Stock.objects.filter(id=stock.id).exists():
            raise serializers.ValidationError({
                'stock_id': 'Invalid stock ID'
            })
        
        # Check if user already has this stock
        user = self.context['request'].user
        if UserStock.objects.filter(user=user, stock=stock).exists():
            raise serializers.ValidationError({
                'stock_id': 'This stock is already selected by the user'
            })
        
        return attrs

    def get_current_price(self, obj):
        """Get current price from StockService"""
        try:
            price = StockService.get_or_fetch_stock_price(obj.stock.symbol)
            return price
        except Exception as e:
            logger.error(f"Error fetching price for {obj.stock.symbol}: {str(e)}")
            return None

    def create(self, validated_data):
        """Create a new UserStock instance"""
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)