from django.db import models


class Client(models.Model):
    first_name = models.CharField(verbose_name='Имя', max_length=100)
    last_name = models.CharField(verbose_name='Фамилия', max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Order(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Двта заказа')
    summa = models.DecimalField(verbose_name='Сумма заказа', default=0, max_digits=10, decimal_places=2)
