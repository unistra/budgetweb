from .models import PeriodeBudget


def period_years(request):
    session_year = request.session.get('period_year')
    years = PeriodeBudget.objects.order_by('annee').distinct('annee')\
        .values_list('annee', flat=True)

    if not session_year:
        try:
            session_year = PeriodeBudget.active.first().annee
        except AttributeError:
            return {'period_years': []}
        request.session['period_year'] = int(session_year)

    years = years.exclude(annee=session_year)
    return {'period_years': years}
