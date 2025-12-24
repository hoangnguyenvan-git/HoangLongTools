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

# HoangLongTools.extension/startup.py
import os
import sys
import clr

import System # type: ignore
from System import AppDomain # type: ignore
from System.Reflection import Assembly # type: ignore

ext_dir  = os.path.dirname(__file__)
core_dir = os.path.join(ext_dir, 'lib', 'NguyenHoangCore')

if core_dir not in sys.path:
    sys.path.append(core_dir)

# Resolve dependencies from core_dir
def _resolve(sender, args):
    try:
        name = args.Name.split(',')[0] + ".dll"
        cand = os.path.join(core_dir, name)
        if os.path.exists(cand):
            return Assembly.LoadFrom(cand)
    except:
        pass
    return None

try:
    AppDomain.CurrentDomain.AssemblyResolve += _resolve
except:
    pass

for fn in os.listdir(core_dir):
    if not fn.lower().endswith('.dll'):
        continue

    lname = fn.lower()
    if lname.startswith('revitapi'):
        continue
    if lname.startswith('adwindows'):
        continue
    if lname.startswith('uiframework'):
        continue

    dll_path = os.path.join(core_dir, fn)

    try:
        clr.AddReferenceToFileAndPath(dll_path)
    except:
        pass
