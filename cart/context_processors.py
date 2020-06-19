from .cart import Cart

def cart(request):
    # 其实实例化一个Cart对象就是在session里保存一个键是cart
    # 值是选购的商品信息的字典的字典
    # 所以这里新建的对象跟add视图创建的对象
    # 指代的都是同一个对象
    # 这就是为什么两者会同步
    return {'cart':Cart(request)}