from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmployeeForm
from .models import Employee


def show(request):
    employees = Employee.objects.all()
    return render(request, "show.html", {'employees': employees})


def emp(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/show')
    else:
        form = EmployeeForm()
    return render(request, 'index.html', {'form': form})


def edit(request, id):
    employee = get_object_or_404(Employee, id=id)
    form = EmployeeForm(instance=employee)
    return render(request, 'edit.html', {'employee': employee, 'form': form})


def update(request, id):
    employee = get_object_or_404(Employee, id=id)
    form = EmployeeForm(request.POST, instance=employee)
    if form.is_valid():
        form.save()
        return redirect("/show")
    return render(request, 'edit.html', {'form': form, 'employee': employee})


def destroy(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == "POST":
        employee.delete()
        return redirect("/show")
    return render(request, 'confirm_delete.html', {'employee': employee})