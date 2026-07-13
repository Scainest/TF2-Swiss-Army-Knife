"""Main window: TF2 detection banner + three module tabs + language picker."""

from __future__ import annotations

import os
import subprocess
import sys
import threading
from tkinter import filedialog

import customtkinter as ctk

from config import ConfigManager
from i18n import (available_languages, detect_default, get_language,
                  set_language, t)
from resources import resource_path
from tf2_locator import find_tf2_path, suggested_paths
from .objector_tab import ObjectorTab
from .sound_tab import SoundTab
from .spray_tab import SprayTab
from .widgets import drain_ui_queue, ui_call

BRAND = "Teufort Toolkit"
_APP_ID = "Scainest.TeufortToolkit"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.config_mgr = ConfigManager()
        set_language(self.config_mgr.get("language") or detect_default())

        self.title(BRAND)
        self.geometry("980x770")
        self.minsize(920, 710)
        ctk.set_appearance_mode("dark")
        self._apply_window_icon()

        # --- top bar: brand + TF2 folder status + language ---
        top = ctk.CTkFrame(self, corner_radius=0)
        top.pack(fill="x")
        ctk.CTkLabel(top, text=f"🔧 {BRAND}",
                     font=ctk.CTkFont(size=17, weight="bold")
                     ).pack(side="left", padx=16, pady=10)

        self._lang_by_native = {n: c for c, n in available_languages()}
        native_by_code = {c: n for c, n in available_languages()}
        self._lang_menu = ctk.CTkOptionMenu(
            top, width=120, values=list(self._lang_by_native.keys()),
            command=self._on_language_change)
        self._lang_menu.set(native_by_code.get(get_language(), "English"))
        self._lang_menu.pack(side="right", padx=(4, 16))
        ctk.CTkLabel(top, text="🌐").pack(side="right")

        ctk.CTkButton(top, text="📁 " + t("app.manual"), width=110,
                      fg_color="#3a3f47", hover_color="#4a505a",
                      command=self._pick_tf2).pack(side="right", padx=(4, 12))
        ctk.CTkButton(top, text="🔍 " + t("app.rescan"), width=120,
                      command=self._detect_tf2).pack(side="right", padx=4)
        self._tf2_label = ctk.CTkLabel(top, text=t("app.searching"),
                                       text_color="#9aa4b0")
        self._tf2_label.pack(side="right", padx=12)

        # --- tabs ---
        self._tabs = ctk.CTkTabview(self, anchor="nw")
        self._tabs.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        tab1 = self._tabs.add("  🎨 " + t("tab.spray") + "  ")
        tab2 = self._tabs.add("  🖼️ " + t("tab.objector") + "  ")
        tab3 = self._tabs.add("  🔊 " + t("tab.sound") + "  ")
        for tab in (tab1, tab2, tab3):
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure(0, weight=1)

        self.spray_tab = SprayTab(tab1, self.config_mgr)
        self.spray_tab.grid(row=0, column=0, sticky="nsew")
        self.objector_tab = ObjectorTab(tab2, self.config_mgr)
        self.objector_tab.grid(row=0, column=0, sticky="nsew")
        self.sound_tab = SoundTab(tab3, self.config_mgr)
        self.sound_tab.grid(row=0, column=0, sticky="nsew")

        self.after(100, self._detect_tf2)
        self.after(30, self._poll_ui_queue)
        self.after(400, self._apply_window_icon)

    # ------------------------------------------------------------------

    def _apply_window_icon(self):
        """Show the app icon in the title bar and taskbar, in dev and exe."""
        if sys.platform == "win32":
            try:
                import ctypes
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                    _APP_ID)
            except Exception:
                pass
        ico = resource_path("assets", "icon.ico")
        if os.path.isfile(ico):
            try:
                self.iconbitmap(ico)
            except Exception:
                pass

    def _poll_ui_queue(self):
        """Runs callables queued by worker threads (thread-safe UI updates)."""
        drain_ui_queue()
        self.after(30, self._poll_ui_queue)

    # -- language -------------------------------------------------------

    def _on_language_change(self, native_name: str):
        code = self._lang_by_native.get(native_name)
        if not code or code == get_language():
            return
        self.config_mgr.set("language", code)
        self._relaunch()

    def _relaunch(self):
        """Restart the app so every widget is rebuilt in the new language."""
        try:
            if getattr(sys, "frozen", False):
                subprocess.Popen([sys.executable])
            else:
                subprocess.Popen([sys.executable, resource_path("main.py")])
        except Exception:
            pass
        self.destroy()

    # -- TF2 detection --------------------------------------------------

    def _detect_tf2(self):
        self._tf2_label.configure(text=t("app.searching"),
                                  text_color="#9aa4b0")

        def work():
            path = self.config_mgr.get("tf2_path")
            if not path or not os.path.isdir(path):
                path = find_tf2_path() or ""
            ui_call(lambda: self._apply_tf2(path))

        threading.Thread(target=work, daemon=True).start()

    def _pick_tf2(self):
        chosen = filedialog.askdirectory(title=t("app.pick_tf2_dialog"))
        if chosen:
            self._apply_tf2(chosen.replace("/", "\\"))

    def _apply_tf2(self, path: str):
        if path and os.path.isdir(path):
            self.config_mgr.set("tf2_path", path)
            self._tf2_label.configure(text=f"✅ {path}",
                                      text_color="#7fca6a")
            for key, value in suggested_paths(path).items():
                if not self.config_mgr.get(key):
                    self.config_mgr.set(key, value)
            self.spray_tab._path_sel.set(
                self.config_mgr.get("spray_export_path"), persist=False)
            self.objector_tab._path_sel.set(
                self.config_mgr.get("objector_export_path"), persist=False)
            self.sound_tab._path_sel.set(
                self.config_mgr.get("sound_export_path"), persist=False)
        else:
            self._tf2_label.configure(
                text="⚠️ " + t("app.tf2_not_found"), text_color="#e0a95b")


def run():
    app = App()
    app.mainloop()
