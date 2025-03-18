# WorkFlowy-calendar-script
Creating OPML code for Workflowy.com with a calendar like set of lines

This code is an adaptation of https://github.com/guidoknoop/workflowy-calendar-generator

DISCLAIMER AND WARNINGS

Use this script at your own risk. Make backups.

Automatic creating nodes may violate some terms of use of the program.

Your WF tariff should allow adding up to 500 nodes at once.

NOW THE SCRIPT HAS:

- optional indented style;
- month lines with a small calendar and predefined note text;
- habit tracker in month lines;
- week lines (green) with predefined note text;
- day lines with predefined note text;
- native OPML date format;
- events imported from Google Calendar;
- output is translated according to the 'local' setting;
- test mode to generate 10 days only.

HOW TO USE

1. Get this Python script into your Python IDE.
2. Install libs using pip: clipboard, datetime, locale, calendar.
3. (optional) Get an .ics file from your Google Calendar. Put it in the directory with the script.
4. Set constants in the script as you prefer. Start with the constant TEST_10_DAYS = True
5. Start the script.
6. Now the OPML code is in the clipboard. Paste it into WF.

Or, if you are brave, copy/paste opml code from files: 
- WF calendar 2025.opml
- WF calendar 2026.opml 
