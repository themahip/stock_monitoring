# project/stocks/views/stock.py
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from stock.serializers.stock_serializer import StockSerializer, UserStockSerializer, StockDetailSerializer
from stock.models.userstock import Stock, UserStock
from stock.services.stock_service import StockService
from ramailo.builders.response_builder import ResponseBuilder
from shared.helpers.logging_helper import logger
from user.models.user import User

class StockListView(generics.ListAPIView):
    """View to list all available stocks"""
    serializer_class = StockSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Stocks retrieved successfully",
                schema=StockSerializer(many=True)
            ),
            400: openapi.Response(
                description="Bad request due to server error"
            ),
            403: openapi.Response(
                description="Forbidden - Authentication failed or insufficient permissions"
            ),
            404: openapi.Response(
                description="No stocks found"
            ),
            500: openapi.Response(
                description="Internal server error"
            )
        }
    )
    def get(self, request, *args, **kwargs):
        response_builder = ResponseBuilder()
        try:
            # Ensure stocks are initialized
            StockService.initialize_stocks()
            stocks = Stock.objects.all()
            serializer = self.get_serializer(stocks, many=True)
            stock_with_prices= StockService.get_all_stock_with_prices()
            logger.info(f"User {request.user.email} fetched stock list")
            return response_builder.result_object(stock_with_prices).success().ok_200().message("Stocks retrieved successfully").get_response()
        except Exception as e:
            """"""
            logger.error(f"Error fetching stock list for user {request.user.email}: {str(e)}")
            return response_builder.result_object({'error': str(e)}).fail().bad_request_400().message("Failed to retrieve stocks").get_response()

class UserStockListView(generics.ListCreateAPIView):
    """View to list or add user's selected stocks"""
    serializer_class = UserStockSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Require token authentication

    def get_queryset(self):
        user_id = getattr(self.request.user, 'user_id', None)
        if not user_id:
            logger.info(f"attempt to view stock without permission by {user_id}")
        user = User.objects.get(id= user_id)
        return UserStock.objects.filter(user=user)
    
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="User stocks retrieved successfully",
                schema=UserStockSerializer(many=True)
            ),
            400: openapi.Response(
                description="Bad request due to server error"
            ),
            403: openapi.Response(
                description="Forbidden - Authentication failed or insufficient permissions"
            ),
            404: openapi.Response(
                description="User or stocks not found"
            ),
            500: openapi.Response(
                description="Internal server error"
            )
        }
    )
    def get(self, request, *args, **kwargs):
        response_builder = ResponseBuilder()
        try:
            user_stocks = self.get_queryset()
            serializer = self.get_serializer(user_stocks, many=True)
            
            # Add current prices to response
            for item in serializer.data:
                price = StockService.get_or_fetch_stock_price(item['stock']['symbol'])
                item['current_price'] = price
            
            logger.info(f"User {request.user.email} fetched their stock list")
            return response_builder.result_object(serializer.data).success().ok_200().message("User stocks retrieved successfully").get_response()
        except Exception as e:
            logger.error(f"Error fetching user stocks for {request.user.email}: {str(e)}")
            return response_builder.result_object({'error': str(e)}).fail().bad_request_400().message("Failed to retrieve user stocks").get_response()

    @swagger_auto_schema(
        request_body=UserStockSerializer,
        responses={
            200: openapi.Response(
                description="Stock added successfully",
                schema=UserStockSerializer()
            ),
            400: openapi.Response(
                description="Bad request due to validation or server error"
            ),
            403: openapi.Response(
                description="Forbidden - Authentication failed or insufficient permissions"
            ),
            404: openapi.Response(
                description="User or stock not found"
            ),
            500: openapi.Response(
                description="Internal server error"
            )
        }
    )
    def post(self, request, *args, **kwargs):
        response_builder = ResponseBuilder()
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            logger.info(f"User stock creation failed for {request.user.email}: {serializer.errors}")
            error_message = ", ".join(["{}: {}".format(key, ", ".join(value)) for key, value in serializer.errors.items()])
            return response_builder.result_object(serializer.errors).fail().bad_request_400().message(error_message).get_response()

        try:
            # Add user to the validated data
            serializer.validated_data['user'] = request.user
            user_stock = serializer.save()
            logger.info(f"User {request.user.email} added stock {user_stock.stock.symbol}")
            return response_builder.result_object(serializer.data).success().ok_200().message("Stock added successfully").get_response()
        except Exception as e:

            logger.error(f"Error adding stock for user {request.user.email}: {str(e)}")
            return response_builder.result_object({'error': str(e)}).fail().bad_request_400().message("Failed to add stock").get_response()

class StockDetail(generics.CreateAPIView):
    """view the details of the stock"""
    serializer_class= StockDetailSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes= [IsAuthenticated]

    def get_object(self):
        symbol= self.kwargs['symbol'].upper()
        try:
            stock= Stock.objects.get(symbol= symbol)
        except Exception as e:
            logger.info(f"Stock with symbol {symbol} not found")
        user_id= self.request.user.id
        try: 
            user= User.objects.get(id= user_id)
        except Exception as e:
            logger.info(f"user with ID {user_id} not found")
        return stock, user

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Stock details retrieved successfully",
                schema=StockDetailSerializer()
            ),
            400: openapi.Response(
                description="Bad request due to server error"
            ),
            403: openapi.Response(
                description="Forbidden - Authentication failed or insufficient permissions"
            ),
            404: openapi.Response(
                description="Stock or user not found"
            ),
            500: openapi.Response(
                description="Internal server error"
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """to get the detail of the stock"""
        response_builder= ResponseBuilder()
        try:
            stock, user= self.get_object()
            serialzer= self.get_serializer(stock, context={'user':user})
            logger.info(f"User {user.id} fetched details for stock {stock.symbol}")
            return response_builder.result_object(serialzer.data).success().ok_200().message("here").get_response()
        except Exception as e:
            logger.error(f"Error fetching stock details for user {request.user.id}: {str(e)}")
            return response_builder.result_object({'error': str(e)}).fail().bad_request_400().message("Failed to retrieve stock details").get_response()
