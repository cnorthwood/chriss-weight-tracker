Chris's weight tracker
======================

Getting started
---------------

You will need Docker installed, and then run `./setup` to set it up locally. You will only need
to do this once, and then re-run it again on every update.

You will also need to create a "personal" application at https://dev.fitbit.com/apps/new. Make sure
the redirect URL is set to `https://localhost:3000`, and make a note of your "OAuth 2.0 Client ID"
and "Client Secret", you will need those in a moment.

Run `FITBIT_CLIENT_ID=<client ID from above> FITBIT_CLIENT_SECRET=<client secret from above> ./weight-tracker` to run the script.

License
-------

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not,
see <https://www.gnu.org/licenses/>. 
