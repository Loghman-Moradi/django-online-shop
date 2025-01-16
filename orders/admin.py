import jdatetime
from django.contrib import admin
from account.models import Address
from orders.models import OrderItem, Order, OrderAddress, ReturnedProducts
import openpyxl
from django.http import HttpResponse
import csv


def export_to_excel(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="orders.xlsx"'
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Orders'

    columns = ['ID', 'Frst Name', 'Last Name', 'Phone', 'Address', 'Total Cost', 'Final Cost', 'Paid', 'Status', 'Created']
    ws.append(columns)

    for order in queryset:
        if order.created_at:
            created_gregorian = jdatetime.datetime.fromgregorian(datetime=order.created_at).togregorian()
            created_gregorian = created_gregorian.strftime('%Y-%m-%d %H:%M:%S')
        else:
            created_gregorian = ''

        if order.order:
            ws.append([
                order.id,
                order.get_first_name(),
                order.get_last_name(),
                order.get_phone_number(),
                order.get_address(),
                order.get_total_cost(),
                order.get_final_cost(),
                order.paid,
                order.status,
                created_gregorian,
            ])
        else:
            ws.append([
                order.id,
                '',  # First Name
                '',  # Last Name
                '',  # Phone
                '',  # Address
                '',  # Postal Code
                '',  # Province
                '',  # City
                order.paid,
                created_gregorian,
            ])

    wb.save(response)
    return response


export_to_excel.short_description = 'Export to Excel'


def export_to_csv(modladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Frst Name', 'Last Name', 'Phone', 'Address', 'Total Cost', 'Final Cost', 'Paid',
                     'Status', 'Created'])

    for order in queryset:
        writer.writerow([
            order.id,
            order.get_first_name(),
            order.get_last_name(),
            order.get_phone_number(),
            order.get_address(),
            order.get_total_cost(),
            order.get_final_cost(),
            order.paid,

        ])

    return response


export_to_csv.short_description = 'Export to CSV'



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'get_first_name', 'get_last_name', 'get_phone_number', 'get_address', 'get_total_cost',
                    'paid', 'status', 'created_at', 'delivery_date')
    list_editable = ['status']
    actions = [export_to_excel, export_to_csv]

    readonly_fields = (
        'get_first_name',
        'get_last_name',
        'get_phone_number',
        'get_address',
        'get_total_cost',
        'get_items',
        'updated_at',
        'paid'
    )

    def get_first_name(self, obj):
        return obj.get_first_name()
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.get_last_name()
    get_last_name.short_description = 'Last Name'

    def get_phone_number(self, obj):
        return obj.get_phone_number()
    get_phone_number.short_description = 'Phone Number'

    def get_address(self, obj):
        return obj.get_address()

    get_address.short_description = 'Address'

    def get_total_cost(self, obj):
        return obj.get_final_cost()

    get_total_cost.short_description = 'Final cost'

    def get_items(self, obj):
        items_list = ", ".join([f"{item.product.name} ({item.quantity}:number)" for item in obj.items.all()])
        return items_list if items_list else "There are no items"

    get_items.short_description = 'order item'


@admin.register(ReturnedProducts)
class ReturnedProductsAdmin(admin.ModelAdmin):
    list_display = ('order_item', 'user', 'request_date', 'status')
    list_editable = ['status']



























