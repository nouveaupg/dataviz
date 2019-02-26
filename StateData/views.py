# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from models import AppealReceiptsData, load_data_from_csv_file

from django.shortcuts import render

# Create your views here.


def index(request):
    years = []
    state_names = []
    all_objects = AppealReceiptsData.objects.all()
    if all_objects.count() == 0:
        load_data_from_csv_file()
        all_objects = AppealReceiptsData.objects.all()

    for each_object in all_objects:
        if each_object.year not in years:
            years.append(each_object.year)
        if each_object.state_name not in state_names:
            state_names.append(each_object.state_name)

    selected_state_name = None
    selected_year = None
    active_control = None

    if "state_menu" in request.GET:
        selected_state_name = request.GET["state_menu"]
    if "year_menu" in request.GET:
        selected_year = int(request.GET["year_menu"])

    if "active_control" in request.GET:
        active_control = request.GET["active_control"]
    elif selected_state_name is None and selected_year is None:
        selected_state_name = state_names[0]
        active_control = "state"

    selected_objects = []  # I think this is way faster than going back to the DB
    first = None
    sorted_objects = None
    sorted_states = None
    if active_control == "state":
        for each in all_objects:
            if each.state_name == selected_state_name:
                if first is None:
                    first = each.year
                selected_objects.append((each.year, each.total_appeal_receipts))
    elif active_control == "year":
        unsorted_objects = []
        sorted_states = []
        for each in all_objects:
            if each.year == selected_year:
                unsorted_objects.append((each.state_name, each.total_appeal_receipts))
        sorted_objects = sorted(unsorted_objects, key=lambda obj: obj[1], reverse=True)[:30]  # lol merge sort?
        for each in sorted_objects:
            sorted_states.append(each[0])
            selected_objects.append(each[1])

    return render(request, "main.html", context={"years": years,
                                                 "state_names": state_names,
                                                 "metrics": selected_objects,
                                                 "selected_state": selected_state_name,
                                                 "selected_year": selected_year,
                                                 "sorted_objects": sorted_objects,
                                                 "sorted_states": sorted_states,
                                                 "first": first,
                                                 "active_control": active_control})
