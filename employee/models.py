from django.db import models

# Model representing an employee in the system
class Employee(models.Model):
    # Unique identifier for the employee (e.g., EMP001)
    eid = models.CharField(max_length=20, unique=True)
    
    # Employee's full name
    ename = models.CharField(max_length=100)
    
    # Employee's email address
    eemail = models.EmailField()
    
    # Employee's contact phone number
    econtact = models.CharField(max_length=15)

    class Meta:
        # Maps model to the 'employee' table in the database
        db_table = "employee"