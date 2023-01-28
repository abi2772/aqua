import imp
from django.http import HttpResponse
from multiprocessing import context
from django.shortcuts import render,redirect
from calendar import mdays
from datetime import datetime, timedelta,date
from .models import Client, Transaction, Vendor, Stock, Expense
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.pagesizes import A4
# Create your views here.

@login_required(login_url='login')
def index(request):
    context = {
        'search': Client.objects.all(),
        'service_today': Client.objects.filter(service=datetime.now().date())[:5],
        'service_coming': Client.objects.filter(service__gte=datetime.now().date())[:5],
        'amount_credit_this_month': Transaction.objects.filter(created_at__month=datetime.now().month,created_at__year=datetime.now().year,payment_type="Paid", credit__isnull=False).aggregate(Sum('credit')),
        'amount_pending_this_month': Transaction.objects.filter(created_at__month=datetime.now().month,created_at__year=datetime.now().year,payment_type="Not Paid", credit__isnull=False).aggregate(Sum('credit')),
        'amount_expense_this_month': Expense.objects.filter(created_at__month=datetime.now().month,created_at__year=datetime.now().year, amount__isnull=False).aggregate(Sum('amount')),
        'new_client_this_month': Client.objects.filter(created_at__month=datetime.now().month,created_at__year=datetime.now().year).count(),
        'total_service_this_month': Client.objects.filter(service__month=datetime.now().month,service__year=datetime.now().year).count(),
        'total_maintance_this_month': Client.objects.filter(maintenace__month=datetime.now().month,maintenace__year=datetime.now().year).count(),
        'expense_list': Expense.objects.filter(created_at__month=datetime.now().month,created_at__year=datetime.now().year)[:5],
    }
    return render(request, "index.html", context)

@login_required(login_url='login')
def client(request):
    object_list = Client.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(object_list, 10)
    try:
        client = paginator.page(page)
    except PageNotAnInteger:
        client = paginator.page(1)
    except EmptyPage:
        client = paginator.page(paginator.num_pages)
    return render(request, "client.html", {'list':client})

@login_required(login_url='login')
def client_new(request):
    today = datetime.now()
    if request.method == 'POST':
       Client.objects.create(
        name=request.POST['name'],
        phone=request.POST['phone'],
        address=request.POST['address'],
        equipement=request.POST['equipement'],
        installation=request.POST['installation'],
        service = today + timedelta(mdays[today.month]),
        maintenace=date(today.year + 1, today.month, today.day),
        staff=request.POST['staff'],
       )
       return redirect('client')

    return render(request, "clientadd.html")

@login_required(login_url='login')
def info(request, id):

    context = {
        'customer':Client.objects.get(id=id),
        'detail':Transaction.objects.filter(customer_id=id)
    }
    return render(request, "info.html", context)

@login_required(login_url='login')
def transaction(request):
    if request.method == 'POST':
       Transaction.objects.create(
        customer_id=request.POST['customer'],
        debit=request.POST['debit'],
        credit=request.POST['credit'],
        service_type=request.POST['service'],
        payment_type=request.POST['payment']
       )
       instance = Client.objects.get(id=request.POST['customer'])
       instance.service = request.POST['service_date']
       instance.maintenace = request.POST['maintance']
       instance.save()

    return redirect('info',request.POST['customer'])

@login_required(login_url='login')
def vendor(request):
    context = {
        'detail': Vendor.objects.all()
    }
    if request.method == 'POST':
       Vendor.objects.create(
        name=request.POST['name'],
        phone=request.POST['phone'],
        address=request.POST['address']
       )
       return redirect('vendor')

    return render(request, "vendor.html", context)

@login_required(login_url='login')
def vendordetail(request, id):
    context = {
        'vendor':Vendor.objects.get(id=id),
        'detail':Stock.objects.filter(supplier_id=id),
        'balance':Stock.objects.filter(supplier_id=id, balance__isnull=False).aggregate(Sum('balance')),
        'pay':Stock.objects.filter(supplier_id=id, pay__isnull=False).aggregate(Sum('pay')),
    }
    return render(request, "vendordetail.html", context)

@login_required(login_url='login')
def vendortransaction(request):
    if request.method == 'POST':
       Stock.objects.create(
        supplier_id=request.POST['supplier'],
        item=request.POST['item'],
        desc=request.POST['desc'],
        qty=request.POST['qty'],
        price=request.POST['price'],
        pay=request.POST['pay'],
        balance=request.POST['balance'],
       )
    return redirect('vendor-detail',request.POST['supplier'])

@login_required(login_url='login')
def reminder(request):
    context = {
        'service': Client.objects.all(),
        'maintance': Client.objects.all()
    }
    return render(request, "reminder.html",context)

    

@login_required(login_url='login')
def expense(request):
    context = {
        'detail': Expense.objects.all()
    }
    if request.method == 'POST':
       Expense.objects.create(
        detail=request.POST['detail'],
        amount=request.POST['amount'],
       )
       return redirect('expense')
    return render(request, "expense.html", context)

def invoice(request):
    
    monthly_installation = Transaction.objects.filter(created_at__month=datetime.now().month,created_at__year=datetime.now().year,service_type="Installation", credit__isnull=False).aggregate(Sum('credit')).get('credit__sum')
    monthly_service = Transaction.objects.filter(created_at__month=datetime.now().month,created_at__year=datetime.now().year,service_type="Service", credit__isnull=False).aggregate(Sum('credit')).get('credit__sum')
    monthly_maintance = Transaction.objects.filter(created_at__month=datetime.now().month,created_at__year=datetime.now().year,service_type="Maintance", credit__isnull=False).aggregate(Sum('credit')).get('credit__sum')
    monthly_installation_total = Transaction.objects.filter(created_at__month=datetime.now().month,created_at__year=datetime.now().year,service_type="Installation", credit__isnull=False).count()
    monthly_service_total = Transaction.objects.filter(created_at__month=datetime.now().month,created_at__year=datetime.now().year,service_type="Service", credit__isnull=False).count()
    monthly_maintance_total = Transaction.objects.filter(created_at__month=datetime.now().month,created_at__year=datetime.now().year,service_type="Maintance", credit__isnull=False).count()

    if monthly_installation == None:
        monthly_installation = 0
    if monthly_service == None:
        monthly_service = 0
    if monthly_maintance == None:
        monthly_maintance = 0    
    
    total = monthly_installation+monthly_service+monthly_maintance
    # Create the HttpResponse object 
    response = HttpResponse(content_type='application/pdf') 
    d = datetime.today().strftime( 'Invoice-%m-%d')
    response['Content-Disposition'] = f'filename="{d}.pdf"'
    buffer = BytesIO()
    p = canvas.Canvas (buffer, pagesize=A4)

    p.setFont("Helvetica", 20, leading=None)
    p.setFillColorRGB(0,0,0)
    p.drawString(280,800, "Aqua Solution Monthly Invoice")
    p.setFont("Helvetica", 15, leading=None)
    p.drawString(470,780, f'{datetime.now().date()}')
    p.setFont("Helvetica", 12, leading=None)
    p.drawString(40,750, "DESCRIPTION")
    p.drawString(250,750, "NO.")
    p.drawString(480,750, "AMOUNT")
    p.line(30,740, 550,740)
    p.line(30,738, 550,738)
    p.drawString(50,710, "Installation")
    p.drawString(250,710, f"#{monthly_installation_total}")
    p.drawString(480,710, f"Rs. {monthly_installation}")
    p.drawString(50,690, "Service")
    p.drawString(250,690, f"#{monthly_service_total}")
    p.drawString(480,690, f"Rs. {monthly_service}")
    p.drawString(50,670, "Maintance")
    p.drawString(250,670, f"#{monthly_maintance_total}")
    p.drawString(480,670, f"Rs. {monthly_maintance}")
    p.line(30,660, 550,660)
    p.drawString(50,640, "Total")
    p.drawString(480,640, f"Rs. {total}")
    p.setTitle(f'Monthly Report {d}')
    p.showPage() 
    p.save()


    pdf = buffer.getvalue() 
    buffer.close() 
    response.write(pdf)
    return response

def search(request):
    if request.method == 'POST':
        name = request.POST['name'].split('-')
        find = Client.objects.get(id=int(name[0]))
        if find:
            return redirect('info',find.id)
    return redirect('home')


def paid_by_client(request):
    id = request.GET.get('id')
    user_id = request.GET.get('trn')
    get_transaction = Transaction.objects.get(id=id)
    get_transaction.payment_type = "Paid"
    get_transaction.save()
    return redirect('info', user_id)

def delete_client(request, id):
    Client.objects.get(id=id).delete()
    return redirect('client')

    