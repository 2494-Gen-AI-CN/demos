"""Connect the desk to its MySQL database."""
import os

import mysql.connector


def connect():
    """Return a connection to ticket_desk as the desk_app account."""
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="desk_app",
        password=os.environ["DESK_DB_PASSWORD"],
        database="ticket_desk",
    )
