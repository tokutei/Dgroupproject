from purchaseapp.models import CartPost, BuyJudge
from foods.models import Food
from django.utils import timezone
from django.utils.timezone import now
import datetime
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
        foods_list = Food.objects.all()
        for i in foods_list:
            if datetime.date.today() > i.shelf_life:
                i.delete()
        return response
