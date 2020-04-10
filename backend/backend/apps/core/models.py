import crypt
from django.db import models
from django.contrib.auth.models import AbstractUser


class HashModel(models.Model):
    """
    A model to reuse the `hash` field
    """
    hash = models.CharField(default='', max_length=255, null=True, unique=True)

    class Meta:
        abstract = True

    def encrypt(self, value):
        salt = crypt.mksalt(crypt.METHOD_MD5)
        return str(crypt.crypt(value, salt=salt)).split('$')[3].replace('/', '-')

    def generate_hashes(self):
        self.hash = self.encrypt(str(self.id))

    def _do_insert(self, manager, using, fields, update_pk, raw):
        self.generate_hashes()
        return super()._do_insert(manager, using, fields, update_pk, raw)


class Province(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'core_province'

    def __str__(self):
        return self.name


class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    latitude = models.CharField(max_length=255, null=True)
    longitude = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'core_city'
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.name


class Address(models.Model):
    line_1 = models.CharField(max_length=255)
    line_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'core_address'


class User(AbstractUser):
    phone = models.CharField(max_length=255, null=True, blank=True)
    from_time = models.TimeField(null=True, blank=True)
    to_time = models.TimeField(null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'core_user'

    def __str__(self):
        return str(self.username)


class STLModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='models')

    class Meta:
        db_table = 'core_stlmodel'


class Product(models.Model):
    name = models.CharField(max_length=255)
    stock = models.IntegerField(default=0)
    photo = models.ImageField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # stl_model = models.ForeignKey(STLModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'core_product'