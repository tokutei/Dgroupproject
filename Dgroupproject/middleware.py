from purchaseapp.models import CartPost, BuyJudge

class Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, response):
        cart_list = CartPost.objects.all()
        for i in cart_list:
            if i.is_expired() == True:
                target = BuyJudge.objects.filter(stripe_product_id=i.stripe_product_id)
                if len(target) > 0:
                    target = BuyJudge.objects.get(stripe_product_id=i.stripe_product_id)
                    target.stock -= i.stock
                    target.save()
                    i.delete()
        response = self.get_response(response)
        return response
