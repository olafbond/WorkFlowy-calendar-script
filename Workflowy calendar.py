import clipboard
from datetime import timedelta, date
import locale

# Settings
year = 2024  # Calendar's date
month_lines = True  # Add months lines inline
week_lines = True  # Add week lines inline
week_day_start = 1  # 1 - Monday, ... 7 - Sunday
day_notes = True  # Add notes to dates for journaling

display_year = '%y'
display_month = '%y%m'
display_date = '%y%m%d'  # DateFormat https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

LOCALE = 'en'  # 'en'. Local variables https://www.localeplanet.com/icu/
if LOCALE == 'ru':
    note_string = '_note="#Цели &#10;#Преодоление &#10;#Знания &#10;#Журнал '
    week_word = 'Неделя'
else:
    note_string = '_note="#Goals &#10;#Achievements &#10;#Knowledge &#10;#Journal '
    week_word = 'Week'

# Don't change anything after this line
locale.setlocale(locale.LC_ALL, LOCALE)


def daterange(s_date, e_date):
    for n in range(int((e_date - s_date).days)):
        yield s_date + timedelta(n)


start_date = date(year, 1, 1)
end_date = date(year + 1, 1, 1)

html = f'<?xml version="1.0"?>\n'
html += f'<opml version="2.0"><body>\n'
html += f'<outline text="&lt;b&gt;{start_date.strftime(display_year)}&lt;/b&gt;"/>\n'  # year's short string

for single_date in daterange(start_date, end_date):

    if month_lines and single_date.day == 1:  # month's string
        html += f'<outline text="&lt;b&gt;{single_date.strftime(display_month)}&lt;/b&gt;"/>\n'

    if week_lines and single_date.isocalendar()[2] == week_day_start:  # weeks's string
        html += f'<outline text="{week_word} {single_date.isocalendar()[1]}"/>\n'

    DateOfWeek = single_date.strftime(display_date) + ' ' + single_date.strftime("%a")  # day's string

    html += f'<outline text="&lt;'
    html += f'time '
    html += f'startYear=&quot;{single_date.strftime("%Y")}&quot; '
    html += f'startMonth=&quot;{single_date.strftime("%m")}&quot; '
    html += f'startDay=&quot;{single_date.strftime("%d")}&quot;'
    if single_date.isocalendar()[2] == 6 or single_date.isocalendar()[2] == 7:  # weekend
        html += f'&gt;&lt;span class=&quot;colored c-pink&quot;'
        html += f'&gt;{DateOfWeek}&lt;'
        html += f'/span&gt;&lt;'
    else:
        html += f'&gt;{DateOfWeek}&lt;'
    html += '/time&gt;"'
    if day_notes:
        html += ' ' + note_string
    html += '" />\n'

html += '</body></opml>'

clipboard.copy(html)
