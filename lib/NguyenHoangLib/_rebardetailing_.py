# ----------------------- UNICODE STYLE -------------------------
# -*- coding: utf-8 -*-

# ======================= CREATED BY ============================
# ╔═╗ ╔╗╔═══╗╔╗ ╔╗╔╗  ╔╗╔═══╗╔═╗ ╔╗    ╔╗ ╔╗╔═══╗╔═══╗╔═╗ ╔╗╔═══╗
# ║║╚╗║║║╔═╗║║║ ║║║╚╗╔╝║║╔══╝║║╚╗║║    ║║ ║║║╔═╗║║╔═╗║║║╚╗║║║╔═╗║
# ║╔╗╚╝║║║ ╚╝║║ ║║╚╗╚╝╔╝║╚══╗║╔╗╚╝║    ║╚═╝║║║ ║║║║ ║║║╔╗╚╝║║║ ╚╝
# ║║╚╗║║║║╔═╗║║ ║║ ╚╗╔╝ ║╔══╝║║╚╗║║    ║╔═╗║║║ ║║║╚═╝║║║╚╗║║║║╔═╗
# ║║ ║║║║╚╩═║║╚═╝║  ║║  ║╚══╗║║ ║║║    ║║ ║║║╚═╝║║╔═╗║║║ ║║║║╚╩═║
# ╚╝ ╚═╝╚═══╝╚═══╝  ╚╝  ╚═══╝╚╝ ╚═╝    ╚╝ ╚╝╚═══╝╚╝ ╚╝╚╝ ╚═╝╚═══╝
# ===============================================================

# ----------------------- IMPORT LIBRARY ------------------------
# Nguyen Hoang Libraries
from NguyenHoangLib._rebarutils_ import create_value_tuple_data
from NguyenHoangLib._styleconfig_ import *

import clr
clr.AddReference('NguyenHoang.RBM.RebarDetailing')
from NguyenHoang.RBM.RebarDetailing import RebarDetailing as RD # type: ignore

# ----------------------- GLOBAL FUNCTION -----------------------
# Rebar Detail Runner
def rebar_detail_runner(doc, window):

    checked_rebar_data = create_value_tuple_data(window)

    if not checked_rebar_data:
        return
    
    try:
        RD.RebarDetailingRunner.RunAll(
            doc,
            checked_rebar_data,
            window.RebarListView.ItemsSource,
            DarkGreen,
            lambda pct, part, mark: update_process_bar(window, pct, "Export Detail " + part, mark, random=False)
        )
    except Exception as e:
        alert(None, str(e), "WARNING")

# Delete Detail Rebar
def delete_rebar_detail(window, doc, alert_message, success_color, fail_color):

    checked_rebar_data = create_value_tuple_data(window)

    if not checked_rebar_data:
        alert(None, alert_message, "WARNING")
        return
    
    try:
        RD.RebarDetailingRunner.DeleteDetails(
            doc, 
            checked_rebar_data, 
            window.RebarListView.ItemsSource,
            success_color, fail_color,
            lambda pct, part, mark: update_process_bar(window, pct, part, mark, random=False)
        )
    except Exception as e:
        alert(None, str(e), "WARNING")

# Rotate Rebar Detail By Angles
def rotate_rebar_detail_by_angle(window, doc, angle, rotate_mode, success_color, fail_color):

    checked_rebar_data = create_value_tuple_data(window)

    if not checked_rebar_data:
        alert(None, no_rebar_alert, "WARNING")
        return
    
    try:
        RD.RebarDetailingRunner.RotateDetails(
            doc, 
            checked_rebar_data, 
            window.RebarListView.ItemsSource,
            angle,
            rotate_mode,
            success_color, 
            fail_color,
            lambda pct, part, mark: update_process_bar(window, pct, part, mark, random=False)
        )
    except Exception as e:
        alert(None, str(e), "WARNING")


# Scale Rebar Detail By Length
def scale_rebar_detail_by_length(window, doc, length, axis_mode, success_color, fail_color):

    checked_rebar_data = create_value_tuple_data(window)

    if not checked_rebar_data:
        alert(None, no_rebar_alert, "WARNING")
        return

    try:
        RD.RebarDetailingRunner.ScaleDetails(
            doc, 
            checked_rebar_data, 
            window.RebarListView.ItemsSource,
            length,
            axis_mode,
            success_color, 
            fail_color,
            lambda pct, part, mark: update_process_bar(window, pct, part, mark, random=False)
        )
    except Exception as e:
        alert(None, str(e), "WARNING")

def scale_rebar_detail_by_factor(window, doc, scale_factor, success_color, fail_color):

    checked_rebar_data = create_value_tuple_data(window)

    if not checked_rebar_data:
        alert(None, no_rebar_alert, "WARNING")
        return

    try:
        RD.RebarDetailingRunner.ScaleDetailsByFactor(
            doc, 
            checked_rebar_data, 
            window.RebarListView.ItemsSource,
            scale_factor,
            success_color, 
            fail_color,
            lambda pct, part, mark: update_process_bar(window, pct, part, mark, random=False)
        )
    except Exception as e:
        alert(None, str(e), "WARNING")