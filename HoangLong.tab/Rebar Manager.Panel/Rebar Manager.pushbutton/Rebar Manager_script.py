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
# pyRevit Libraries
from pyrevit import forms

# Autodesk.Revit Libraries
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.UI import UIApplication

# Nguyen Hoang Libraries
from NguyenHoangLib._rebarutils_ import *
from NguyenHoangLib._rebardetailing_ import *
from NguyenHoangLib._calculation_ import *
from NguyenHoangLib._filtercolorize_ import *

import clr
clr.AddReference('NguyenHoang.RBM.Login')
from NguyenHoang.RBM.Login import AuthSession # type: ignore
clr.AddReference('NguyenHoang.RBM.Constant')
from NguyenHoang.RBM.Constant import SettingWindow # type: ignore
clr.AddReference('NguyenHoang.RBM.RebarUltils')
from NguyenHoang.RBM.RebarUltils import RebarUtils as RBU # type: ignore

# System Libraries
from System.Windows.Data import CollectionViewSource, PropertyGroupDescription # type: ignore
from System.Windows import WindowState # type: ignore
from System.Windows.Input import MouseButtonState # type: ignore

# ----------------------- MAIN CODE -----------------------
# RebarWindow WPF
class RebarWindow(forms.WPFWindow):
    def __init__(self, xaml_file):
        forms.WPFWindow.__init__(self, xaml_file)
        self.collection_view_source = None
        self.RebarListView.ItemsSource = []
        self.Resources["MyNasalFont"] = nasal_font

    # -------------------------------
    # Populate Data
    def populate_data(self, data):
        self.original_data = data
        self.collection_view_source = CollectionViewSource()
        self.collection_view_source.Source = data
        self.collection_view_source.GroupDescriptions.Add(PropertyGroupDescription("Partition"))
        self.RebarListView.ItemsSource = self.collection_view_source.View

    def refresh_list(self):
        if self.collection_view_source:
            self.collection_view_source.View.Refresh()

    # -------------------------------
    # Window Button Handler   
    def CloseButton_Click(self, sender, args):
        self.Close()

    def MaximizeRestoreButton_Click(self, sender, args):
        if self.WindowState == WindowState.Maximized:
            self.WindowState = WindowState.Normal
        else:
            self.WindowState = WindowState.Maximized

    def MinimizeButton_Click(self, sender, args):
        self.WindowState = WindowState.Minimized

    def Window_MouseLeftButtonDown(self, sender, args):
        if args.ButtonState == MouseButtonState.Pressed:
            self.DragMove()

    # -------------------------------
    # Shape Option Combobox
    def ShapeOption_SelectionChanged(self, sender, args):
        try:
            combo = sender
            selected_value = combo.SelectedValue
            selected_items = self.RebarListView.SelectedItems

            if selected_value is None or not selected_items:
                return

            for item in selected_items:
                item.SelectedShapeOption = selected_value

            self.refresh_list()
        except Exception as e:
            print("ShapeOption_SelectionChanged error:", str(e))

    # -------------------------------
    # User Check In
    def User_Button_Click(self, sender, args):
        try:
            if not AuthSession.EnsureAuthenticated(True):
                return
        except Exception as e:
            print(str(e))

    # -------------------------------
    # On Search Textbox
    def OnSearchTextChanged(self, sender, args):
        try:
            search_text = sender.Text.lower().strip()
            current_length = len(search_text)
            
            # Initialize tracking variables
            if not hasattr(self, 'last_length'):
                self.last_length = 0
            if not hasattr(self, 'last_search_text'):
                self.last_search_text = ""
                
            # Skip if same search
            if search_text == self.last_search_text:
                return
            
            # Detect backspacing
            is_backspacing = current_length < self.last_length
            self.last_length = current_length
            self.last_search_text = search_text
            
            if search_text in ["", "search here please..."]:
                self.collection_view_source.View.Filter = None
            else:
                if is_backspacing:
                    filtered_items = []
                    all_items = list(self.collection_view_source.Source)
                    
                    for item in all_items:
                        if (search_text in (item.ScheduleMark or "").lower() or
                            search_text in (item.Partition or "").lower() or
                            search_text in str(item.Diameter or "").lower()):
                            filtered_items.append(item)
                            
                            if len(filtered_items) >= 50:
                                break
                    
                    filtered_set = set(filtered_items)
                    def limited_filter(item):
                        return item in filtered_set
                    
                    self.collection_view_source.View.Filter = limited_filter
                else:
                    def filter_function(item):
                        return (search_text in (item.ScheduleMark or "").lower() or
                                search_text in (item.Partition or "").lower() or
                                search_text in str(item.Diameter or "").lower())
                    
                    self.collection_view_source.View.Filter = filter_function

            self.collection_view_source.View.Refresh()

        except Exception as e:
            alert(self, "Error in OnSearchTextChanged: {0}".format(e), "WARNING")
 
    def SearchTextBox_GotFocus(self, sender, args):
        if sender.Text == "Search here please...":
            sender.Text = ""
            sender.Foreground = Black

    def SearchTextBox_LostFocus(self, sender, args):
        if not sender.Text.strip():
            sender.Text = "Search here please..."
            sender.Foreground = LightOrange    

    # -------------------------------
    # Group Type Combobox Handler
    def GroupTypeCbx_SelectionChanged(self, sender, args):
        selected_item = sender.SelectedItem
        if selected_item and hasattr(selected_item, "Content"):
            content_text = selected_item.Content.Text.strip()

            group_map = {
                "Group By Partition": "Partition",
                "Group By Diameter": "Diameter",
                "Group By Rebar Shape": "RebarShape"
            }

            selected_type = group_map.get(content_text, None)

            if selected_type:
                self.collection_view_source.GroupDescriptions.Clear()
                self.collection_view_source.GroupDescriptions.Add(PropertyGroupDescription(selected_type))

    # -------------------------------
    # Multiple Checkbox Click
    def CheckBox_Click(self, sender, args):
        new_value = sender.IsChecked
        selected_items = self.RebarListView.SelectedItems
        for item in selected_items:
            item.IsChecked = new_value
        self.refresh_list()

    # -------------------------------
    # Check All/None Button Click
    def All_None_Button_Click(self, sender, args):
        for rebar_data in self.collection_view_source.Source:
            if not rebar_data.IsChecked:
                rebar_data.IsChecked = True
            else:
                rebar_data.IsChecked = False
        self.refresh_list()
    
    # -------------------------------
    # Show Button
    def Show_Button_Click(self, sender, args):
        process_rebar("Show",self, no_rebar_alert, DarkGreen, DeepOrange)
        self.refresh_list()

    # -------------------------------
    # Hide Button
    def Hide_Button_Click(self, sender, args):
        process_rebar("Hide",self, no_rebar_alert, DarkGreen, DeepOrange)
        self.refresh_list()

    # -------------------------------
    # Show Only Button
    def ShowOnly_Button_Click(self, sender, args):
        process_rebar("ShowOnly",self, no_rebar_alert, DarkGreen, DeepOrange)
        self.refresh_list()
        
    # -------------------------------
    # Filter Button
    def Create_Filters_Button_Click(self, sender, args):
        create_rebar_filter(self, doc, DarkGreen, DeepOrange, Red)
        self.refresh_list()

    # -------------------------------
    # Colorize Combobox Handler
    def Combobox_GotFocus(self, sender, args):
        if self.selected_index > 0 :
            sender.SelectedIndex = self.selected_index
        else:
            sender.SelectedIndex = -1

    def Combobox_LostFocus(self,sender, args):
        if sender.SelectedIndex > 0:
            self.selected_index = sender.SelectedIndex

    def ColorizeCbx_SelectionChanged(self, sender, args):
        selected_item = sender.SelectedItem
        if selected_item and hasattr(selected_item, "Content"):
            content_text = selected_item.Content.Text

            group_map = {
                "Colorize": "Colorize",
                "ByPartition": "Partition",
                "ByScheduleMark": "Schedule Mark",
                "ByVariation": "05. HL_Ghi chú cốt thép",
                "ResetColor": "Reset Color"
            }

            self.selected_mode = group_map.get(content_text,None)
            self.selected_mode_name = content_text

    def Apply_Color_Button_Click(self, sender, args):
        if self.selected_mode != "Colorize":
            if self.selected_mode == "05. HL_Ghi chú cốt thép":
                self.Calculate_Button_Click(sender, args, reset=False)

                colorize_rebars_by_mode(self, self.selected_mode, doc, view, DarkGreen)
            else:
                colorize_rebars_by_mode(self, self.selected_mode, doc, view, DarkGreen)
        else:
            alert(self, "Chọn Color Mode trong Combobox trước tiên.", "WARNING")
        
        self.refresh_list()

    # -------------------------------
    # Calculate Button
    def Calculate_Button_Click(self, sender, args, reset = True):
        calculate_rebar_runner(doc, self, 0)
        self.refresh_list()
        if reset:
            schedule_progress_reset(self)

    # -------------------------------
    # Bending Detail Button Click
    def Bending_Detail_Button_Click(self, sender, args):
        try:
            # Calculate Before Export Bending  Detail
            calculate_rebar_runner(doc, self, 5)
            self.refresh_list()
            rebar_detail_runner(doc, self, uiapp)
            self.refresh_list()
            schedule_progress_reset(self)
        except Exception as e:
            print(" Crash in run():", str(e))
    
    # -------------------------------
    # Detail Setting Button Click
    def Detail_Setting_Button_Click(self, sender, args):
        try:
            win = SettingWindow(self)
            win.Show()
        except Exception as e:
            print(str(e))

    # -------------------------------
    # Detail Setting Button Click
    def Create_Schedule_Button_Click(self, sender, args):
        try:
            create_schedule_rebar(doc,self)
            schedule_progress_reset(self)
        except Exception as e:
            print(str(e))

    # -------------------------------
    # Delete Bending Detail Button Click
    def Delete_Rebar_Detail_Button_Click(self, sender, args):
        delete_rebar_detail(self, doc, no_rebar_alert, DarkGreen, Red)
        self.refresh_list()
        schedule_progress_reset(self)
            
    # -------------------------------
    # Delete Button Click   
    def Delete_Rebar_Button_Click(self, sender, args):
        process_rebar("Delete",self, no_rebar_alert)
        updated_rebar_data = RBU.GetRebarData(doc, Black, "Chọn Calculate để tính toán cốt thép")
        self.populate_data(updated_rebar_data)
    
    # -------------------------------
    # Rotate Detail Button Click
    def Rotate_Angle_GotFocus(self, sender, args):
        if sender.Text == "- 90° -":
            sender.Text = ""
            sender.Foreground = DeepBlue
        else:
            sender.Foreground = DeepBlue

    def Rotate_Angle_LostFocus(self, sender, args):
        if not sender.Text.strip():
            sender.Text = "- 90° -"
            sender.Foreground = DeepBlue

    def Rotate_Angle_TextChanged(self, sender, args):
        text = sender.Text.strip()
        self.angle_text = text
        
        if text == "" or text == "- 90° -":
            self.angle = None
            return
        
        if text == "-" or text == "+" or text == ".":
            self.angle = None
            return
        
        if text in ["-.", "+."]:
            self.angle = None
            return
        
        try:
            angle = float(text)
            if not (-360 <= angle <= 360):
                alert(self, "Góc xoay phải nằm trong khoảng -360° đến 360°", "WARNING")
                self.angle = None
                return
            self.angle = angle
        except ValueError:
            alert(self, "Giá trị góc không hợp lệ", "WARNING")
            self.angle = None

    def Rotate_Angle_Button_Click(self, sender, args):
        if self.angle is None:
            alert(self, "Chọn góc xoay hợp lệ trước khi thực hiện", "WARNING")
            return
        
        rotate_rebar_detail_by_angle(self, doc, self.angle, 0, DarkGreen, Red)
        self.refresh_list()
        schedule_progress_reset(self)

    def Auto_Rotate_X_Button_Click(self, sender, args):
        rotate_rebar_detail_by_angle(self, doc, 0, 1, DarkGreen, Red)
        
        self.refresh_list()

        schedule_progress_reset(self)

    def Auto_Rotate_Y_Button_Click(self, sender, args):
        rotate_rebar_detail_by_angle(self, doc, 0, 2, DarkGreen, Red)
        
        self.refresh_list()

        schedule_progress_reset(self)

    # -------------------------------
    # Scaling Detail Button Click
    def Scale_Detail_GotFocus(self, sender, args):
        if sender.Text == "- 2x -":
            sender.Text = ""
            sender.Foreground = DeepBlue
        else:
            sender.Foreground = DeepBlue
    
    def Scale_Detail_LostFocus(self, sender, args): 
        if not sender.Text.strip():
            sender.Text = "- 2x -"
            sender.Foreground = DeepBlue

    def Scale_Detail_TextChanged(self, sender, args):
        text = sender.Text.strip()
        self.scale_text = text
        
        if text == "" or text == "- 2x -":
            self.scale = None
            return
        
        if len(text) == 1 and text in ["-", "+", "."]:
            self.scale = None
            return
        
        if text in ["-.", "+."]:
            self.scale = None
            return
        
        try:
            scale = float(text)
            self.scale = scale
        except ValueError:
            alert(self, "Giá trị không hợp lệ", "WARNING")
            self.scale = None

    def Scale_Detail_Button_Click(self, sender, args):
        if self.scale is None:
            alert(self, "Nhập thông số hợp lệ trước khi thực hiện", "WARNING")
            return
        
        scale_rebar_detail_by_factor(self, doc, self.scale, DarkGreen, Red)

        self.refresh_list()
        schedule_progress_reset(self)

    # -------------------------------
    # View Model Button Click
    def View_Model_Button_Click (self, sender, args):
        self.Close()
        try:
            uidoc.Selection.PickObjects(ObjectType.Element, "View model tạm thời (Sử dụng Zoom, Pan,...)")

        except:
            pass
        import __main__
        __main__.rebar_window_open()

# -------------------------------
# Rebar window
def rebar_window_open():
    # Ensure user is authenticated
    try:
        if not AuthSession.EnsureAuthenticated():
            return
    except Exception as e:
        print(str(e))

    # Unit setup
    current_unit = get_unit(doc)
    if current_unit in ["m", "cm"]:
        with Transaction(doc, "Set Unit to mm") as t:
            t.Start()
            set_unit(doc)
            t.Commit()

    # Gather your data and show the main RebarListView
    rebar_data = RBU.GetRebarData(doc, Black, "Chọn Calculate để tính toán cốt thép")

    xaml_file  = "Rebar Manager.xaml"
    try:
        window = RebarWindow(xaml_file)
        window.populate_data(rebar_data)
        load_logo(window, __file__)
        window.show(modal=True)
    except Exception as e:
        alert(None, str(e), "UI DISPLAY ERROR")

# -------------------------------
# Entry point
def run_check():
    try:
        rebar_window_open()
    except Exception as e:
        print(str(e))

run_check()