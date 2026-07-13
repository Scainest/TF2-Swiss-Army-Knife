"""Module 3 tab — Hitsound / Killsound trimmer."""

from __future__ import annotations

import os
import threading
from tkinter import filedialog

import customtkinter as ctk

from core import audio
from i18n import t
from .widgets import PathSelector, WaveformCanvas, ui_call


def _chan_label(n: int) -> str:
    return {1: "mono", 2: "stereo"}.get(n, t("sound.channels", n=n))


def _fmt_db(v: float) -> str:
    v = round(v)
    return f"{v:+d} dB" if v else "0 dB"


class SoundTab(ctk.CTkFrame):
    def __init__(self, master, config):
        super().__init__(master, fg_color="transparent")
        self._config = config
        self._data = None
        self._rate = 0
        self._duration = 0.0

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self, text=t("sound.header"), anchor="w", text_color="#9aa4b0",
            wraplength=880, justify="left").grid(
            row=0, column=0, sticky="ew", padx=16, pady=(12, 4))

        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.grid(row=1, column=0, sticky="ew", padx=16, pady=4)
        ctk.CTkButton(bar, text="📂 " + t("sound.pick_file"),
                      command=self._pick_file).pack(side="left")
        self._info = ctk.CTkLabel(bar, text="", text_color="#9aa4b0")
        self._info.pack(side="left", padx=12)

        wave_frame = ctk.CTkFrame(self)
        wave_frame.grid(row=2, column=0, sticky="ew", padx=16, pady=8)
        wave_frame.grid_columnconfigure(0, weight=1)
        self._wave = WaveformCanvas(wave_frame, width=860, height=190,
                                    on_change=self._on_marker_drag)
        self._wave.grid(row=0, column=0, padx=10, pady=10)
        self._wave._redraw()

        # --- trim controls ---
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.grid(row=3, column=0, sticky="ew", padx=16, pady=4)
        ctk.CTkLabel(controls, text=t("sound.start")).pack(side="left")
        self._start_var = ctk.StringVar(value="0.00")
        self._end_var = ctk.StringVar(value="0.00")
        start_entry = ctk.CTkEntry(controls, textvariable=self._start_var,
                                   width=80)
        start_entry.pack(side="left", padx=(6, 16))
        ctk.CTkLabel(controls, text=t("sound.end")).pack(side="left")
        end_entry = ctk.CTkEntry(controls, textvariable=self._end_var,
                                 width=80)
        end_entry.pack(side="left", padx=(6, 16))
        for entry in (start_entry, end_entry):
            entry.bind("<Return>", lambda e: self._apply_entries())
            entry.bind("<FocusOut>", lambda e: self._apply_entries())
        self._sel_label = ctk.CTkLabel(controls, text="",
                                       text_color="#9aa4b0")
        self._sel_label.pack(side="left", padx=8)

        ctk.CTkButton(controls, text="⏹ " + t("sound.stop"), width=100,
                      fg_color="#3a3f47", hover_color="#4a505a",
                      command=self._stop_preview).pack(side="right", padx=4)
        ctk.CTkButton(controls, text="▶ " + t("sound.preview_btn"), width=100,
                      command=self._preview).pack(side="right", padx=4)

        # --- effects (Audacity-style): volume / bass / treble / normalize ---
        fx = ctk.CTkFrame(self)
        fx.grid(row=4, column=0, sticky="ew", padx=16, pady=(2, 6))
        ctk.CTkLabel(fx, text="🎛 " + t("sound.effects"),
                     font=ctk.CTkFont(weight="bold")).pack(side="left",
                                                           padx=(12, 14), pady=8)
        self._gain = self._fx_slider(fx, "sound.volume")
        self._bass = self._fx_slider(fx, "sound.bass")
        self._treble = self._fx_slider(fx, "sound.treble")
        self._normalize = ctk.CTkCheckBox(fx, text=t("sound.normalize"),
                                          onvalue=True, offvalue=False)
        self._normalize.pack(side="left", padx=(10, 8))
        ctk.CTkButton(fx, text="↺ " + t("sound.reset_fx"), width=108,
                      fg_color="#3a3f47", hover_color="#4a505a",
                      command=self._reset_fx).pack(side="right", padx=(4, 12))

        self._path_sel = PathSelector(
            self, config, "sound_export_path", t("common.export_dir_custom"))
        self._path_sel.grid(row=5, column=0, sticky="ew", padx=16, pady=8)

        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.grid(row=6, column=0, sticky="ew", padx=16, pady=(4, 16))
        self._hit_btn = ctk.CTkButton(
            bottom, text="🎯 " + t("sound.export_hit"), height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda: self._export("hitsound"))
        self._hit_btn.pack(side="left")
        self._kill_btn = ctk.CTkButton(
            bottom, text="💀 " + t("sound.export_kill"), height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#8c3b3b", hover_color="#a34848",
            command=lambda: self._export("killsound"))
        self._kill_btn.pack(side="left", padx=12)
        self._status = ctk.CTkLabel(bottom, text="", wraplength=460,
                                    justify="left")
        self._status.pack(side="left", padx=8)

    # ------------------------------------------------------------------

    def _fx_slider(self, parent, label_key):
        box = ctk.CTkFrame(parent, fg_color="transparent")
        box.pack(side="left", padx=(0, 10))
        ctk.CTkLabel(box, text=t(label_key), width=42, anchor="w").pack(
            side="left")
        vallab = ctk.CTkLabel(box, text="0 dB", width=48, text_color="#9aa4b0")
        slider = ctk.CTkSlider(
            box, from_=-12, to=12, number_of_steps=48, width=110,
            command=lambda v, lab=vallab: lab.configure(text=_fmt_db(v)))
        slider.set(0)
        slider.pack(side="left", padx=(4, 2))
        vallab.pack(side="left")
        slider._vallab = vallab
        return slider

    def _effects(self) -> dict:
        return dict(gain_db=self._gain.get(), bass_db=self._bass.get(),
                    treble_db=self._treble.get(),
                    normalize=bool(self._normalize.get()))

    def _reset_fx(self):
        for s in (self._gain, self._bass, self._treble):
            s.set(0)
            s._vallab.configure(text="0 dB")
        self._normalize.deselect()

    def _pick_file(self):
        path = filedialog.askopenfilename(
            title=t("sound.pick_dialog"),
            filetypes=[(t("common.audio_filter"), "*.mp3 *.wav *.ogg *.flac"),
                       (t("common.all_files"), "*.*")])
        if not path:
            return
        self._info.configure(text="⏳ " + t("sound.loading"))

        def work():
            try:
                data, rate = audio.load_audio(path)
                env = audio.waveform_envelope(data, 840)
            except Exception as exc:
                ui_call(lambda exc=exc: self._load_done(path, error=str(exc)))
            else:
                ui_call(lambda: self._load_done(path, data=data,
                                                rate=rate, env=env))

        threading.Thread(target=work, daemon=True).start()

    def _load_done(self, path, data=None, rate=0, env=None, error=None):
        if error:
            self._info.configure(text="")
            self._set_status(f"❌ {error}", error=True)
            return
        self._data, self._rate = data, rate
        self._duration = audio.duration_seconds(data, rate)
        self._wave.set_audio(env, self._duration)
        self._start_var.set("0.00")
        self._end_var.set(f"{self._duration:.2f}")
        self._info.configure(text=t(
            "sound.file_info", name=os.path.basename(path),
            dur=f"{self._duration:.2f}", rate=rate,
            ch=_chan_label(data.shape[1])))
        self._update_sel_label()
        self._set_status("")

    def _on_marker_drag(self, start, end):
        self._start_var.set(f"{start:.2f}")
        self._end_var.set(f"{end:.2f}")
        self._update_sel_label()

    def _apply_entries(self):
        if self._data is None:
            return
        try:
            start = float(self._start_var.get().replace(",", "."))
            end = float(self._end_var.get().replace(",", "."))
        except ValueError:
            return
        self._wave.set_selection(start, end)
        start, end = self._wave.get_selection()
        self._start_var.set(f"{start:.2f}")
        self._end_var.set(f"{end:.2f}")
        self._update_sel_label()

    def _update_sel_label(self):
        start, end = self._wave.get_selection()
        self._sel_label.configure(text=t("sound.selection", x=f"{end - start:.2f}"))

    def _selection(self):
        start, end = self._wave.get_selection()
        return start, end

    def _preview(self):
        if self._data is None:
            self._set_status("❌ " + t("sound.load_first"), error=True)
            return
        try:
            import sounddevice as sd
            start, end = self._selection()
            segment = audio.process_selection(self._data, self._rate,
                                              start, end, **self._effects())
            sd.stop()
            sd.play(segment, audio.TARGET_SAMPLE_RATE)
        except Exception as exc:
            self._set_status("❌ " + t("common.preview_error", exc=exc),
                             error=True)

    def _stop_preview(self):
        try:
            import sounddevice as sd
            sd.stop()
        except Exception:
            pass

    def _export(self, kind: str):
        if self._data is None:
            self._set_status("❌ " + t("sound.load_first"), error=True)
            return
        export_dir = self._path_sel.get()
        if not export_dir:
            self._set_status("❌ " + t("common.select_export_custom"),
                             error=True)
            return
        start, end = self._selection()
        effects = self._effects()
        for btn in (self._hit_btn, self._kill_btn):
            btn.configure(state="disabled")
        self._set_status("⏳ " + t("sound.exporting"))

        def work():
            try:
                info = audio.export_sound(self._data, self._rate, start, end,
                                          export_dir, kind, **effects)
            except Exception as exc:
                ui_call(lambda exc=exc: self._export_done(error=str(exc)))
            else:
                ui_call(lambda: self._export_done(info=info))

        threading.Thread(target=work, daemon=True).start()

    def _export_done(self, info=None, error=None):
        for btn in (self._hit_btn, self._kill_btn):
            btn.configure(state="normal")
        if error:
            self._set_status(f"❌ {error}", error=True)
            return
        self._set_status("✅ " + t(
            "sound.saved", dur=f"{info['duration']:.2f}",
            ch=_chan_label(info["channels"]), path=info["output_path"]))

    def _set_status(self, text, error=False):
        self._status.configure(
            text=text, text_color="#e05b5b" if error else "#7fca6a")
