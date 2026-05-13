from django.core.management.base import BaseCommand
from calculator.models import LoanProduct
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seeds the database with initial loan products demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting existing loan products...")
        LoanProduct.objects.all().delete()

        products = [
            {
                'name': 'Elite Home Loan',
                'loan_type': 'HOME',
                'interest_rate': Decimal('7.50'),
                'min_cibil_score': 750,
                'max_tenure_years': 30,
                'min_income_required': Decimal('60000.00'),
                'max_dti_ratio': Decimal('55.00')
            },
            {
                'name': 'Gold Standard Home Loan',
                'loan_type': 'HOME',
                'interest_rate': Decimal('8.50'),
                'min_cibil_score': 650,
                'max_tenure_years': 30,
                'min_income_required': Decimal('40000.00'),
                'max_dti_ratio': Decimal('50.00')
            },
            {
                'name': 'Swift Personal Loan',
                'loan_type': 'PERSONAL',
                'interest_rate': Decimal('12.00'),
                'min_cibil_score': 650,
                'max_tenure_years': 5,
                'min_income_required': Decimal('25000.00'),
                'max_dti_ratio': Decimal('40.00')
            },
            {
                'name': 'Easy Access Personal Loan',
                'loan_type': 'PERSONAL',
                'interest_rate': Decimal('15.00'),
                'min_cibil_score': 550,
                'max_tenure_years': 3,
                'min_income_required': Decimal('15000.00'),
                'max_dti_ratio': Decimal('35.00')
            },
            {
                'name': 'Speedy Vehicle Loan',
                'loan_type': 'VEHICLE',
                'interest_rate': Decimal('9.50'),
                'min_cibil_score': 650,
                'max_tenure_years': 7,
                'min_income_required': Decimal('30000.00'),
                'max_dti_ratio': Decimal('45.00')
            },
            {
                'name': 'Subprime Vehicle Loan',
                'loan_type': 'VEHICLE',
                'interest_rate': Decimal('14.00'),
                'min_cibil_score': 500,
                'max_tenure_years': 5,
                'min_income_required': Decimal('20000.00'),
                'max_dti_ratio': Decimal('30.00')
            },
            {
                'name': 'Premium Business Loan',
                'loan_type': 'BUSINESS',
                'interest_rate': Decimal('10.50'),
                'min_cibil_score': 700,
                'max_tenure_years': 10,
                'min_income_required': Decimal('100000.00'),
                'max_dti_ratio': Decimal('45.00')
            },
            {
                'name': 'Education Support Loan',
                'loan_type': 'EDUCATION',
                'interest_rate': Decimal('7.00'),
                'min_cibil_score': 600,
                'max_tenure_years': 15,
                'min_income_required': Decimal('15000.00'),
                'max_dti_ratio': Decimal('30.00')
            },
        ]

        for p_data in products:
            LoanProduct.objects.create(**p_data)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(products)} loan products.'))
