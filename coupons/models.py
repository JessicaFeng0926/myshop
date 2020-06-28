from django.db import models
from django.core.validators import MinValueValidator, \
    MaxValueValidator
# Create your models here.

class Coupon(models.Model):
    code = models.CharField(max_length=50,
                            unique=True)
    # 有效期的起始时间
    valid_from = models.DateTimeField()
    # 有效期的结束时间
    valid_to = models.DateTimeField()
    # 规定了最大值和最小值
    discount = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(100)]
    )
    active = models.BooleanField()

    def __str__(self):
        return self.code
