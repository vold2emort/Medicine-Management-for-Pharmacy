from django.db import models

# Create your models here.
class Medicine(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    diseases_used_for = models.CharField(
        max_length=300,
        help_text="Comma separated diseases"
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)

    quantity = models.PositiveIntegerField()

    expiry_date = models.DateField()

    image = models.ImageField(
        upload_to='medicines/',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
