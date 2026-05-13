from django.shortcuts import render
from .models import LoanProduct
from decimal import Decimal

def calculate_emi(principal, annual_interest_rate, tenure_years):
    r = (annual_interest_rate / 100) / 12
    n = tenure_years * 12
    if r == 0:
        return principal / n
    emi = principal * r * (1 + r)**n / ((1 + r)**n - 1)
    return emi

def index(request):
    results = []
    form_data = {}
    profile_recommendations = []
    
    if request.method == 'POST':
        income = Decimal(request.POST.get('income', 0))
        loan_amount = Decimal(request.POST.get('loan_amount', 0))
        tenure = int(request.POST.get('tenure', 0))
        existing_emi = Decimal(request.POST.get('existing_emi', 0))
        cibil_score = int(request.POST.get('cibil_score', 750))
        loan_type_requested = request.POST.get('loan_type_requested', 'ALL')
        
        form_data = {
            'income': income,
            'loan_amount': loan_amount,
            'tenure': tenure,
            'existing_emi': existing_emi,
            'cibil_score': cibil_score,
            'loan_type_requested': loan_type_requested
        }
        
        # Profile Recommendations
        if cibil_score < 750:
            profile_recommendations.append("Improving your CIBIL score to 750+ will unlock premium loans and lower interest rates.")
        if income < Decimal('25000'):
            profile_recommendations.append("A higher reported monthly income will help you qualify for premium loan products.")
        if existing_emi > 0 and (existing_emi / max(income, Decimal('1'))) > Decimal('0.3'):
            profile_recommendations.append("Your existing debt obligations are quite high. Consider paying off existing EMI debts to improve your eligibility.")

        if loan_type_requested == 'ALL':
            products = LoanProduct.objects.all()
        else:
            products = LoanProduct.objects.filter(loan_type=loan_type_requested)
            
        best_emi = float('inf')
        best_product_index = -1
        
        for product in products:
            eligible = True
            reasons = []
            
            # CIBIL logic
            interest_rate = product.interest_rate
            if cibil_score >= 750:
                interest_rate = max(Decimal('1.0'), interest_rate - Decimal('0.5'))
            elif cibil_score >= 700:
                pass # base rate
            elif cibil_score >= 650:
                interest_rate += Decimal('1.0')
            else:
                interest_rate += Decimal('2.0') # Penalty for very low scores if they somehow pass
                
            # Check product specific min_cibil_score
            if cibil_score < product.min_cibil_score:
                eligible = False
                reasons.append(f"Minimum CIBIL score required is {product.min_cibil_score}.")
            
            # Check tenure
            if tenure > product.max_tenure_years:
                eligible = False
                reasons.append(f"Maximum tenure for {product.name} is {product.max_tenure_years} years.")
            
            # Check income
            if income < product.min_income_required:
                eligible = False
                reasons.append(f"Minimum monthly income required is {product.min_income_required}.")
            
            # Calculate EMI for this product
            emi = calculate_emi(float(loan_amount), float(interest_rate), tenure)
            total_monthly_debt = float(existing_emi) + emi
            dti_ratio = (total_monthly_debt / float(income)) * 100 if income > 0 else 100
            
            # Check DTI
            if Decimal(str(dti_ratio)) > product.max_dti_ratio:
                eligible = False
                reasons.append(f"Debt-to-Income ratio ({dti_ratio:.2f}%) exceeds maximum limit ({product.max_dti_ratio}%).")
                
            if eligible and emi < best_emi:
                best_emi = emi
                best_product_index = len(results)
            
            results.append({
                'product': product,
                'effective_rate': round(interest_rate, 2),
                'eligible': eligible,
                'reasons': reasons,
                'emi': round(emi, 2),
                'dti': round(dti_ratio, 2),
                'is_best': False
            })
            
        if best_product_index != -1:
            results[best_product_index]['is_best'] = True

    return render(request, 'calculator/index.html', {
        'results': results,
        'form_data': form_data,
        'loan_types': LoanProduct.LOAN_TYPES,
        'profile_recommendations': profile_recommendations
    })
