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
import traceback
from System import AppDomain #type: ignore
from System.Reflection import Assembly, AssemblyName #type: ignore
from System.IO import FileInfo #type: ignore

ext_dir = os.path.dirname(__file__)
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
    except Exception:
        pass
    return None

try:
    AppDomain.CurrentDomain.AssemblyResolve += _resolve
except Exception:
    pass

# Load all DLLs
try:
    dlls = [fn for fn in os.listdir(core_dir) if fn.lower().endswith('.dll')]
    dlls.sort()
    
    for fn in dlls:
        dll_path = os.path.join(core_dir, fn)
        try:
            if not os.path.exists(dll_path):
                continue
            
            # Pre-validate the assembly (this was in your debug version)
            fi = FileInfo(dll_path)
            try:
                an = AssemblyName.GetAssemblyName(dll_path)
            except Exception:
                continue
            
            # Now load it
            clr.AddReferenceToFileAndPath(dll_path)
            
            # Pre-load the assembly to trigger dependency resolution
            try:
                asm = Assembly.LoadFrom(dll_path)
            except Exception:
                pass
                
        except Exception:
            traceback.print_exc()
except Exception:
    traceback.print_exc()