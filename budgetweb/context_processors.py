from .models import PeriodeBudget


def period_years(request):
    session_year = request.session.get('period_year')
    years = PeriodeBudget.objects.order_by('annee').distinct('annee')\
        .values_list('annee', flat=True)
    if session_year:
        years = years.exclude(annee=session_year)
    return {
        'period_years': years
    }
