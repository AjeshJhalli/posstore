from django.db import models


class Customer(models.Model):
  name = models.TextField()
  
  def __str__(self):
    return self.name


class Address(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  line1 = models.TextField()
  line2 = models.TextField()
  city = models.TextField()
  county = models.TextField()
  country = models.TextField()
  postcode = models.TextField()
  

class Product(models.Model):
  name = models.TextField()
  lead_time_days = models.IntegerField()
  image_url = models.TextField(null=True)
  
  def __str__(self):
    return self.name
  
  
class PriceBreak(models.Model):
  minimum_units = models.IntegerField(default=0)
  price = models.FloatField()
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  
  def __str__(self):
    return self.product.name + ' - ' + str(self.minimum_units) + ' units'


class Order(models.Model):
  order_date = models.DateField()
  invoice_address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, related_name='invoice_address_id')
  delivery_addresses = models.ManyToManyField(Address)
  
  
class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
  quantity = models.IntegerField()
