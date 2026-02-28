from .cart import Cart
def cart_length(request):
    cart = Cart(request)
    return {'cart_length': cart.__len__()}

#lets u use cart_length in our templates to show the number of items in the cart. We need to add this context processor to our settings.py file under TEMPLATES -> OPTIONS -> 'context_processors' list.