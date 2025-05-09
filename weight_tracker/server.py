from flask import Flask, redirect, request
import gunicorn.app.base

from weight_tracker.analysis import day_data, days
from weight_tracker.auth import start_login, complete_login
from weight_tracker.fitbit import add_readings_to_database
from weight_tracker.google_sheet import write_google_sheet
from weight_tracker.tsv_file import write_tsv


class Server(gunicorn.app.base.BaseApplication):
    def __init__(self, port):
        self.port = port
        super().__init__()

    def load_config(self):
        self.cfg.set("bind", f"0.0.0.0:{self.port}")
        self.cfg.set("workers", 1)

    def load(self):
        return app


app = Flask(__name__)

@app.route("/")
def main():
    if request.args.get("state"):
        oauth_session, _, _ = start_login(request.args["state"])
        complete_login(oauth_session, request.url)

        add_readings_to_database(oauth_session)
        data = [day_data(day) for day in days()]

        if app.config.get("tsv_file"):
            write_tsv(app.config["tsv_file"], data)

        if app.config.get("google_sheet_url"):
            write_google_sheet(app.config["google_sheet_url"], data)

        return "OK"
    else:
        _, redirect_url, _ = start_login()
        return redirect(redirect_url)