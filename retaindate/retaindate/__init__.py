from datetime import datetime
from calendar import monthrange

def is_obsolete(date,
        dailies=90,
        monthlies=12*31,
        yearlies=5*365):

    """
    Checks is a date is considered obsolete. Resolution = 1 day

    There are 3 different time-frames:

    daily
        dates are all marked as non-obsolete

    monthly
        only the last day of the month is considered non-obsolete

    yearly
        only the last day of the year is marked as non-obsolete.

    Parameters
    ----------

    date
        The date to check (should be a ``datetime`` instance)

    dailies
        For how many days are files retained on a daily basis
        Default = 90 days

    monthlies
        For how many days are files retained on a monthly basis
        Default: 12*31 days

    yearlies
        For how many days are files retained on a yearly basis
        Default: 5*365 days
    """

    now = datetime.now()
    delta = (now - date).days

    last_day_of_month = monthrange(date.year, date.month)[1]

    if delta <= dailies:
        # while in the 'dailies' period, we accept anything
        return False

    if delta <= monthlies:
        # while in the 'monthlies' period, we accept only the last day of the
        # month.
        if date.day == last_day_of_month:
            return False
        else:
            return True

    if delta <= yearlies:
        # while in the 'yearlies' period, we accept only the last day of the
        # year.
        if date.day == 31 and date.month == 12:
            return False
        else:
            return True

    # anything else is obsolete
    return True
