from django.db import models

class Expense(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    is_late = models.BooleanField(default=False)
    installments = models.IntegerField(default=1)

    def __str__(self):
        return self.description

class Income(models.Model):
    source = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_received = models.DateField()

    def __str__(self):
        return f"{self.source} - {self.amount}"
