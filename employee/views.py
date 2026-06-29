from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmployeeForm
from .models import Employee


# Retrieve and display all employee records
def show(request):
    # Fetch all employees from the database
    employees = Employee.objects.all()
    # Render the list page with employee details
    return render(request, "show.html", {'employees': employees})


# Create a new employee record (displays form or processes submitted form data)
def emp(request):
    if request.method == "POST":
        # Bind submitted POST data to the EmployeeForm
        form = EmployeeForm(request.POST)
        if form.is_valid():
            # Save the new employee record to the database
            form.save()
            # Redirect to the employee list page
            return redirect('/show')
    else:
        # Instantiate an empty form for GET request
        form = EmployeeForm()
    return render(request, 'index.html', {'form': form})


# Display form pre-filled with data for a specific employee to edit
def edit(request, id):
    # Fetch the employee by ID or raise a 404 error if not found
    employee = get_object_or_404(Employee, id=id)
    # Bind employee data to the form for rendering
    form = EmployeeForm(instance=employee)
    return render(request, 'edit.html', {'employee': employee, 'form': form})


# Process the update of an existing employee record
def update(request, id):
    # Fetch the employee by ID or raise a 404 error if not found
    employee = get_object_or_404(Employee, id=id)
    # Bind POST data to the existing employee instance
    form = EmployeeForm(request.POST, instance=employee)
    if form.is_valid():
        # Save updated details to the database
        form.save()
        # Redirect to the employee list page
        return redirect("/show")
    return render(request, 'edit.html', {'form': form, 'employee': employee})


# Delete a specific employee record
def destroy(request, id):
    # Fetch the employee by ID or raise a 404 error if not found
    employee = get_object_or_404(Employee, id=id)
    if request.method == "POST":
        # Delete record from database if confirmed via POST
        employee.delete()
        # Redirect back to the employee list page
        return redirect("/show")
    # Render the delete confirmation page for GET requests
    return render(request, 'confirm_delete.html', {'employee': employee})