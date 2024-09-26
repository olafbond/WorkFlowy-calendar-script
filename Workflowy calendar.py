import clipboard
from datetime import date, datetime, timedelta
import locale, calendar

# --------------
# Settings
# --------------
TEST_10_DAYS = True  # generate 10 days only for tests

LOCALE = 'fr'  # 'en', 'de'... Local variables https://www.localeplanet.com/icu/

YEAR = 2025  # Calendar's year
YEAR_LINE = True  # Add a year's line
DISPLAY_YEAR_STR = '%Y'  # DateFormat https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

MONTH_LINES = True  # Add months lines inline
DISPLAY_MONTH_STR = '%B'
MONTH_NOTE = True  # Add a small calendar in a month line's note field

WEEK_LINES = False  # Add week lines inline
WEEK_WORD = '*******'
WEEK_DAY_START = 1  # 1 - Monday, ... 7 - Sunday

DAY_LINES = True
WEEK_DAYS_NAMES = True  # Add a short week day's name
DAY_NOTES_BDAYS = True  # Add BDays from Google calendar's export file
GOOGLE_CALENDAR_FILE = "addressbook#contacts@group.v.calendar.google.com.ics"  # Google Calendar export file
DAY_NOTES = True  # Add notes for journaling
NOTE_HEADERS = ('#Цели', '#Подвижность', '#Чтение', '#Знание', '#Преодоление', '#Вперед', '#Позитив', '#Вопросы', '#Журнал')

# -------------------------------------
# Don't change anything after this line
# -------------------------------------
locale.setlocale(locale.LC_ALL, LOCALE)


def color_string(text, color):  # OPML formatted text with color
    return f'&lt;span class=&quot;colored {color}&quot;&gt;{text}&lt;/span&gt;'


def date_OPML(date):  # OPML date
    date_OPML_str = f'&lt;time startYear=&quot;{date.strftime("%Y")}&quot; '
    date_OPML_str += f'startMonth=&quot;{date.strftime("%m")}&quot; '
    date_OPML_str += f'startDay=&quot;{date.strftime("%d")}&quot;'
    date_OPML_str += f'&gt;WWW, MMM DD, YYYY&lt;/time&gt; '
    return date_OPML_str


def get_weekday_names():  # line of local weekdays' names
    first_day = calendar.firstweekday()  # local first week's day 0 - monday, 6 - sunday
    today = date.today()  # current date for reference
    delta = (today.weekday() - first_day) % 7  # calculating days to the nearest week start
    first_weekday = today - timedelta(days=delta)  # the nearest week start

    days = [first_weekday + timedelta(days=i) for i in range(7)]  # set of 7 week's days
    short_names = [day.strftime("%a") for day in days]  # set of short names

    return '&#9;'.join(short_names)  # combining names in a line with tabs


def month_note_text(date, lang):  # a small calendar for a month
    year = date.year  # getting a year and a month
    month = date.month

    header = '" _note="' + get_weekday_names()  # the first line of a note

    cal = calendar.Calendar(firstweekday=calendar.firstweekday())  # setting the calendar
    days = cal.monthdayscalendar(year, month)  # getting weeks of the month

    calendar_lines = []  # creating lines for days
    for week in days:
        week_line = '&#9;'.join(str(day) if day != 0 else '' for day in week)
        calendar_lines.append(week_line)

    return header + '&#10;' + '&#10;'.join(calendar_lines) + '" ' # joining the header and the calendar lines


def day_note_text(tags):  # tags for journaling
    note_tags_string = ''
    for tag in tags:
        note_tags_string += f'{color_string(tag + ".", "bc-gray")} &#10;'
    return note_tags_string


def google_calendar_dict(file, year):  # import Google calendar file into a dictionary
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


def date_range(s_date, e_date):  # returns dates in a range
    for n in range(int((e_date - s_date).days)):
        yield s_date + timedelta(n)  # this function returns one value at every call


start_date = date(YEAR, 1, 1)  # the first date of our calendar
if TEST_10_DAYS:  # generate 10 days only for tests
    end_date = date(YEAR, 1, 11)  # till Jan 10
else:  # generate the whole year
    end_date = date(YEAR + 1, 1, 1)  # the year end + 1

html = f'<?xml version="1.0"?>\n'  # OPML start lines
html += f'<opml version="2.0"><body>\n'

if YEAR_LINE:  # year's line
    html += f'<outline text="&lt;b&gt;{start_date.strftime(DISPLAY_YEAR_STR)}&lt;/b&gt;"/>\n'

if DAY_NOTES_BDAYS:  # getting a dictionary with dates and events
    cdict = google_calendar_dict(GOOGLE_CALENDAR_FILE, YEAR)

for single_date in date_range(start_date, end_date):  # for every year's day

    if MONTH_LINES and single_date.day == 1:  # month's line
        html += f'<outline text="&lt;b&gt;{single_date.strftime(DISPLAY_MONTH_STR)}&lt;/b&gt;'
        if MONTH_NOTE:
            html += month_note_text(single_date, LOCALE)  # add a calendar for the month
        html += '/>\n'

    if WEEK_LINES and single_date.isocalendar()[2] == WEEK_DAY_START:  # weeks's line
        html += f'<outline text="{WEEK_WORD} {single_date.isocalendar()[1]}"/>\n'  # with the week's number

    if DAY_LINES:
        html += f'<outline text="'  # day's OPML code
        html += date_OPML(single_date)  # OPML date's representation
        if WEEK_DAYS_NAMES:  # Add a short week day's name
            if single_date.isocalendar()[2] == 6 or single_date.isocalendar()[2] == 7:  # weekend
                html += color_string(single_date.strftime("%a"), 'c-pink')  # colored weekend
            else:
                html += single_date.strftime("%a")

        if DAY_NOTES:  # note block
            html += '" _note="'
            if DAY_NOTES_BDAYS:  # display event from a calendar
                date_string = single_date.strftime('%Y%m%d')  # date in a format for calendar import
                if date_string in cdict:  # there is an event in the dictionary at this date
                    html += color_string(cdict[date_string], 'c-red')  # BDays in red

            html += day_note_text(NOTE_HEADERS)  # and the predefined text lines

        html += '" />\n'  # note and day's block end

html += '</body></opml>'  # OPML end

clipboard.copy(html)  # copying OPML code to the clipboard
print('OPML code is in the clipboard. Paste it into WF.')
