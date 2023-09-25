import clipboard
from datetime import timedelta, date
import locale

# Settings
year = 2024  # For which year would you like to generate a calendar?
month_lines = True  # Add months lines inline?
day_notes = True  # Add notes to dates for journaling?
note_string = '_note="#Goals &#10;#Achievements &#10;#Knowledge &#10;#Journal "'
LOCALE = 'en'  # Local variables https://www.localeplanet.com/icu/
display_date = '%y%m%d'  # DateFormat https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

# Don't change anything after this line
locale.setlocale(locale.LC_ALL, LOCALE)


def daterange(s_date, e_date):
    for n in range(int((e_date - s_date).days)):
        yield s_date + timedelta(n)


ye = year - 2000

html = f'<?xml version="1.0"?>\n'
html += f'<opml version="2.0"><body>\n'
html += f'<outline text="&lt;b&gt;{ye}&lt;/b&gt;">\n'  # year's string

start_date = date(year, 1, 1)
end_date = date(year + 1, 1, 1)

for single_date in daterange(start_date, end_date):

    if month_lines and single_date.day == 1:  # month's string
        html += f'<outline text="&lt;b&gt;{single_date.strftime("%y%m")}&lt;/b&gt;"/>\n'

    DateOfWeek = single_date.strftime(display_date) + ' ' + single_date.strftime("%a")  # day's string

    if single_date.strftime("%w") != '0' and single_date.strftime("%w") != '6':  # working days
        html += f'<outline text="{DateOfWeek}"'
    else:  # weekend
        html += f'<outline text="&lt;span class=&quot;colored c-pink&quot;&gt;{DateOfWeek}&lt;/span&gt;"'

    if day_notes:
        html += ' ' + note_string

    html += ' />\n'

html += '</outline></body></opml>'

clipboard.copy(html)
