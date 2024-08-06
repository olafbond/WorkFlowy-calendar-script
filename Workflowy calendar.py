import clipboard
from datetime import timedelta, date
import locale

# --------------
# Settings
# --------------
LOCALE = 'ru'  # 'en'. Local variables https://www.localeplanet.com/icu/

YEAR = 2025  # Calendar's date
YEAR_LINE = True  # Add months lines inline

MONTH_LINES = True  # Add months lines inline

WEEK_LINES = False  # Add week lines inline
WEEK_DAY_START = 1  # 1 - Monday, ... 7 - Sunday
if LOCALE == 'ru':
    WEEK_WORD = 'Неделя'
else:
    WEEK_WORD = 'Week'

DAY_NOTES_BDAYS = True  # Add BDays from Google calendar's export file
GOOGLE_CALENDAR_FILE = "addressbook#contacts@group.v.calendar.google.com.ics"  # Google Calendar export file

DAY_NOTES = True  # Add notes for journaling
NOTE_HEADERS = ('#Цели дня', '#Спорт, подвижность', '#Чтение дня', '#Новое знание', '#Преодоление дня', '#Вперед движение', '#Позитив, благодарности', '#Вопросы обдумать', '#Журнал, мысли')

DISPLAY_YEAR_STR = '__.__.%y'  # DateFormat https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
DISPLAY_MONTH_STR = '__.%m.%y'

# -------------------------------------
# Don't change anything after this line
# -------------------------------------
locale.setlocale(locale.LC_ALL, LOCALE)

def color_string(text, color):
    return f'&lt;span class=&quot;colored {color}&quot;&gt;{text}&lt;/span&gt;'


def date_OPML(date):
    date_OPML_str = f'&lt;time startYear=&quot;{date.strftime("%Y")}&quot; '
    date_OPML_str += f'startMonth=&quot;{date.strftime("%m")}&quot; '
    date_OPML_str += f'startDay=&quot;{date.strftime("%d")}&quot;'
    date_OPML_str += f'&gt;WWW, MMM DD, YYYY&lt;/time&gt; '
    return date_OPML_str


def note_text(tags):
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


def date_range(s_date, e_date):  # generating dates in a range
    for n in range(int((e_date - s_date).days)):
        yield s_date + timedelta(n)  # this function returns one value at every call


start_date = date(YEAR, 1, 1)  # the first date of our calendar
end_date = date(YEAR + 1, 1, 1)  # the last date + 1
end_date = date(YEAR, 1, 10)  # the last date + 1

html = f'<?xml version="1.0"?>\n'  # OPML start
html += f'<opml version="2.0"><body>\n'

if YEAR_LINE:
    html += f'<outline text="&lt;b&gt;{start_date.strftime(DISPLAY_YEAR_STR)}&lt;/b&gt;"/>\n'  # year's line

if DAY_NOTES_BDAYS:
    cdict = google_calendar_dict(GOOGLE_CALENDAR_FILE, YEAR)  # getting a dictionary with dates and events

for single_date in date_range(start_date, end_date):  # for every year's day

    if MONTH_LINES and single_date.day == 1:  # month's line
        html += f'<outline text="&lt;b&gt;{single_date.strftime(DISPLAY_MONTH_STR)}&lt;/b&gt;"/>\n'

    if WEEK_LINES and single_date.isocalendar()[2] == WEEK_DAY_START:  # weeks's line
        html += f'<outline text="{WEEK_WORD} {single_date.isocalendar()[1]}"/>\n'

    html += f'<outline text="'  # day's OPML code
    html += date_OPML(single_date)  # OPML date's representation
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

        html += note_text(NOTE_HEADERS)  # and the predefined text lines

    html += '" />\n'  # note and day's block end

html += '</body></opml>'  # OPML end

clipboard.copy(html)  # copying OPML code to the clipboard
print('OPML code is in the clipboard. Paste it into WF.')
