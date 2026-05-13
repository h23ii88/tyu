from django.db import models

class LoanProduct(models.Model):
    LOAN_TYPES = [
        ('HOME', 'Home Loan'),
        ('VEHICLE', 'Vehicle Loan'),
        ('PERSONAL', 'Personal Loan'),
        ('BUSINESS', 'Business Loan'),
        ('EDUCATION', 'Education Loan'),
    ]
    name = models.CharField(max_length=100, help_text="Name of the loan product (e.g., Home Loan, Personal Loan)")
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES, default='PERSONAL', help_text="Type of the loan")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Annual interest rate in % (e.g., 8.50)")
    min_cibil_score = models.PositiveIntegerField(default=650, help_text="Minimum CIBIL score required for this loan product")
    max_tenure_years = models.PositiveIntegerField(help_text="Maximum allowed loan tenure in years")
    min_income_required = models.DecimalField(max_digits=12, decimal_places=2, help_text="Minimum monthly income required to be eligible")
    max_dti_ratio = models.DecimalField(max_digits=5, decimal_places=2, help_text="Maximum allowed DTI ratio in % (e.g., 50.0 for 50%)")

    def __str__(self):
        return f"{self.name} ({self.interest_rate}%)"
