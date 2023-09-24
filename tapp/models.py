from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Products Model
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Customers Model
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Case(models.Model):

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('pending', 'Pending'),
        ('closed', 'Closed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description1 = models.TextField()
    description2 = models.TextField()
    start_time = models.DateTimeField(null=True, blank=True,default=timezone.now)  # Case oluşturulduğunda otomatik olarak atanır
    end_time = models.DateTimeField(null=True, blank=True)  # Case tamamlandığında atanır, başlangıçta boş bırakılır
    duration = models.IntegerField(null=True, blank=True)  # Süreyi dakika cinsinden saklayacak sütun
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

    def __str__(self):
        return f"Case {self.id}"

    def duration(self):
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time).total_seconds() / 60
        else:
            return None

    def save(self, *args, **kwargs):
        if self.end_time and self.start_time:
            # Zaman dilimi bilgisi eklemek için timezone kullanın
            self.duration = (self.end_time - self.start_time).total_seconds() / 60
        else:
            self.duration = None
        super(Case, self).save(*args, **kwargs)



