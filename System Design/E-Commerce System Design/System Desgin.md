# E-commerce System Design

## Overview

This document outlines the system design for a small yet effective e-commerce website similar to Amazon. The system supports users (customers), sellers, and admins, providing functionalities for product management, order processing, payment, and shipping.

## Table of Contents

1. [Functional Requirements](#functional-requirements)
2. [Non-Functional Requirements](#non-functional-requirements)
3. [Architecture Overview](#architecture-overview)
4. [Database Schema](#database-schema)
5. [API Endpoints](#api-endpoints)
6. [Authentication and Authorization](#authentication-and-authorization)
7. [Admin Dashboard](#admin-dashboard)
8. [Deployment](#deployment)


## Functional Requirements

1. **User Management:**
   - User registration and login.
   - Seller registration and login.
   - Admin management.
   
2. **Product Management:**
   - Sellers can add, update, and delete products.
   - Products can have variations (size, color).

3. **Order Management:**
   - Users can create and manage orders.
   - Order processing and status tracking.

4. **Payment and Shipping:**
   - Payment processing.
   - Shipping information management.
   - Order shipping status tracking.

5. **Notifications:**
   - Users receive notifications about order status and other relevant information.

## Non-Functional Requirements

1. **Scalability:** 
   - The system should handle increasing numbers of users and orders.
   
2. **Performance:** 
   - Fast response times for user interactions.
   
3. **Security:** 
   - Secure user authentication and authorization.
   - Data encryption for sensitive information.

4. **Maintainability:** 
   - Clear code structure and documentation.

## Architecture Overview

The system follows a typical 3-tier architecture:

1. **Presentation Layer:** 
   - Frontend (React.js, Svelte.js, or any other frontend framework).

2. **Application Layer:** 
   - Backend (Django REST Framework).

3. **Data Layer:** 
   - Database (PostgreSQL).

### Models

1. **User**
   ```python
   class User(AbstractUser):
       full_name = models.CharField(max_length=255)
       address = models.TextField()
       phone_number = models.CharField(max_length=20)
   ```

2. **Seller**
   ```python
   class Seller(User):
       business_address = models.TextField()
       tax_id = models.CharField(max_length=50)
   ```

3. **Product**
   ```python
   class Product(models.Model):
       name = models.CharField(max_length=255)
       description = models.TextField()
       price = models.DecimalField(max_digits=10, decimal_places=2)
       seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
       created_at = models.DateTimeField(auto_now_add=True)
   ```

4. **ProductVariation**
   ```python
   class ProductVariation(models.Model):
       product = models.ForeignKey(Product, on_delete=models.CASCADE)
       variation_name = models.CharField(max_length=255)
       variation_value = models.CharField(max_length=255)
   ```

5. **Order**
   ```python
   class Order(models.Model):
       user = models.ForeignKey(User, on_delete=models.CASCADE)
       total_amount = models.DecimalField(max_digits=10, decimal_places=2)
       status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES)
       created_at = models.DateTimeField(auto_now_add=True)
   ```

6. **OrderItem**
   ```python
   class OrderItem(models.Model):
       order = models.ForeignKey(Order, on_delete=models.CASCADE)
       product = models.ForeignKey(Product, on_delete=models.CASCADE)
       quantity = models.PositiveIntegerField()
       price = models.DecimalField(max_digits=10, decimal_places=2)
   ```

7. **Payment**
   ```python
   class Payment(models.Model):
       order = models.ForeignKey(Order, on_delete=models.CASCADE)
       amount = models.DecimalField(max_digits=10, decimal_places=2)
       method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
       status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES)
       transaction_id = models.CharField(max_length=255)
       created_at = models.DateTimeField(auto_now_add=True)
   ```

8. **Shipping**
   ```python
   class Shipping(models.Model):
       order = models.ForeignKey(Order, on_delete=models.CASCADE)
       address = models.TextField()
       status = models.CharField(max_length=20, choices=SHIPPING_STATUS_CHOICES)
       tracking_number = models.CharField(max_length=255)
       created_at = models.DateTimeField(auto_now_add=True)
   ```

9. **Notification**
   ```python
   class Notification(models.Model):
       user = models.ForeignKey(User, on_delete=models.CASCADE)
       message = models.TextField()
       is_read = models.BooleanField(default=False)
       created_at = models.DateTimeField(auto_now_add=True)
   ```

## API Endpoints

### User Endpoints

1. **Register User:**
   - `POST /register/user/`
   - Request Body: `{ "username": "john", "password": "password123", "email": "john@example.com", "full_name": "John Doe" }`

2. **Register Seller:**
   - `POST /register/seller/`
   - Request Body: `{ "username": "seller1", "password": "password123", "email": "seller@example.com", "full_name": "Seller One", "business_address": "123 Business St.", "tax_id": "TAX12345" }`

3. **Login:**
   - `POST /login/`
   - Request Body: `{ "username": "john", "password": "password123" }`

4. **Logout:**
   - `POST /logout/`

### Product Endpoints

1. **List Products:**
   - `GET /products/`

2. **Create Product:**
   - `POST /products/`
   - Request Body: `{ "name": "Product 1", "description": "Description of Product 1", "price": "10.00", "seller": 1 }`

3. **Retrieve Product:**
   - `GET /products/{id}/`

4. **Update Product:**
   - `PUT /products/{id}/`
   - Request Body: `{ "name": "Updated Product", "description": "Updated description", "price": "12.00" }`

5. **Delete Product:**
   - `DELETE /products/{id}/`

### Order Endpoints

1. **List Orders:**
   - `GET /orders/`

2. **Create Order:**
   - `POST /orders/`
   - Request Body: `{ "user": 1, "total_amount": "100.00", "status": "Pending" }`

3. **Retrieve Order:**
   - `GET /orders/{id}/`

4. **Update Order:**
   - `PUT /orders/{id}/`
   - Request Body: `{ "status": "Shipped" }`

5. **Delete Order:**
   - `DELETE /orders/{id}/`

### Payment Endpoints

1. **List Payments:**
   - `GET /payment/`

2. **Create Payment:**
   - `POST /payment/`
   - Request Body: `{ "order": 1, "amount": "100.00", "method": "Credit Card", "status": "Completed", "transaction_id": "TX12345" }`

### Shipping Endpoints

1. **List Shipping:**
   - `GET /shipping/`

2. **Create Shipping:**
   - `POST /shipping/`
   - Request Body: `{ "order": 1, "address": "123 Shipping St.", "status": "Shipped", "tracking_number": "TRACK12345" }`

### Notification Endpoints

1. **List Notifications:**
   - `GET /notifications/`

2. **Create Notification:**
   - `POST /notifications/`
   - Request Body: `{ "user": 1, "message": "Your order has been shipped." }`

## Authentication and Authorization

- **Session-Based Authentication:** Used for user authentication.
- **Permissions:**
  - Only authenticated users can create or manage products and orders.
  - Admin users have full access to manage all entities.
  - Sellers can manage their products and view their orders.

### Implementing Session-Based Authentication in Django

1. **Update `settings.py`:**

   ```python
   INSTALLED_APPS = [
       ...,
       'django.contrib.sessions',
       'rest_framework',
       'rest_framework.authtoken',
       'djoser',
       ...
   ]

   MIDDLEWARE = [
       ...,
       'django.contrib.sessions.middleware.SessionMiddleware',
       'django.middleware.common.CommonMiddleware',
       ...
   ]

   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework.authentication.SessionAuthentication',
       ],
   }

   AUTHENTICATION_BACKENDS = (
       'django.contrib.auth.backends.ModelBackend',
   )
   ```

2. **Update `urls.py`:**

   ```python
   from django.urls import path, include
   from rest_framework.authtoken.views import obtain_auth_token

   urlpatterns = [
       path('api-auth/', include('rest_framework.urls')),
       path('api/', include('djoser.urls')),
   ]
   ```

3. **Views for login and logout:**

```python
   from django.contrib.auth import login, logout
   from rest_framework.decorators import api_view, permission_classes
   from rest_framework.permissions import AllowAny
   from rest_framework.response import Response

   @api_view(['POST'])
   @permission_classes([AllowAny])
   def user_login(request):
       username = request.data.get('username')
       password = request.data.get('password')
       user = authenticate(username=username, password=password)
       if user is not None:
           login(request, user)
           return Response({'message': 'Login successful.'})
       else:
           return Response({'error': 'Invalid credentials.'}, status=400)

   @api_view(['POST'])
   def user_logout(request):
       logout(request)
       return Response({'message': 'Logout successful.'})
   ```

4. **URL Patterns:**

   ```python
   urlpatterns += [
       path('login/', user_login),
       path('logout/', user_logout),
   ]
   ```

## Admin Dashboard

The admin dashboard allows admins to manage users, products, orders, payments, shipping, and notifications.

- **User Management:** List, create, update, and delete users.
- **Product Management:** List, create, update, and delete products.
- **Order Management:** List, update, and delete orders.
- **Payment Management:** List and create payments.
- **Shipping Management:** List and create shipping information.
- **Notification Management:** List and create notifications.

## ~~Deployment~~

### ~~Development Environment~~

1. ~~**Install Dependencies:**~~
   ```bash
   pip install -r requirements.txt
   ```

2. ~~**Run Migrations:**~~
   ```bash
   python manage.py migrate
   ```

3. ~~**Create Superuser:**~~
   ```bash
   python manage.py createsuperuser
   ```

4. ~~**Run Server:**~~
   ```bash
   python manage.py runserver
   ```

### ~~Production Environment~~

1. ~~**Set up Database~~

~~:**~~
   - ~~Use PostgreSQL.~~

2. ~~**Configure Web Server:**~~
   - ~~Use Nginx as the reverse proxy.~~
   - ~~Use Gunicorn to serve the Django application.~~

3. ~~**Deploy using Docker:**~~
   - ~~Use Docker Compose to set up the services.~~

```yaml
version: '3'

services:
  db:
    image: postgres
    environment:
      POSTGRES_DB: ecommerce
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    depends_on:
      - db

  nginx:
    image: nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web

volumes:
  postgres_data:
```

## ~~Conclusion~~

~~This document provides a detailed overview of the system design for a small yet effective e-commerce website. It includes functional and non-functional requirements, architecture, database schema, API endpoints, authentication and authorization details, admin dashboard, and deployment instructions.~~
