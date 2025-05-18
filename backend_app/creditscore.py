from datetime import datetime

def calculate_credit_score(member_id, chama_id):
    from .models import Members, Loans, Contributions, Chamas
    from django.db.models import Sum
    chama = Chamas.objects.get(chama_id=chama_id)
    member = Members.objects.get(member_id=member_id,chama=chama)

    # 1. Savings Score
    total_savings = Contributions.objects.filter(member=member).aggregate(total=Sum('amount'))['total'] or 0
    savings_score = min(total_savings / 1000, 1.0) * 30  # e.g., max score at 1000 KES saved

    # 2. Repayment Timeliness
    loans = Loans.objects.filter(name=member)
    on_time_repayments = 0
    total_loans = loans.count()

    for loan in loans:
        if loan.loan_status == 'paid' and loan.loan_date and loan.loan_deadline:
            repayment_days = (loan.loan_deadline - loan.loan_date).days
            if repayment_days >= 0:
                on_time_repayments += 1

    timeliness_score = (on_time_repayments / total_loans) * 40 if total_loans > 0 else 0

    # 3. Repayment Completion
    fully_paid_loans = Loans.objects.filter(name=member, loan_status='paid').count()
    completion_score = (fully_paid_loans / total_loans) * 20 if total_loans > 0 else 0

    # 4. Loan Frequency (penalize too many loans)
    loan_frequency_penalty = min(total_loans / 10, 1.0) * 10
    loan_frequency_score = 10 - loan_frequency_penalty

    # Final score
    total_score = savings_score + timeliness_score + completion_score + loan_frequency_score
    member.credit_score = total_score
    member.save()
    return round(total_score, 2)
