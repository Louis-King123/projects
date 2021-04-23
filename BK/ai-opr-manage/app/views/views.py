from datetime import datetime

from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from app.jobs.report.resource_metrice import resouce_metric_work
from app.jobs.report.resource_set import resouce_set_work
from app.utils.util_oracle_execute_sql import OracleExecuteSQL


def index(request):
    return render(request, "index.html")


def test(request):
    # resouce_set_work()
    # resouce_metric_work()
    # sql = """select * from ITEST."user_1";"""
    # oracle_execute_sql = OracleExecuteSQL()
    # data = oracle_execute_sql.fetchall_to_dict(sql)
    # print(data)

    return JsonResponse({"status":"success"})
