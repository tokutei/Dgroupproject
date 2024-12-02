from purchaseapp.models import CartPost


def my_cart(request):
    user_list = CartPost.objects.filter(user=request.user.id)
    cart_stock = 0
    if len(user_list) > 0:
        for i in user_list:
            cart_stock += i.stock
    return {'cart_stock': cart_stock}
