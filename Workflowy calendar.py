import clipboard
from datetime import timedelta, date
import locale

# Settings
year = 2024  # Calendar's date
month_lines = True  # Add months lines inline
week_lines = False  # Add week lines inline
week_day_start = 1  # 1 - Monday, ... 7 - Sunday
day_notes = True  # Add notes to dates for journaling
day_notes_bdays = True  # Add BDays from Google calendar's export file
gcalendar_file = "addressbook#contacts@group.v.calendar.google.com.ics"

display_year = '%y'
display_month = '%y%m'
display_date = '%y%m%d'  # DateFormat https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

LOCALE = 'ru'  # 'en'. Local variables https://www.localeplanet.com/icu/
if LOCALE == 'ru':
    note_string = '#Цели &#10;#Преодоление &#10;#Знания &#10;#Журнал '
    week_word = 'Неделя'
else:
    note_string = '#Goals &#10;#Achievements &#10;#Knowledge &#10;#Journal '
    week_word = 'Week'

# Don't change anything after this line
locale.setlocale(locale.LC_ALL, LOCALE)


def gcdict(file, year):  # import Google calendar file into a dictionary
    cdict = {}  # resulting dictionary
    cevent = False  # we are not in the event's block
    cevent_date = ""  # event's date string YYYYMMDD
    cevent_descr = ""  # event's description

    with open(file, "r", encoding="utf8") as f:

        line = f.readline()
        while line:  # reading calendar's file
            line = line.strip()  # cleaning the line

            if line.startswith("BEGIN:VEVENT"):  # start of the even's block
                cevent = True  # we are in
                cevent_current_year = False  # year is not defined

            if cevent and line.startswith("DTSTART;VALUE=DATE:" + str(year)):  # line with event's date and current year
                cevent_date = line.replace("DTSTART;VALUE=DATE:", "")  # selecting date's string
                cevent_date = cevent_date.strip()  # cleaning the line
                cevent_current_year = True  # the year is current

            if cevent and cevent_current_year and line.startswith("DESCRIPTION:"):  # line with event's description
                cevent_descr = line.replace("DESCRIPTION:", "")  # selecting event's description
                cevent_descr = cevent_descr.strip()  # cleaning the line

            if cevent and cevent_current_year and line.startswith("END:VEVENT"):  # end of the event's block
                cevent = False  # event is closed
                cevent_current_year = False  # year is not defined

                if cevent_date != "":  # event's date is defined
                    if cevent_date in cdict:  # date is in the dictionary
                        cdict[cevent_date] += cevent_descr + "&#10;"  # adding a line to the value
                    else:  # # date isn't in the dictionary
                        cdict[cevent_date] = cevent_descr + "&#10;"  # creating dictionary's record

            line = f.readline()  # reading the next line from the file

    return cdict  # returning the dictionary with dates and events


def daterange(s_date, e_date):  # generating dates in a range
    for n in range(int((e_date - s_date).days)):
        yield s_date + timedelta(n)  # this function returns one value at every call


start_date = date(year, 1, 1)  # the first date of our calendar
end_date = date(year + 1, 1, 1)  # the last date + 1

html = f'<?xml version="1.0"?>\n'  # OPML start
html += f'<opml version="2.0"><body>\n'

html += f'<outline text="&lt;b&gt;{start_date.strftime(display_year)}&lt;/b&gt;"/>\n'  # year's short string

if day_notes_bdays:
    cdict = gcdict(gcalendar_file, year)  # getting a dictionary with dates and events

for single_date in daterange(start_date, end_date):  # for every yaer's day

    if month_lines and single_date.day == 1:  # month's string
        html += f'<outline text="&lt;b&gt;{single_date.strftime(display_month)}&lt;/b&gt;"/>\n'

    if week_lines and single_date.isocalendar()[2] == week_day_start:  # weeks's string
        html += f'<outline text="{week_word} {single_date.isocalendar()[1]}"/>\n'

    date_string = single_date.strftime('%Y%m%d')  # date format for calendar import
    date_of_week = single_date.strftime(display_date) + ' ' + single_date.strftime("%a")  # day's string

    html += f'<outline text="&lt;'  # day's OPML code
    html += f'time '  # WF date format
    # hidden part
    html += f'startYear=&quot;{single_date.strftime("%Y")}&quot; '
    html += f'startMonth=&quot;{single_date.strftime("%m")}&quot; '
    html += f'startDay=&quot;{single_date.strftime("%d")}&quot;'
    # displayed part
    if single_date.isocalendar()[2] == 6 or single_date.isocalendar()[2] == 7:  # weekend
        html += f'&gt;&lt;span class=&quot;colored c-pink&quot;'  # pink colour
        html += f'&gt;{date_of_week}&lt;'
        html += f'/span&gt;&lt;'
    else:
        html += f'&gt;{date_of_week}&lt;'

    html += '/time&gt;"'  # WF date format end

    if day_notes:  # note block
        html += ' _note = "'
        if day_notes_bdays:  # display event from a calendar
            if date_string in cdict:  # there is an event in the dictionary at this date
                # red text from the dictionary
                html += '&lt;span class=&quot;colored c-red&quot;&gt;' + cdict[date_string] + '&lt;/span&gt;'
        html += note_string  # and a predefined text
    html += '" />\n'  # note and day's block end

html += '</body></opml>'  # OPML end

clipboard.copy(html)  # OPML code to a clipboard
