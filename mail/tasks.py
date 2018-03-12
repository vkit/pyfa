from __future__ import absolute_import

from pyfactory19.celery import app

from .utils import send_emails
from celery import shared_task


@app.task
def mailer():
    return send_emails(to=['emiamar@gmail.com'])


@app.task
def add():
    return "OK"
