from datetime import timedelta

from django.db import models
from django.db.models import Model, CharField, IntegerField, ImageField, SlugField, \
    PositiveSmallIntegerField, DateTimeField, JSONField, ForeignKey, CASCADE, CheckConstraint, Q
from django.utils.text import slugify
from django.utils.timezone import now
from django_ckeditor_5.fields import CKEditor5Field
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = SlugField(max_length=255, unique=True, editable=False)

    class MPTTMeta:
        order_insertion_by = ['name']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        while Category.objects.filter(slug=self.slug).exists():
            self.slug += '-1'

        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name


class Product(Model):
    name = CharField(max_length=255)
    price = IntegerField()
    discount_percent = PositiveSmallIntegerField(default=0, db_default=0)
    quantity = PositiveSmallIntegerField(default=0, db_default=0)
    category = ForeignKey('apps.Category', CASCADE, related_name='products')
    updated_at = DateTimeField(auto_now=True)
    specifications = JSONField(default=dict)
    created_at = DateTimeField(auto_now_add=True)
    description = CKEditor5Field()

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(discount_percent__lte=100),
                name="discount_percent__lte__100",
            )
        ]

    @property
    def is_new(self) -> bool:
        return self.created_at >= now() - timedelta(days=7)

    @property
    def in_stock(self) -> bool:
        return self.quantity > 0

    @property
    def current_price(self):
        return self.price - self.price * self.discount_percent // 100

    @property
    def show_spec(self):
        return list(self.specifications.values())[:5]

    @property
    def is_premium(self) -> bool:
        return


class ProductImage(Model):
    image = ImageField(upload_to='products/%Y/%m/%d/')
    product = ForeignKey('apps.Product', CASCADE, related_name='images')


