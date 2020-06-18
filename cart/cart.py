from decimal import Decimal

from django.conf import settings

from shop.models import Product

class Cart(object):

    def __init__(self, request):
        '''初始化购物车'''
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # 新建一个空的购物车
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        '''添加商品或者修改商品的数量'''
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0,
                                     'price':str(product.price)}
        # 覆盖或者是添加数量
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # 把会话标记为已修改，确保保存了数据
        self.session.modified = True

    def remove(self, product):
        '''从购物车里移除商品'''
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        '''迭代购物车里的商品并从数据库中获取商品'''
        product_ids = self.cart.keys()
        # 从数据库中获取各个商品并添加到购物车里面
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price']*item['quantity']
            yield item

    def __len__(self):
        '''获取购物车中商品总数'''
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price'])*item['quantity'] \
            for item in self.cart.values())

    def clear(self):
        # 把购物车从会话中移除
        del self.session[settings.CART_SESSION_ID]
        self.save()

    