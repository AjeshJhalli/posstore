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
  
  @property
  def minimum_quantity(self):
    return min([price_break.minimum_units for price_break in PriceBreak.objects.filter(product_id=self.pk)])
  
  def get_price(self, quantity):
    
    price_breaks = PriceBreak.objects.filter(product_id=self.pk)
    
    if len(price_breaks) == 0:
      return 0
    
    if quantity < min([price_break.minimum_units for price_break in price_breaks]):
      return 0
    
    total = 0
    prev_qty = 0
    highest_past = True
    
    for price_break in price_breaks:
      
      current_qty = price_break.minimum_units
      
      if current_qty >= quantity:
        diff = quantity - prev_qty
        total += diff * price_break.price
        highest_past = False
        break
      else:
        diff = current_qty - prev_qty  
        total += diff * price_break.price
      
      prev_qty = current_qty
      
    if highest_past:
      diff = quantity - prev_qty  
      total += diff * price_break.price
    
    return total
  
  
  def get_price_breakdown(self, quantity):
    
    price_breaks = PriceBreak.objects.filter(product_id=self.pk)
    
    if len(price_breaks) == 0:
      return 'No price breaks configured', 0
    
    if quantity < min([price_break.minimum_units for price_break in price_breaks]):
      return 'Invalid quantity', 0
    
    breakdown_string = ''
    total = 0
    
    prev_qty = 0
    
    highest_past = True
    
    for price_break in price_breaks:
      
      current_qty = price_break.minimum_units
      formatted_price = '£{0:.2f}'.format(price_break.price)
      
      if current_qty >= quantity:
        diff = quantity - prev_qty
        total += diff * price_break.price
        breakdown_string += str(diff) + ' x ' + formatted_price + ' + '
        highest_past = False
        break
      else:
        diff = current_qty - prev_qty  
        total += diff * price_break.price
        breakdown_string += str(diff) + ' x ' + formatted_price + ' + '
      
      prev_qty = current_qty
      
    if highest_past:
      diff = quantity - prev_qty  
      total += diff * price_break.price
      breakdown_string += str(diff) + ' x ' + formatted_price + ' + '
  
    if len(breakdown_string) > 2:
      breakdown_string = breakdown_string[:-2]
      
    breakdown_string += '= £' + '{0:.2f}'.format(total)
    
    return breakdown_string, total
  
  
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


class CartItem(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.IntegerField()
  
  def __str__(self):
    return self.product.name + ' x ' + str(self.quantity)
  
  @property
  def price(self):
    return self.product.get_price(self.quantity)
