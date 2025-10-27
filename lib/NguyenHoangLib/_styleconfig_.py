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
# System Libraries
import clr
clr.AddReference('PresentationCore')
clr.AddReference('PresentationFramework')
clr.AddReference('WindowsBase')

import System # type: ignore
from System.Windows.Media import Brushes, Color, SolidColorBrush # type: ignore
from System import Action # type: ignore
from System.Windows.Threading import DispatcherPriority, DispatcherTimer # type: ignore
from System.Windows.Media import FontFamily # type: ignore
from System.Windows.Media.Imaging import BitmapImage # type: ignore
from System import Uri # type: ignore

# Python Libraries
import os

# pyRevit Libraries
from pyrevit import script

# Nguyen Hoang Libraries
import clr
clr.AddReference('NguyenHoang.RBM.Msb')
from NguyenHoang.RBM.Msb import MessageBoxWindow   # type: ignore

# -------------------------------
# Global Color
DarkGreen = SolidColorBrush(Color.FromRgb(0, 150, 0))
DeepOrange = SolidColorBrush(Color.FromRgb(255, 140, 0))
Black = Brushes.Black
Gray = Brushes.Gray
Red = Brushes.Red
BlueGreen = SolidColorBrush(Color.FromRgb(0, 127, 160))
LightOrange = SolidColorBrush(Color.FromRgb(247,146,108))
DeepBlue = SolidColorBrush(Color.FromRgb(25,25,111))

# ProgressBar Color
FineRed = SolidColorBrush(Color.FromRgb(255, 132, 132))
FineYellow = SolidColorBrush(Color.FromRgb(243, 255, 136))
FineGreen = SolidColorBrush(Color.FromRgb(0, 241, 15))

# -------------------------------
# Global Rebar Alert Message
no_rebar_alert = "Không có cốt thép được chọn (┬┬﹏┬┬)"

# ----------------------- GLOBAL FUNCTION -----------------------
# Message Warning
def alert(owner, message, title="Alert"):
    return MessageBoxWindow.Show(owner, message, title, False)

# UI Update Message Column
def update_ui_message(window, partition, schedule_mark, message, color):
    for rebar_data in window.RebarListView.ItemsSource:
        if (rebar_data.Partition, rebar_data.ScheduleMark) == (partition, schedule_mark):
            rebar_data.Message = message
            rebar_data.MessageColor = color
            break

# ProgressBar Color
def get_progress_color(value):
    value = max(0, min(100, value))
    
    red_color = (251, 47, 47)      
    yellow_color = (233, 255, 40)  
    green_color = (0, 241, 15)     
    
    if value <= 50:
        ratio = value / 50.0
        r = int(red_color[0] + (yellow_color[0] - red_color[0]) * ratio)
        g = int(red_color[1] + (yellow_color[1] - red_color[1]) * ratio)
        b = int(red_color[2] + (yellow_color[2] - red_color[2]) * ratio)
    else:
        ratio = (value - 50) / 50.0
        r = int(yellow_color[0] + (green_color[0] - yellow_color[0]) * ratio)
        g = int(yellow_color[1] + (green_color[1] - green_color[1]) * ratio)
        b = int(yellow_color[2] + (green_color[2] - yellow_color[2]) * ratio)
    
    color = Color.FromArgb(255, r, g, b)
    return SolidColorBrush(color)

# Refresh ListView
def refresh_list(window):
    if window.collection_view_source:
        window.collection_view_source.View.Refresh()

# Update ProgressBar
def update_process_bar(window, value, partition=None, schedule_mark=None, random = True):
    try:
        window.ProgressBar.Value = value
        window.ProgressBar.Foreground = get_progress_color(value)

        if hasattr(window, "ProgressLabel"):
            if not partition and not schedule_mark:
                window.ProgressLabel.Text = "{}% - Running: . . .".format(value)
            elif not schedule_mark:
                window.ProgressLabel.Text = "{}% - Running: {}".format(value, partition)
            else:
                window.ProgressLabel.Text = "{}% - Running: {} - {}".format(value, partition, schedule_mark)

        if random:
            refresh_checkpoints = getattr(window, "_refresh_checkpoints", [])
            
            if value in refresh_checkpoints or value == 100:
                window.Dispatcher.Invoke(Action(lambda: None), DispatcherPriority.Background)
        else:
            window.Dispatcher.Invoke(Action(lambda: None), DispatcherPriority.Background)
            
    except Exception as e:
        print(" update_process_bar failed:", str(e))

# Force UI Update
def force_ui_update(control):
    def _noop(): pass
    control.Dispatcher.Invoke(Action(_noop), DispatcherPriority.Background)

# Delay Reset 0 Value
def schedule_progress_reset(window, delay_ms=1500):
    timer = DispatcherTimer()
    timer.Interval = System.TimeSpan.FromMilliseconds(delay_ms)

    def reset(sender, args):
        timer.Stop()
        update_process_bar(window, 0)
        force_ui_update(window.ProgressBar)

    timer.Tick += reset
    timer.Start()

# Load Logo 
def load_logo(window, current_file):
    logo_path_1 = os.path.join(os.path.dirname(current_file), 'Logo.png')
    logo_path_2 = os.path.join(os.path.dirname(current_file), 'Login.png')

    if os.path.exists(logo_path_1) or os.path.exists(logo_path_2):
        window.NguyenHoang_Logo.Source = BitmapImage(Uri(logo_path_1))
        window.NguyenHoang_Login.Source = BitmapImage(Uri(logo_path_2))
    else:
        print("Logo not found")

# Font For Logo If Missing
nasal_font_path = script.get_bundle_file('Nasalization.ttf')
base_uri = Uri("file:///" + os.path.dirname(nasal_font_path).replace('\\', '/') + "/")
nasal_font = FontFamily(base_uri, "./#Nasalization")

