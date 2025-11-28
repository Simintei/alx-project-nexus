# ALX Backend Program – Overview

This README provides a learner's summary of key concepts, technologies, and experiences gained throughout the past few weeks in the ALX Backend program. It highlights major learnings in Python, databases, frameworks, DevOps tooling, and backend engineering best practices.

---

## 🚀 Key Technologies Covered

### **1. Python (Advanced)**

* Deepened understanding of advanced Python concepts.
* Working with decorators, context managers, iterators, and generators.
* Writing cleaner, modular, maintainable code.
* Improved debugging and testing workflows.

### **2. Django Framework**

* Implementing models, views, and URL routing.
* Using Django ORM for database operations.
* Creating RESTful endpoints.
* Using Django signals, caching, and middleware.

### **3. REST APIs**

* Building and structuring scalable API endpoints.
* Serializers, request/response patterns.
* Versioning, documentation, and authentication considerations.

### **4. GraphQL**

* Understanding schema, queries, and mutations.
* Integrating Graphene with Django.
* Implementing advanced features such as filtering and pagination.

### **5. SQL (Advanced)**

* Joins, subqueries, window functions.
* Stored procedures, triggers, and indexing.
* Query optimization and performance analysis.
* Using SQLite, MySQL, and PostgreSQL in different environments.

### **6. Docker & Containerization**

* Writing Dockerfiles and using multi-stage builds.
* Docker Compose for multi‑service setups.
* Persisting data using Docker volumes.
* Deploying reproducible environments.

### **7. CI/CD Workflows**

* Understanding continuous integration pipelines.
* Running automated tests in CI.
* Preparing backend apps for deployment.

### 🌐 **Container Orchestration with Kubernetes**

Understanding Pods, Deployments, and Services.

Managing container scaling, rolling updates, and self-healing.

Working with YAML configuration files.

Deploying Django and API services to Kubernetes clusters.


### 🖥️ **Advanced Shell Scripting**

Building automation scripts for deployment and monitoring.

Using loops, conditionals, and functions in Bash.

Log management and cleanup scripts.

Enhancing productivity with reusable shell utilities.


### 💳 **Payment Integration – Chapa API**

Integrating secure payment workflows.

Handling callbacks, signatures, and transaction verification.

Creating reusable payment service modules.

Testing payment flows and webhook events.


### 🔧 **Jenkins & GitHub Actions (CI/CD)**

Building pipelines for automated testing and deployment.

Webhooks, pipeline triggers, and artifact management.

Running migrations, tests, and lint checks automatically.

Workflow files for multi-step deployment processes.


### ⏱️ **Scheduling Automations – Crontab & Advanced Scheduling**

Writing cron expressions.

Scheduling periodic tasks (cleanup, emails, reports).

Integrating crontab with Django & Celery.

Error handling and logging for automated jobs.


### 🔐 **Security & Analytics – IP Tracking**

Implementing middleware for IP logging.

Rate limiting and blocking suspicious users.

Using geolocation APIs for analytics.

Storing and analyzing request patterns.


### 🗄️ Database Setup & Configuration

* Setting up MySQL/PostgreSQL locally and in Docker.
* Managing schema migrations with Django.
* Using admin tools (dbshell, Prisma-like tools, GUI clients).
* Ensuring proper indexing, normalization, and relationships.
* Environment-based configurations: dev, staging, production.

---

## ⚙️ Important Backend Development Concepts

### **1. Database Design**

* Designing ER diagrams and relational models.
* Understanding one-to-one, one-to-many, and many-to-many relations.
* Data normalization vs. denormalization.
* Real‑world schema modification and migration handling.

### **2. Asynchronous Programming**

* Using async/await in Python.
* Task scheduling with Celery and crontab.
* Performing background tasks (emails, cleanup, ETL jobs).

### **3. Caching Strategies**

* Implementing Django caching with Redis.
* Low-level caching: keys, invalidation strategies, hit ratios.
* View-level & template caching.
* Evaluating caching effectiveness.

---

## 🧪 Testing

* Writing unit tests for views, models, and utilities.
* Using Django's `TestCase` and pytest setups.
* Mocking external services.
* Ensuring high test coverage.
* Integrating tests into CI pipelines.

---

## 💡 Challenges Faced & Solutions Implemented

* **Broken migrations** – resolved by resetting DB or applying fake migrations.
* **Docker networking issues** – fixed by mapping correct ports and services.
* **Merge conflicts** – learned GitFlow and conflict resolution techniques.
* **API bugs** – debugged using Django Debug Toolbar and better logging.
* **Caching errors** – solved by reviewing Redis keys and invalidation logic.
* **GraphQL schema confusion** – overcame by building schemas incrementally.

---

## 📝 Best Practices & Personal Takeaways

* Always write modular, readable code.
* Use virtual environments and Docker for consistent environments.
* Commit early, commit often.
* Document APIs properly (README, docstrings, schema docs).
* Write tests before deployments.
* Use caching wisely but carefully.
* Keep database schema clean and optimized.
* Always review pull requests thoroughly.

---

## ✔️ Final Thoughts

This program has strengthened backend engineering skills through hands‑on work with real technologies used in production. The integration of Python, Django, Docker, SQL, and GraphQL has provided a solid foundation for building scalable and maintainable backend systems.

---

# Bookstore API

A Django REST Framework (DRF) project for managing books, authors, and categories. Includes Swagger/OpenAPI documentation, nested serializers, and structured endpoints.

## Features

* CRUD for **Books**, **Authors**, and **Categories**
     Create, read, update, and delete operations for products and categories.
     User authentication and management features using JWT. 
* API Features
     Filtering and Sorting: Allow users to filter products by category and sort by price.
     Pagination: Implement paginated responses for large product datasets.
* Nested serializers with writable foreign keys
* Swagger UI & Redoc API documentation
* Fully RESTful URL structure

## Requirements

* Python 3.10+
* Django 4+
* Django REST Framework
* drf-yasg (for Swagger)

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Project Structure

```
alx-project-nexus/
    bookstore/ <------------main project
        settings.py
        urls.py  
    books/ <----------apps
        models.py
        serializers.py
        views.py
        urls.py
    users/ <----------apps
        models.py
        serializers.py
        views.py
        urls.py
    orders/ <----------apps
        models.py
        serializers.py
        views.py
        urls.py
    manage.py
    README.MD
    seed.py
    requirements.txt
```

## Models

### Category

```python
class Category(models.Model):
    name = models.CharField(max_length=100)
```

### Author

```python
class Author(models.Model):
    name = models.CharField(max_length=100)
```

### Book

```python
class Book(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
```

## Serializers

### BookSerializer (nested + writable foreign keys)

```python
from rest_framework import serializers
from .models import Book, Category, Author


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name"


class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source="category", write_only=True)

    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), source="author", write_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "author", "author_id", "category", "category_id", "price"]
```

## Views

### DRF ModelViewSets

```python
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

## URLs

### books/urls.py

```python
router = DefaultRouter()
router.register(r"books", BookViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"authors", AuthorViewSet)

urlpatterns = [path("", include(router.urls))]
```

### users/urls.py

```python
from django.urls import path
from .views import RegisterView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
```

### orders/urls.py

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, OrderViewSet, CheckoutView

router = DefaultRouter()

# CartViewSet handles:
#   GET /cart/         → list cart items
#   POST /cart/        → add to cart
#   DELETE /cart/{id}/ → remove from cart
router.register(r'cart', CartViewSet, basename='cart')

# List user orders
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),

    # Checkout endpoint
    path('checkout/', CheckoutView.as_view({'post': 'create'}), name='checkout'),
]
```

### bookstore/urls.py

```python
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Bookstore API",
        default_version="v1",
        description="API for bookstore backend",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Redirect root URL to Swagger UI
def redirect_to_swagger(request):
    return redirect('schema-swagger-ui')

urlpatterns = [
    # Root redirects to Swagger
    path('', redirect_to_swagger),

    # Admin
    path('admin/', admin.site.urls),

    # App URLs
    path('api/books/', include('books.urls')),
    path('api/users/', include('users.urls')),
    path('api/orders/', include('orders.urls')),

    # JWT Authentication
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger / OpenAPI
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
```

## Swagger / API Docs

* Swagger UI: `/docs/swagger/`
* ReDoc: `/docs/redoc/`

## Example Create Book Request

```json
{
  "title": "Django for Beginners",
  "author_id": 1,
  "category_id": 2,
  "price": 1500
}
```

## Running the Server

```bash
python manage.py runserver
```

## License

MIT


