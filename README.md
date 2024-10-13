# WorkFlowy-calendar-script
Creating OPML code for Workflowy.com with a calendar like set of lines

This code is an adaptation of https://github.com/guidoknoop/workflowy-calendar-generator

DISCLAIMER AND WARNINGS

Use this script at your own risk. Make backups.

Automatic creating nodes may violate some terms of use of the program.

Your WF tariff should allow adding up to 500 nodes at once.

NOW THE SCRIPT HAS:

- month lines with a small calendar and predefined note text;
- week lines with predefined note text;
- day lines with predefined note text;
- day lines could be indented form a month line;
- native OPML date format;
- events imported from Google Calendar;
- output is translated according to the 'local' setting;
- test mode to generate 10 days only.

HOW TO USE

1. Get this Python script into your Python IDE.
2. (optional) Get an .ics file from your Google Calendar. Put it in the directory with the script.
3. Set constants in the script as you prefer. Start with the constant TEST_10_DAYS = True
4. Start the script.
5. Now the OPML code is in the clipboard. Paste it into WF.
