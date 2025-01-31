Chris's weight tracker
======================

Getting started
---------------

You will need Python and Poetry installed, then run `poetry install`.

You will need to create a "personal" application at https://dev.fitbit.com/apps/new. Make sure
the redirect URL is set to `https://localhost:3000`, and make a note of your "OAuth 2.0 Client ID"
and "Client Secret", you will need those in a moment.

To login, run `FITBIT_DATABASE=fitbit.sqlite FITBIT_CLIENT_ID=<client ID from above> FITBIT_CLIENT_SECRET=<client secret from above> poetry run python3 -mweight_tracker --login`.
You will be given a URL to visit, which will then authorise the script. You will then be redirected to a localhost URL,
but will get a "connection refused" error. This is fine, what you want is the URL in your address bar to copy and paste
into the app.

Once you have logged in, you can write the output to a tsv file, `FITBIT_DATABASE=fitbit.sqlite FITBIT_CLIENT_ID=<client ID from above> FITBIT_CLIENT_SECRET=<client secret from above> HEIGHT=<your height in cm> poetry run python3 -mweight_tracker --tsv-file Weight_Tracker.tsv`.
Your outputs are now in `Weight_Tracker.tsv`, you can copy/paste this into a Google Sheet, e.g., `pbcopy < Weight_Tracker.tsv`.
I use a Google Sheet because it has some conditional formatting on it (e.g., I use colour coding for if I'm
tracking the direction I'd like to go or not) and then I can plot some charts etc in it.

It stores the values into a `fitbit.sqlite` database so it only fetches new ones from Fitbit (and also means the first
row in your data is consistent, so you can keep copy/pasting in the top corner of a Google Sheet you use to add to it).

The data it outputs is the data I like to track - which importantly includes a 7-day moving average so I can
weigh daily but get some cleaner data to track my progress. I [wrote a blog post about how I track my weight](https://cnorthwood.medium.com/tracking-losing-weight-78eadc616507)
which gives a bit of rationale.

You can also have this write directly to the Google Sheet if you'd like. To do this, first create a Google service account:

1. Open https://console.developers.google.com/apis/library and find sheets. Make sure it's enabled, and if necessary, create a project.
2. Under the IAM admin in the Google Cloud console, create a service account. You can leave everything as default.
3. Make a note of the service account email, and share your Google Sheet with this email account.
4. On the service account screen, create a key and download it in JSON form.

Now you can run the command `FITBIT_DATABASE=fitbit.sqlite FITBIT_CLIENT_ID=<client ID from above> FITBIT_CLIENT_SECRET=<client secret from above> GOOGLE_SERVICE_ACCOUNT=service-account.json HEIGHT=<your height in cm> poetry run python3 -mweight_tracker --google-sheet <sheet URL>`

Deploying to k8s
----------------

TODO

License
-------

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not,
see <https://www.gnu.org/licenses/>. 
