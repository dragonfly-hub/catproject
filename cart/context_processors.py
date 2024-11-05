#یک فایل که ابجکت ریکوئست رو به عنوان ارگومان ورودی دریافت میکنه و یه دیکشنری 

from .cart import Cart

def cart(request):
    return {'cart':Cart(request)}