import redis
from django.conf import settings

from .models import Product


# 连接redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                username=settings.REDIS_USERNAME,
                password=settings.REDIS_PASSWORD)

class Recommender(object):

    def get_product_key(self, id):
        return f'product:{id}:purchased_with'

    def products_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # 获取和这个商品一起买的其他商品
                if product_id != with_id:
                    # 增加一起买的权重
                    r.zincrby(self.get_product_key(product_id),
                              1,
                              with_id)
    
    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # 如果只买了一个商品
            suggestions = r.zrange(self.get_product_key(product_ids[0]),
                                   0,1,desc=True)[:max_results]
        else:
            # 生成一个临时的key
            flat_ids = ''.join(str(id) for id in product_ids)
            tmp_key = f'tmp_{flat_ids}'
            keys = [self.get_product_key(id) for id in product_ids]
            # 把所有的商品为键的集合并起来了
            # 相同的商品会把权重加起来
            r.zunionstore(tmp_key,keys)
            # 移除当前订单里已有的商品
            r.zrem(tmp_key,*product_ids)
            # 按照score降序排列，获取推荐一起购买的商品
            suggestions = r.zrange(tmp_key,0,-1,desc=True)[:max_results]
            # 移除这个临时的键
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]
        # 获取推荐的商品，用它们的权重顺序排序
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x:suggested_products_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id',flat=True):
            r.delete(self.get_product_key(id))

    
