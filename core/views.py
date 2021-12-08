import base64
import json

from django.core import serializers
from django.db.models import Sum, F, Value
from django.db.models.functions import Concat
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from core.forms import IndexPageForm
from core.models import Order, Client
from core.tools import get_week_list, get_current_week


class OrderView(View):
    def get(self, request):
        orders = Order.objects.all()
        clients = Client.objects.all()
        return render(request, 'order.html', {
            'orders': orders,
            'clients': clients,
        })


def order_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            client_id = request.POST['client_id']
            client = Client.objects.get(id=client_id)
            create_date = request.POST['order_date']
            summa = request.POST['order_sum']
            new_order = Order(client=client, date=create_date, summa=summa)
            new_order.save()
            return HttpResponse(
                json.dumps({
                    'client': f'{client.first_name} {client.last_name}',
                    'create_date': new_order.date,
                    'summa': new_order.summa,
                    'id': new_order.id,
                }),
                content_type="application/json"
            )
    return HttpResponse(
        'Вы не авторизованы',
    )


def order_delete(request, pk):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return redirect('/order/')
    return redirect('/')


def index_page(request):
    default_week = get_current_week()

    # Если запрос из формы, то меняем неделю на запрашиваемый
    if 'week' in request.GET:
        request_week = int(request.GET['week'])
        week = get_week_list()[request_week]
    else:
        week = get_week_list()[default_week]

    filter_by_week = Order.objects.filter(date__gte=week[0], date__lte=week[1]).annotate(fullname=Concat(
        F('client__first_name'),
        Value(' '),
        F('client__last_name')
    ))

    q = filter_by_week.values('date').annotate(daily_sum=Sum('summa')).order_by()

    data = []
    for i in q:
        clients_names_for_day = Order.objects.filter(date=i['date']).annotate(fullname=Concat(
            F('client__first_name'),
            Value(' '),
            F('client__last_name')
        )).values_list('fullname', flat=True).distinct()

        data.append({
            'date': i['date'].strftime('%d. %m. %Y '),
            'clients_name': '; '.join(clients_names_for_day),
            'sum': float(i['daily_sum'])
        })

    total_sum = filter_by_week.aggregate(Sum('summa'))['summa__sum']
    names = filter_by_week.values_list('fullname', flat=True).distinct()

    return render(request, 'index.html', {
        'week_index': default_week,
        'form': IndexPageForm(),
        'data': data,
        'names': names,
        'total_sum': total_sum,
    })


def export_order_by_json(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            if auth[0].lower() == "basic":
                username, password = base64.b64decode(auth[1]).split(':'.encode('ascii'))
                if username.decode("utf-8") == 'admin' and password.decode("utf-8") == '12345':
                    qs = Order.objects.all()
                    qs_json = serializers.serialize('json', qs)
                    return HttpResponse(qs_json, content_type='application/json')
    response = HttpResponse()
    response.status_code = 401
    response['WWW-Authenticate'] = 'Basic realm="%s"' % "Basci Auth Protected"
    return response
