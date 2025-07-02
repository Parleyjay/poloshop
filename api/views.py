from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User



from store.models import Product, Category, Customer, Cart, CartItem, ShippingAddress
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    CustomerSerializer,
    CartSerializer,
    ShippingAddressSerializer
)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        category_id = self.request.query_params.get('category')
        if category_id:
            return Product.objects.filter(category_id=category_id)
        return Product.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_superuser or (hasattr(user, 'customer') and user.customer.user_type == 'seller'):
            serializer.save(creator=user)
        else:
            raise PermissionError("Only sellers or admins can create products.")

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except PermissionError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            serializer.save(user=user)
        else:
            raise PermissionError("You must be logged in to create a customer.")


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(customer=self.request.user.customer)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def add_to_cart(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=404)

        customer = request.user.customer
        cart, _ = Cart.objects.get_or_create(customer=customer, complete=False)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity = cart_item.quantity + quantity if not created else quantity
        cart_item.save()

        return Response({'message': 'Item added to cart successfully.'})

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_from_cart(self, request):
        product_id = request.data.get('product_id')
        cart = Cart.objects.filter(customer=request.user.customer, complete=False).first()

        if not cart:
            return Response({'error': 'No active cart found'}, status=404)

        item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if item:
            item.delete()
            return Response({'message': 'Item removed'}, status=200)
        return Response({'error': 'Item not found in cart'}, status=404)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def increase_quantity(self, request):
        product_id = request.data.get('product_id')
        cart = Cart.objects.filter(customer=request.user.customer, complete=False).first()
        item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if item:
            item.quantity += 1
            item.save()
            return Response({'message': 'Quantity increased'}, status=200)
        return Response({'error': 'Item not found'}, status=404)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def checkout(self, request):
        cart = Cart.objects.filter(customer=request.user.customer, complete=False).first()
        if cart:
            cart.complete = True
            cart.save()
            return Response({'message': 'Checkout successful'}, status=200)
        return Response({'error': 'No active cart found'}, status=404)


class ShippingAddressViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ShippingAddress.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        cart_id = self.request.data.get('cart')
        serializer.save(customer=self.request.user, cart_id=cart_id)


# Auth API views

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    user_type = request.data.get('user_type', 'buyer')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)
    Customer.objects.create(user=user, email=email, name=username, user_type=user_type)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'message': 'User registered', 'token': token.key})


@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id, 'username': user.username})
    return Response({'error': 'Invalid credentials'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    user = request.user
    if user.is_authenticated:
        Token.objects.filter(user=user).delete()
        return Response({'message': 'Logged out successfully'})
    return Response({'error': 'Not logged in'}, status=400)
