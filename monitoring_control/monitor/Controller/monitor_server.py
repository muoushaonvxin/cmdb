# -*- encoding: utf-8 -*-
import sys
import os
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monitoring_control.settings")
from monitoring_control import settings

from monitor.models import *
from . import data_processing

if __name__ == '__main__':
    reactor = data_processing.DataHandler()
    reactor.looping()