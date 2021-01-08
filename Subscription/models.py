from django.db import models



class SubscriptionType(models.Model):
    plan_name       = models.CharField(max_length=100)
    description     = models.TextField()
    plan_validity   = models.PositiveIntegerField()
    price           = models.FloatField()
    is_active       = models.BooleanField()
    user_enrolled   = models.PositiveIntegerField()


    def __str__(self):
        return self.plan_name
