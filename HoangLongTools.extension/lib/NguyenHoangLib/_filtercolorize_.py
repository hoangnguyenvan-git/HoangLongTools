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
# Python Libraries
import random

# Nguyen Hoang Libraries
from NguyenHoangLib._rebarutils_ import *

import clr
clr.AddReference('NguyenHoang.RBM.RebarUltils')
from NguyenHoang.RBM.RebarUltils import RebarColorizer as RCL # type: ignore
from NguyenHoang.RBM.RebarUltils import RebarFilterCreator as RFC # type: ignore

# ----------------------- GLOBAL FUNCTION -----------------------
# Colorize Rebars In Model By Selected Mode
def colorize_rebars_by_mode(window, mode, doc, view, success_color):

    window._refresh_checkpoints = sorted(random.sample(range(1, 100), 4))

    checked_rebar_data = create_value_tuple_data(window)

    if not checked_rebar_data:
        alert(None, no_rebar_alert, "WARNING")
        return

    try:
        RCL.ColorizeRebarsByMode(
        doc,
        view,
        checked_rebar_data,
        window.RebarListView.ItemsSource,
        mode,
        success_color,
        lambda pct, step, detail: update_process_bar(window, pct, step, detail)
    )
        schedule_progress_reset(window)

    except Exception as e:
        alert(None, str(e), "WARNING")

# Create Rebar Filter By Partition - ScheduleMark
def create_rebar_filter(window, doc, success_color, warning_color, fail_color):

    checked_rebar_data = create_value_tuple_data(window)

    if not checked_rebar_data:
        alert(None, no_rebar_alert, "WARNING")
        return
    
    try:
        RFC.CreateRebarFilters(
            doc,
            checked_rebar_data,
            window.RebarListView.ItemsSource,
            success_color,
            warning_color,
            fail_color,
            lambda pct, step, detail: update_process_bar(window, pct, step, detail, random=False)
        )

        schedule_progress_reset(window)

    except Exception as e:
        alert(None, str(e), "WARNING")



