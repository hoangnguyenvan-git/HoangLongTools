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
clr.AddReference('NguyenHoang.RBM.RebarCalculation')
from NguyenHoang.RBM.RebarCalculation import RebarCalculator as RC # type: ignore
from NguyenHoang.RBM.RebarCalculation import ScheduleHelper as SH # type: ignore

# ----------------------- GLOBAL FUNCTION -----------------------
# Rebar Calculation   
def calculate_rebar_runner(doc, window, trans_equal):
    checked_rebar_data = create_value_tuple_data(window)

    if not checked_rebar_data:
        alert(None, no_rebar_alert, "WARNING")
        return
    
    try:
        RC.RebarCalculationRunner.RunAll(
            doc,
            checked_rebar_data,
            window.RebarListView.ItemsSource,
            DarkGreen,
            lambda pct, step, detail:
        update_process_bar(window, pct, step, detail, random=False),
            trans_equal
        )
    except Exception as e:
        alert(None, str(e), "WARNING")


# Create Schedule For Structural Rebar
def create_schedule_rebar(doc, window):
    try:
        SH.CopyAllRebarSchedulesFromTemplate(
            doc,
            lambda pct, step, detail: 
            update_process_bar(window, pct, step, detail, random=False))
    except Exception as e:
        alert(None, str(e), "WARNING")