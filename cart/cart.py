from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session

        self.request = request

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # lets make sure cart is available on all our sites
        self.cart = cart


    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
    
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # save carty to profile models
            current_user.update(old_cart=str(carty))


    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
    
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # save carty to profile models
            current_user.update(old_cart=str(carty))

            

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities


    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # Get cart
        ourcart = self.cart

        # Update cart
        ourcart[product_id] = product_qty

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # save carty to profile models
            current_user.update(old_cart=str(carty))

        thing = self.cart
        return thing
        

    
    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # save carty to profile models
            current_user.update(old_cart=str(carty))



    def cart_total(self):

        # Get product IDs
        product_ids = self.cart.keys()

        # lookup those keys in our database model
        products = Product.objects.filter(id__in=product_ids)

        # get quantities
        quantities = self.cart

        # start counting at zerro
        total = 0

        for key, value in quantities.items():
            # convert key string
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)

        return total