# myapp/context_processors.py
from .models import Wishlist, Cart


def site_counts(request):
    """
    Makes wishlist_count, total_quantity, and total (cart subtotal)
    available in every template automatically.
    """
    wishlist_count = 0
    total_quantity = 0
    total = 0

    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()

        cart_items = Cart.objects.filter(user=request.user).select_related("product")
        for item in cart_items:
            total_quantity += item.quantity
            total += item.product.price * item.quantity

    return {
        "wishlist_count": wishlist_count,
        "total_quantity": total_quantity,
        "total": total,
    }
    
    
