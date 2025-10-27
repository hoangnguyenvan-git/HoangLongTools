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
# Autodesk.Revit Libraries
from Autodesk.Revit.DB import *

# Python Libraries
import random

# Nguyen Hoang Libraries
from NguyenHoangLib._styleconfig_ import *

import clr
clr.AddReference('NguyenHoang.RBM.RebarUltils')
from NguyenHoang.RBM.RebarUltils import RebarUtils as RBU # type: ignore
clr.AddReference('NguyenHoang.RBM.ElementCollector')
from NguyenHoang.RBM.ElementCollector import ElementCollector as EC # type: ignore

# System Libraries
from System.Collections.Generic import List # type: ignore
from System import ValueTuple # type: ignore

uiapp = __revit__ # type: ignore
uidoc = uiapp.ActiveUIDocument
doc   = uidoc.Document
view  = doc.ActiveView

# ----------------------- GLOBAL FUNCTION -----------------------
# Rebar Connected From Universe
def get_all_rebar(doc):
    return RBU.GetAllRebar(doc)

def get_checked_rebar_value(window):
    return [
        (rebar_data.Partition, rebar_data.ScheduleMark)
        for rebar_data in window.RebarListView.ItemsSource
        if rebar_data.IsChecked
    ]

def get_rebars_in_models_by_checked(checked_rebars):
    value_tuple = List[ValueTuple[str, str]]()
    for item in checked_rebars:
        value_tuple.Add(ValueTuple[str, str](item[0], item[1]))
    return list(RBU.GetRebarsByChecked(doc, value_tuple))

# Create Value Tuple
def create_value_tuple_data(window):
    checked = get_checked_rebar_value(window)

    pairs = List[ValueTuple[str,str]]()
    for p,m in checked: pairs.Add(ValueTuple[str,str](p,m))
    
    return pairs

# Valid View Wonder
def is_valid_view(view):
    return view.ViewType in [
        ViewType.FloorPlan,
        ViewType.CeilingPlan,
        ViewType.EngineeringPlan,
        ViewType.Section,
        ViewType.Detail,
        ViewType.ThreeD
    ]

# Process Multiple Actions For Rebar
def process_rebar(action, window, alert_message, success_color =None, warning_color = None):
    
    if not is_valid_view(view):
        alert(window, "View hiện tại không phù hợp, hãy chọn View 3D, Floor Plan, Section.", "WARNING")
        return
    
    window._refresh_checkpoints = sorted(random.sample(range(1, 99), 3))
    
    structural_rebar_category = EC.Get_structural_rebar_category(doc)
    
    if view.GetCategoryHidden(structural_rebar_category.Id):
        alert(window, "Category: Structural Rebar Đã Bị Ẩn.", "WARNING")
        return
    
    else:
        checked_rebars_value = get_checked_rebar_value(window)
        rebars_in_models_by_checked = get_rebars_in_models_by_checked(checked_rebars_value)
        element_ids = List[ElementId]([rebar.Id for rebar in rebars_in_models_by_checked])

        if not rebars_in_models_by_checked:
            alert(window, alert_message, "WARNING")
            return
        
        total = len(rebars_in_models_by_checked) if rebars_in_models_by_checked else 1
        
        if action == "ShowOnly":
            show_element_ids = List[ElementId]([rebar.Id for rebar in rebars_in_models_by_checked])
            
            all_rebar_ids = List[ElementId]([rebar.Id for rebar in get_all_rebar(doc)])

            hide_element_ids = List[ElementId]([rebar_id for rebar_id in all_rebar_ids if rebar_id not in show_element_ids])
        else:
            pass
            
        with Transaction(doc, "{} Selected Rebars".format(action)) as t:
            t.Start()
            if action == "Hide":
                view.HideElements(element_ids)
                update_process_bar(window, 100, action, "Success",random=False)
            
            elif action == "Show":
                view.UnhideElements(element_ids)
                update_process_bar(window, 100, action, "Success", random=False)
            
            elif action == "Delete":
                for idx, rebar in enumerate(rebars_in_models_by_checked):
                    doc.Delete(rebar.Id)
                    progress = int((float(idx + 1) / float(total)) * 100)
                    update_process_bar(window, progress, action, "Rebar Number {}".format(idx + 1))

            elif action == "ShowOnly":
                view.HideElements(hide_element_ids)
                update_process_bar(window, 50, action, "Hiding")
                view.UnhideElements(show_element_ids)
                update_process_bar(window, 100, action, "Success")
            t.Commit()

            schedule_progress_reset(window)
        
        for item in window.RebarListView.ItemsSource:
            is_checked = (item.Partition, item.ScheduleMark) in checked_rebars_value

            if action == "Hide":
                if is_checked:
                    item.Message = "Cốt Thép Đã Được Ẩn"
                    item.MessageColor = warning_color
            elif action == "Show":
                if is_checked:
                    item.Message = "Cốt Thép Đã Được Hiện"
                    item.MessageColor = success_color
            elif action == "ShowOnly":
                if is_checked:
                    item.Message = "Cốt Thép Đã Được Hiện"
                    item.MessageColor = success_color
                else:
                    item.Message = "Cốt Thép Đã Được Ẩn"
                    item.MessageColor = warning_color

# -------------------------------
# Get Rebar Data
rebar_data_value = RBU.GetRebarData(doc, Black, "Chọn Calculate để tính toán cốt thép")

# Get Unit
def get_unit(doc):
    units = doc.GetUnits()
    format_options = units.GetFormatOptions(SpecTypeId.Length)
    unit_type = format_options.GetUnitTypeId()
    if unit_type == UnitTypeId.Millimeters:
        return "mm"
    elif unit_type == UnitTypeId.Meters:
        return "m"
    elif unit_type == UnitTypeId.Centimeters:
        return "cm"
    else:
        return "unknown"

# Set Unit
def set_unit(doc):
    units = doc.GetUnits()
    format_options = FormatOptions(UnitTypeId.Millimeters)
    units.SetFormatOptions(SpecTypeId.Length, format_options)
    doc.SetUnits(units)






