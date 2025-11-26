# seed.py
import os
import django
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')
django.setup()

from django.contrib.auth.models import User
from books.models import Author, Category, Book
from orders.models import CartItem, Order, OrderItem

def seed_users():
    """Create some test users."""
    if not User.objects.filter(username='testuser').exists():
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        print(f"Created user: {user.username}")
    else:
        print("User 'testuser' already exists")

def seed_categories():
    """Create sample categories."""
    categories = ['Fiction', 'Non-Fiction', 'Science', 'History']
    for name in categories:
        category, created = Category.objects.get_or_create(name=name)
        if created:
            print(f"Created category: {name}")

def seed_authors():
    """Create sample authors."""
    authors = ['Jane Austen', 'Mark Twain', 'Isaac Newton', 'Albert Einstein']
    for name in authors:
        author, created = Author.objects.get_or_create(name=name)
        if created:
            print(f"Created author: {name}")

def seed_books():
    """Create sample books."""
    authors = list(Author.objects.all())
    categories = list(Category.objects.all())

    for i in range(1, 6):
        book, created = Book.objects.get_or_create(
            title=f"Book {i}",
            defaults={
                "author": random.choice(authors),
                "category": random.choice(categories),
                "price": random.randint(500, 2000)
            }
        )
        if created:
            print(f"Created book: {book.title}")

def seed_cart_and_orders():
    """Add some items to cart and create an order for testuser."""
    user = User.objects.get(username='testuser')
    books = list(Book.objects.all())

    # Add items to cart
    for book in books[:3]:
        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            book=book,
            defaults={"quantity": random.randint(1, 3)}
        )
        if created:
            print(f"Added {book.title} to {user.username}'s cart")

    # Create a sample order
    cart_items = CartItem.objects.filter(user=user)
    if cart_items.exists():
        total_amount = sum(item.book.price * item.quantity for item in cart_items)
        order = Order.objects.create(user=user, total_amount=total_amount)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )
        cart_items.delete()  # Clear cart
        print(f"Created order {order.id} for {user.username} with {len(order.items.all())} items")

if __name__ == "__main__":
    seed_users()
    seed_categories()
    seed_authors()
    seed_books()
    seed_cart_and_orders()
    print("Seeding complete!")
