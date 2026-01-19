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
from System import AppDomain # type: ignore
from System.Reflection import Assembly, AssemblyName # type: ignore
from System.IO import FileInfo # type: ignore

ext_dir = os.path.dirname(__file__)
core_dir = os.path.join(ext_dir, 'lib', 'NguyenHoangCore')

if core_dir not in sys.path:
    sys.path.append(core_dir)

# -----------------------------
# Helpers
# -----------------------------
def _get_short_name(full_name):
    try:
        return AssemblyName(full_name).Name
    except:
        try:
            return full_name.split(',')[0]
        except:
            return full_name

def _find_loaded(short_name, want_reflection_only):
    try:
        for asm in AppDomain.CurrentDomain.GetAssemblies():
            try:
                if asm.GetName().Name == short_name:
                    if want_reflection_only:
                        if asm.ReflectionOnly:
                            return asm
                    else:
                        if not asm.ReflectionOnly:
                            return asm
            except:
                continue
    except:
        pass
    return None

def _resolve_path(short_name):
    cand = os.path.join(core_dir, short_name + ".dll")
    if os.path.exists(cand):
        return cand
    return None

# -----------------------------
# Resolve handlers (SAFE)
# -----------------------------
def _resolve(sender, args):
    try:
        short_name = _get_short_name(args.Name)

        # Never return reflection-only assembly for normal AssemblyResolve
        loaded = _find_loaded(short_name, want_reflection_only=False)
        if loaded is not None:
            return loaded

        dll_path = _resolve_path(short_name)
        if dll_path:
            return Assembly.LoadFrom(dll_path)
    except:
        pass
    return None

def _resolve_reflection_only(sender, args):
    try:
        short_name = _get_short_name(args.Name)

        loaded = _find_loaded(short_name, want_reflection_only=True)
        if loaded is not None:
            return loaded

        dll_path = _resolve_path(short_name)
        if dll_path:
            return Assembly.ReflectionOnlyLoadFrom(dll_path)
    except:
        pass
    return None

# Install handlers once
try:
    if not hasattr(AppDomain.CurrentDomain, "_nguyenhoang_resolver_installed"):
        AppDomain.CurrentDomain.AssemblyResolve += _resolve
        AppDomain.CurrentDomain.ReflectionOnlyAssemblyResolve += _resolve_reflection_only
        AppDomain.CurrentDomain._nguyenhoang_resolver_installed = True
except:
    pass

# -----------------------------
# Load DLLs (use ONE method only)
# -----------------------------
try:
    dlls = [fn for fn in os.listdir(core_dir) if fn.lower().endswith(".dll")]
    dlls.sort()

    for fn in dlls:
        dll_path = os.path.join(core_dir, fn)

        try:
            if not os.path.exists(dll_path):
                continue

            # Validate assembly name first
            try:
                an = AssemblyName.GetAssemblyName(dll_path)
                asm_name = an.Name
            except:
                continue

            # Skip if already loaded (normal load)
            if _find_loaded(asm_name, want_reflection_only=False) is not None:
                continue

            # IMPORTANT: Only add reference; do NOT also Assembly.LoadFrom again
            clr.AddReferenceToFileAndPath(dll_path)

        except Exception:
            traceback.print_exc()

except Exception:
    traceback.print_exc()
