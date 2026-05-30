from django.shortcuts import render, redirect
from .models import Attendance
from datetime import date

def home(request):
    records = Attendance.objects.all().order_by('-date', '-time')
    
    # Date filter
    filter_date = request.GET.get('date')
    if filter_date:
        records = records.filter(date=filter_date)
    
    today_count = Attendance.objects.filter(date=date.today()).count()
    today_date = date.today().strftime("%B %d, %Y")
    
    return render(request, 'dashboard/home.html', {
        'records': records,
        'today_count': today_count,
        'today_date': today_date,
        'filter_date': filter_date
    })

def delete_attendance(request, id):
    record = Attendance.objects.get(id=id)
    record.delete()
    return redirect('home')