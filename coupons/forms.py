from django import forms
from django.utils.translation import gettext_lazy as _

class CouponApplyForm(forms.Form):
    '''用户提交优惠码的表单'''
    code = forms.CharField(label=_('Coupon'))