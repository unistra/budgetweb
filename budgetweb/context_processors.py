import budgetweb

from .models import PeriodeBudget


def period_years(request):
    # TODO: move to a middleware
    session_year = request.session.get('period_year')
    current_session_year = request.session.get('current_period_year')

    if not session_year:
        try:
            session_year = PeriodeBudget.active.first().annee
        except AttributeError:
            return {'period_years': []}
        request.session['period_year'] = int(session_year)

    if session_year != current_session_year\
            or not request.session.get('period_years'):
        years_dict = {}
        for period in PeriodeBudget.objects.select_related('period')\
                .order_by('annee', 'period__code'):
            default = ' (%s)' % period.period.code if period.is_active else ''
            years_dict[period.annee] = years_dict.get(period.annee) or default
        years = list(sorted(years_dict.items(),
                            key=lambda t: t[0] != session_year))

        request.session['current_period_year'] = request.session['period_year']
        request.session['period_years'] = years
        return {'period_years': years}

    return {'period_years': request.session['period_years']}
