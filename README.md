# nyuad-2017-directory
HTML page for NYU AD hackathon directory

### To build the site
You need to
- grab the CVS file from the Google Spreadsheet
- run the following Python code: `python generate_directory.py  > directory.html`. This will create an HTML file.

### To make changes to the output
The HTML is generated from the CSV data and from a Jija template.
To make changes to the output, you can:
- add new variables into the `USERS` variables
- use these variables in your Jinja2 template

### Issues with pictures
Some people provided links to pictures that cannot be embedded into an HTML page.
The easiest way is to download them manually into Google Drive and serve them from there.
