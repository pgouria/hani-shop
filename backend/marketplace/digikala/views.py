import subprocess
from decimal import Decimal
from django.http import HttpResponse
from .models import Order, Variant, Product
from .infrastructure.digikala_api import DigikalaClient
from django.http import HttpResponseRedirect
import requests
from django.utils import timezone
import jdatetime
from datetime import datetime, timedelta
from django.contrib import messages
 
from django.shortcuts import render, redirect

from django.http import JsonResponse



 

def display_orders(request):
    clinet = DigikalaClient()
    new_orders = clinet.fetch_orders()  # Fetch orders and check for new ones
    orders = Order.objects.all()

    context = {
        'orders': orders,
        'new_orders': new_orders,  # Pass the new orders to the template
    }

    return render(request, 'inventory/orders.html', context)

def filter_orders(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    orders = Order.objects.all()

    if start_date and end_date:
        try:
            # Convert Solar (Jalali) dates to Gregorian dates
            start_date_jalali = jdatetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date_jalali = jdatetime.datetime.strptime(end_date, '%Y-%m-%d')
            
            # Convert to Gregorian
            start_date_gregorian = start_date_jalali.togregorian()
            end_date_gregorian = end_date_jalali.togregorian()
                       
            # Filter orders by the converted Gregorian dates
            orders = orders.filter(created_at__range=(start_date_gregorian, end_date_gregorian))

        except ValueError:
            # Handle invalid date format
            return render(request, 'inventory/orders.html', {'orders': orders, 'error': 'Invalid date format. Please use YYYY-MM-DD.'})

    return render(request, 'inventory/orders.html', {'orders': orders})


# Function to get service status
def get_service_status(service_name):
    try:
        result = subprocess.run(['/usr/bin/systemctl', 'is-active', service_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8').strip()  # Return the status like 'active', 'inactive', etc.
    except Exception as e:
        return f"Error: {str(e)}"

# Function to restart a service
def restart_service(request, service_name):
    if request.method == 'POST':
        subprocess.run(['/usr/bin/systemctl', 'restart', service_name])
        return JsonResponse({'status': 'success', 'message': f'{service_name} restarted successfully!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

# View to display services and their status
def home(request):
    services = ['nginx', 'aryangostar', 'redis','celery','celeryworker']  # List of services to check
    services_status = {service: get_service_status(service) for service in services}

    context = {
        'services_status': services_status
    }
    return render(request, 'home.html', context)

# Function to get service logs
def get_service_logs(service_name):
    try:
        # Fetch the last 100 lines of the service logs using journalctl
        logs  = subprocess.check_output(['/usr/bin/journalctl', '-u', service_name, '-n', '100'], text=True)
        logs_lines = logs.splitlines()  # Split logs into individual lines    
        return    logs_lines if    logs else "No logs available."
    except subprocess.CalledProcessError:
        logs_lines = ["Failed to retrieve logs for the service."]

# View to fetch and return logs for a specific service
def service_logs(request, service_name):
    if request.method == 'GET':
        logs = get_service_logs(service_name)
        return JsonResponse({'status': 'success', 'logs': logs})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def variant_list(request):


    variants = Variant.objects.all()
    selling_stock_filter=request.GET.get("selling_stock_filter")
    if selling_stock_filter:
       variants= variants.filter(selling_stock=selling_stock_filter)
    title_filter = request.GET.get('title_filter')
    if title_filter:
        variants = variants.filter(title__icontains=title_filter)
    return render(request, 'inventory/variant_list.html', {'variants': variants})

def update_prices(request):
    if request.method == 'POST':
        try:
            # Iterate through all variants in the database
            for variant in Variant.objects.all():
                buying_price = request.POST.get(f'buying_price_{variant.variant_id}', '')
                commission_percentage = request.POST.get(f'commission_percentage_{variant.variant_id}', '')
                fulfilment_cost = variant.fulfilment_and_delivery_cost
                stock_in_seller_warehouse= request.POST.get(f'stock_in_seller_warehouse_{variant.variant_id}')


      
                # API request logic...
                url = f"https://seller.digikala.com/api/v1/variants/{variant.variant_id}/"
                token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzM4NCJ9.eyJ0b2tlbl9pZCI6MTkyNzksInBheWxvYWQiOm51bGx9.szlA_BVTVwRHOaMvBe5R4yXl98iWkBALBTntvnwoKvVf2EY13MKcnCq28ymCJ0k0"
                payload = {
                    "site": "digikala",
                    "shipping_type": "digikala",
                    "is_active": False,
                }
                headers = {
                    "authorization": f"{token}",
                    "Content-Type": "application/json"
                }
          
                response = requests.put(url, headers=headers, json=payload)

                if response.status_code == 200:
                    messages.success(request, f"Price updated successfully for variant {variant.variant_id}")
                else:
                    messages.error(request, f"Failed to update price for variant {variant.id}: {response.text}")

            return redirect('variant_list')

        except Exception as e:
            messages.error(request, f"Error in form processing: {str(e)}")
            return redirect('variant_list')

   