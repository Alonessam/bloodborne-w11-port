#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bloodborne PC - Definitive Windows 11 GUI Launcher
Supports: Multi-Language (8 Languages), DLSS, XeSS, FSR 4 Neural, FSR 3.1,
          Intel 12th+ Gen Hybrid CPU Pinning, 6GB VRAM Protection & Save Manager.
"""

import os
import sys
import locale
import zipfile
import datetime
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import launcher_i18n

REPO_ROOT = Path(__file__).resolve().parent
CONFIG_PATH = REPO_ROOT / "bbport.ini"
RUN_PS1 = REPO_ROOT / "run.ps1"
USER_DIR = REPO_ROOT / "user"
SAVES_DIR = USER_DIR / "savedata"
BACKUPS_DIR = USER_DIR / "backups"

# Upscaler identifiers and definitions
UPSCALER_KEYS = [
    ("dlss", "NVIDIA DLSS (AI Tensor - RTX 20/30/40)"),
    ("xess", "Intel XeSS (AI Upscaling - Arc / GTX / AMD)"),
    ("fsr4", "AMD FSR 4 (Neural INT8 v07 - Pass 11 Fixed)"),
    ("fsr3", "AMD FSR 3.1 (FidelityFX - Kararlı)"),
    ("taa",  "TAA (Doğal / Native Anti-Aliasing)"),
    ("off",  "Kapalı / Off (Doğal 1080p)")
]

PRESET_KEYS = [
    ("0", "preset_native"),
    ("1", "preset_quality"),
    ("2", "preset_balanced"),
    ("3", "preset_perf"),
    ("4", "preset_ultra_perf")
]

FPS_MODES = [
    ("144", "uncap", "144", "fps_desc_144"),
    ("120", "uncap", "120", "fps_desc_120"),
    ("90",  "uncap", "90",  "fps_desc_90"),
    ("60",  "uncap", "60",  "fps_desc_60"),
    ("uncap", "uncap", "0", "fps_desc_uncap"),
    ("30",  "30",    "30",  "fps_desc_30")
]

RESOLUTIONS = [
    "1920x1080",
    "2560x1440",
    "3840x2160",
    "1280x720"
]


class BBDefinitiveLauncher:
    def __init__(self, root):
        self.root = root
        self.root.geometry("820x760")
        self.root.minsize(780, 700)
        self.root.configure(bg="#121316")

        # Determine default language
        self.current_lang = self.detect_initial_language()

        # Styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()

        # Try window icon
        self.setup_window_icon()

        # State Variables
        self.lang_var = tk.StringVar(value=self.current_lang)
        self.fps_var = tk.StringVar(value="144")
        self.res_var = tk.StringVar(value="1920x1080")
        self.upscaler_var = tk.StringVar(value="dlss")
        self.preset_var = tk.StringVar(value="0")
        self.sharpness_val = tk.DoubleVar(value=0.10)
        self.game_path_var = tk.StringVar(value="")

        # Checkboxes
        self.chk_chromatic = tk.BooleanVar(value=True)  # True = Disabled chromatic (clean)
        self.chk_motion_blur = tk.BooleanVar(value=False)
        self.chk_dof = tk.BooleanVar(value=True)
        self.chk_ssao = tk.BooleanVar(value=True)
        self.chk_dyn_shadows = tk.BooleanVar(value=True)
        self.chk_skip_intro = tk.BooleanVar(value=True)
        self.chk_show_fps = tk.BooleanVar(value=True)

        # Hardware & Stability
        self.chk_intel_hybrid = tk.BooleanVar(value=True)
        self.chk_vram_safe = tk.BooleanVar(value=True)
        self.chk_jitter = tk.BooleanVar(value=True)

        # Load existing config
        self.load_ini()

        # Build UI
        self.build_ui()
        self.refresh_ui_text()

    def tr(self, key):
        return launcher_i18n.get_text(self.current_lang, key)

    def detect_initial_language(self):
        try:
            loc, _ = locale.getdefaultlocale()
            if loc:
                prefix = loc.split("_")[0].lower()
                if prefix in launcher_i18n.LANGUAGES:
                    return prefix
        except Exception:
            pass
        return "tr"

    def find_game_directory(self):
        saved = self.game_path_var.get()
        if saved and (Path(saved) / "eboot.bin").exists():
            return saved
        env_dir = os.environ.get("BB_GAME_DIR")
        if env_dir and (Path(env_dir) / "eboot.bin").exists():
            return env_dir
        candidates = [
            REPO_ROOT / "game",
            REPO_ROOT / "game" / "CUSA03173",
            REPO_ROOT.parent / "CUSA03173",
            REPO_ROOT.parent / "Bloodborne",
            Path.home() / "Desktop" / "Ps4 oyun" / "CUSA03173",
            Path.home() / "Desktop" / "Ps4 oyun",
            Path.home() / "Desktop" / "CUSA03173",
            Path.home() / "Desktop" / "Bloodborne"
        ]
        for c in candidates:
            if (c / "eboot.bin").exists():
                return str(c)
            if c.exists():
                for sub in c.glob("**/eboot.bin"):
                    return str(sub.parent)
        return ""

    def setup_window_icon(self):
        icon_path = REPO_ROOT / "user" / "savedata" / "1" / "CUSA00900" / "SPRJ0005.sce_sys" / "icon0.png"
        if not icon_path.exists():
            g_dir = self.find_game_directory()
            if g_dir:
                icon_path = Path(g_dir) / "sce_sys" / "icon0.png"
        if icon_path.exists():
            try:
                self.icon_img = tk.PhotoImage(file=str(icon_path))
                self.root.iconphoto(False, self.icon_img)
            except Exception:
                pass

    def configure_styles(self):
        card_bg = "#1b1d22"
        text_fg = "#f1f5f9"
        text_dim = "#94a3b8"
        accent_red = "#991b1b"
        accent_hover = "#b91c1c"

        self.style.configure(".", background="#121316", foreground=text_fg, font=("Segoe UI", 10))
        self.style.configure("TLabel", background="#121316", foreground=text_fg)
        self.style.configure("Card.TFrame", background=card_bg, relief="solid", borderwidth=1)
        self.style.configure("CardLabel.TLabel", background=card_bg, foreground="#f8fafc", font=("Segoe UI", 10, "bold"))
        self.style.configure("CardText.TLabel", background=card_bg, foreground=text_fg, font=("Segoe UI", 9, "bold"))
        self.style.configure("Desc.TLabel", background=card_bg, foreground="#38bdf8", font=("Segoe UI", 9, "italic"))
        self.style.configure("Dim.TLabel", background=card_bg, foreground=text_dim, font=("Segoe UI", 9))

        self.style.configure("TCheckbutton", background=card_bg, foreground=text_fg, font=("Segoe UI", 9))
        self.style.map("TCheckbutton", background=[("active", card_bg)], foreground=[("active", "#ffffff")])

        self.style.configure("TCombobox", fieldbackground="#262930", background="#262930", foreground="#ffffff", arrowcolor="#ffffff")
        self.style.map("TCombobox", fieldbackground=[("readonly", "#262930")], foreground=[("readonly", "#ffffff")])

        self.style.configure("Launch.TButton", background=accent_red, foreground="#ffffff", font=("Segoe UI", 12, "bold"), padding=10)
        self.style.map("Launch.TButton", background=[("active", accent_hover), ("pressed", "#7f1d1d")])

        self.style.configure("Secondary.TButton", background="#262930", foreground="#ffffff", font=("Segoe UI", 10), padding=6)
        self.style.map("Secondary.TButton", background=[("active", "#333842"), ("pressed", "#1e2127")])

        self.style.configure("Save.TButton", background="#047857", foreground="#ffffff", font=("Segoe UI", 9, "bold"), padding=5)
        self.style.map("Save.TButton", background=[("active", "#059669"), ("pressed", "#065f46")])

    def build_ui(self):
        # 1. Header Bar
        header = tk.Frame(self.root, bg="#0d0e11", padx=20, pady=12)
        header.pack(fill="x")

        title_box = tk.Frame(header, bg="#0d0e11")
        title_box.pack(side="left")

        self.title_lbl = tk.Label(title_box, text=self.tr("title"), font=("Georgia", 18, "bold"), fg="#f8fafc", bg="#0d0e11")
        self.title_lbl.pack(anchor="w")

        self.sub_lbl = tk.Label(title_box, text=self.tr("subtitle"), font=("Segoe UI", 9), fg="#94a3b8", bg="#0d0e11")
        self.sub_lbl.pack(anchor="w")

        # Language dropdown at top right
        lang_box = tk.Frame(header, bg="#0d0e11")
        lang_box.pack(side="right", padx=(0, 5))

        self.lang_label = tk.Label(lang_box, text=self.tr("lang_label"), font=("Segoe UI", 9, "bold"), fg="#cbd5e1", bg="#0d0e11")
        self.lang_label.pack(side="left", padx=(0, 6))

        lang_names = [f"{code.upper()} - {name}" for code, name in launcher_i18n.LANGUAGES.items()]
        self.lang_combo = ttk.Combobox(lang_box, values=lang_names, state="readonly", width=16)
        # Select current
        for item in lang_names:
            if item.lower().startswith(self.current_lang):
                self.lang_combo.set(item)
                break
        self.lang_combo.pack(side="left")
        self.lang_combo.bind("<<ComboboxSelected>>", self.on_language_change)

        # Main scrollable canvas container
        container = tk.Frame(self.root, bg="#121316")
        container.pack(fill="both", expand=True, padx=14, pady=8)

        canvas = tk.Canvas(container, bg="#121316", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg="#121316")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(xscrollcommand=None, yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mouse wheel support
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # 1.5. Game Directory Card
        self.game_card = ttk.Frame(self.scroll_frame, style="Card.TFrame", padding=12)
        self.game_card.pack(fill="x", pady=5)

        self.game_card_header = ttk.Label(self.game_card, text=self.tr("game_card_title"), style="CardLabel.TLabel")
        self.game_card_header.pack(anchor="w")

        game_row = tk.Frame(self.game_card, bg="#1b1d22")
        game_row.pack(fill="x", pady=(6, 2))

        self.game_path_entry = tk.Entry(game_row, textvariable=self.game_path_var, bg="#262930", fg="#ffffff", insertbackground="#ffffff", relief="flat", font=("Segoe UI", 9))
        self.game_path_entry.pack(side="left", fill="x", expand=True, padx=(0, 8), ipady=4)

        self.btn_browse = ttk.Button(game_row, text=self.tr("btn_browse"), style="Secondary.TButton", command=self.browse_game_dir)
        self.btn_browse.pack(side="right")

        self.game_status_lbl = tk.Label(self.game_card, text="", bg="#1b1d22", font=("Segoe UI", 9))
        self.game_status_lbl.pack(anchor="w", pady=(2, 0))

        # 2. Performance & Target FPS Card
        self.fps_card = ttk.Frame(self.scroll_frame, style="Card.TFrame", padding=12)
        self.fps_card.pack(fill="x", pady=5)

        self.fps_card_header = ttk.Label(self.fps_card, text=self.tr("fps_card_title"), style="CardLabel.TLabel")
        self.fps_card_header.pack(anchor="w")

        fps_row = tk.Frame(self.fps_card, bg="#1b1d22")
        fps_row.pack(fill="x", pady=(6, 2))

        self.fps_title_lbl = ttk.Label(fps_row, text=self.tr("fps_label"), style="CardText.TLabel")
        self.fps_title_lbl.pack(side="left")

        fps_display_values = [
            f"{mode[0]} FPS" if mode[0] != "uncap" else "Uncapped (Sınırsız)" for mode in FPS_MODES
        ]
        self.fps_combo = ttk.Combobox(fps_row, values=fps_display_values, state="readonly", width=40)
        self.fps_combo.pack(side="right", fill="x", expand=True, padx=(10, 0))
        self.fps_combo.bind("<<ComboboxSelected>>", self.on_fps_change)

        self.fps_desc_lbl = ttk.Label(self.fps_card, text="", style="Desc.TLabel", wraplength=720)
        self.fps_desc_lbl.pack(anchor="w", pady=(4, 0))

        # 3. Display & AI Upscaling Card
        self.disp_card = ttk.Frame(self.scroll_frame, style="Card.TFrame", padding=12)
        self.disp_card.pack(fill="x", pady=5)

        self.disp_card_header = ttk.Label(self.disp_card, text=self.tr("display_card_title"), style="CardLabel.TLabel")
        self.disp_card_header.pack(anchor="w")

        grid_disp = tk.Frame(self.disp_card, bg="#1b1d22")
        grid_disp.pack(fill="x", pady=(6, 4))

        # Resolution
        self.res_lbl = ttk.Label(grid_disp, text=self.tr("resolution_label"), style="CardText.TLabel")
        self.res_lbl.grid(row=0, column=0, sticky="w", pady=4)
        self.res_combo = ttk.Combobox(grid_disp, values=RESOLUTIONS, state="readonly", width=18)
        self.res_combo.set(self.res_var.get())
        self.res_combo.grid(row=0, column=1, sticky="w", padx=(8, 20), pady=4)
        self.res_combo.bind("<<ComboboxSelected>>", lambda e: self.res_var.set(self.res_combo.get()))

        # Upscaler
        self.upscaler_lbl = ttk.Label(grid_disp, text=self.tr("upscaler_label"), style="CardText.TLabel")
        self.upscaler_lbl.grid(row=0, column=2, sticky="w", pady=4)
        upscaler_display = [u[1] for u in UPSCALER_KEYS]
        self.upscaler_combo = ttk.Combobox(grid_disp, values=upscaler_display, state="readonly", width=34)
        self.upscaler_combo.grid(row=0, column=3, sticky="w", padx=(8, 0), pady=4)
        self.upscaler_combo.bind("<<ComboboxSelected>>", self.on_upscaler_change)

        # Preset Quality
        self.preset_lbl = ttk.Label(grid_disp, text=self.tr("preset_label"), style="CardText.TLabel")
        self.preset_lbl.grid(row=1, column=0, sticky="w", pady=4)
        self.preset_combo = ttk.Combobox(grid_disp, state="readonly", width=22)
        self.preset_combo.grid(row=1, column=1, sticky="w", padx=(8, 20), pady=4)
        self.preset_combo.bind("<<ComboboxSelected>>", self.on_preset_change)

        # Sharpness Slider
        sharp_row = tk.Frame(self.disp_card, bg="#1b1d22")
        sharp_row.pack(fill="x", pady=(4, 4))
        self.sharp_title_lbl = ttk.Label(sharp_row, text=self.tr("sharpness_label"), style="CardText.TLabel")
        self.sharp_title_lbl.pack(side="left")

        self.sharp_val_disp = tk.Label(sharp_row, text=f"{self.sharpness_val.get():.2f}", font=("Segoe UI", 9, "bold"), fg="#38bdf8", bg="#1b1d22", width=5)
        self.sharp_val_disp.pack(side="right")

        sharp_scale = ttk.Scale(
            sharp_row,
            from_=0.0,
            to=1.0,
            variable=self.sharpness_val,
            orient="horizontal",
            command=lambda v: self.sharp_val_disp.config(text=f"{float(v):.2f}")
        )
        sharp_scale.pack(side="left", fill="x", expand=True, padx=(10, 10))

        self.sharp_tip_lbl = ttk.Label(self.disp_card, text=self.tr("sharpness_tip"), style="Dim.TLabel")
        self.sharp_tip_lbl.pack(anchor="w")

        # 4. Community Patches & Fixes Card
        self.patch_card = ttk.Frame(self.scroll_frame, style="Card.TFrame", padding=12)
        self.patch_card.pack(fill="x", pady=5)

        self.patch_card_header = ttk.Label(self.patch_card, text=self.tr("patches_card_title"), style="CardLabel.TLabel")
        self.patch_card_header.pack(anchor="w", pady=(0, 4))

        patch_grid = tk.Frame(self.patch_card, bg="#1b1d22")
        patch_grid.pack(fill="x")

        self.c_chroma = ttk.Checkbutton(patch_grid, text=self.tr("chk_chromatic"), variable=self.chk_chromatic)
        self.c_chroma.grid(row=0, column=0, sticky="w", pady=2)

        self.c_mblur = ttk.Checkbutton(patch_grid, text=self.tr("chk_motion_blur"), variable=self.chk_motion_blur)
        self.c_mblur.grid(row=1, column=0, sticky="w", pady=2)

        self.c_intro = ttk.Checkbutton(patch_grid, text=self.tr("chk_skip_intro"), variable=self.chk_skip_intro)
        self.c_intro.grid(row=2, column=0, sticky="w", pady=2)

        self.c_dof = ttk.Checkbutton(patch_grid, text=self.tr("chk_dof"), variable=self.chk_dof)
        self.c_dof.grid(row=0, column=1, sticky="w", padx=(20, 0), pady=2)

        self.c_ssao = ttk.Checkbutton(patch_grid, text=self.tr("chk_ssao"), variable=self.chk_ssao)
        self.c_ssao.grid(row=1, column=1, sticky="w", padx=(20, 0), pady=2)

        self.c_dyn = ttk.Checkbutton(patch_grid, text=self.tr("chk_dyn_shadows"), variable=self.chk_dyn_shadows)
        self.c_dyn.grid(row=2, column=1, sticky="w", padx=(20, 0), pady=2)

        self.c_fps = ttk.Checkbutton(self.patch_card, text=self.tr("chk_show_fps"), variable=self.chk_show_fps)
        self.c_fps.pack(anchor="w", pady=(4, 0))

        # 5. Hardware & Stability Card
        self.hw_card = ttk.Frame(self.scroll_frame, style="Card.TFrame", padding=12)
        self.hw_card.pack(fill="x", pady=5)

        self.hw_card_header = ttk.Label(self.hw_card, text=self.tr("hardware_card_title"), style="CardLabel.TLabel")
        self.hw_card_header.pack(anchor="w", pady=(0, 4))

        self.c_intel = ttk.Checkbutton(self.hw_card, text=self.tr("chk_intel_hybrid"), variable=self.chk_intel_hybrid)
        self.c_intel.pack(anchor="w", pady=2)

        self.c_vram = ttk.Checkbutton(self.hw_card, text=self.tr("chk_vram_safe"), variable=self.chk_vram_safe)
        self.c_vram.pack(anchor="w", pady=2)

        self.c_jitter = ttk.Checkbutton(self.hw_card, text=self.tr("chk_jitter"), variable=self.chk_jitter)
        self.c_jitter.pack(anchor="w", pady=2)

        # 6. Save Game & Backup Manager Card
        self.save_card = ttk.Frame(self.scroll_frame, style="Card.TFrame", padding=12)
        self.save_card.pack(fill="x", pady=5)

        self.save_card_header = ttk.Label(self.save_card, text=self.tr("save_card_title"), style="CardLabel.TLabel")
        self.save_card_header.pack(anchor="w", pady=(0, 6))

        save_btn_row = tk.Frame(self.save_card, bg="#1b1d22")
        save_btn_row.pack(fill="x")

        self.btn_backup = ttk.Button(save_btn_row, text=self.tr("btn_backup_save"), style="Save.TButton", command=self.backup_save_game)
        self.btn_backup.pack(side="left", padx=(0, 8))

        self.btn_restore = ttk.Button(save_btn_row, text=self.tr("btn_restore_save"), style="Secondary.TButton", command=self.restore_save_game)
        self.btn_restore.pack(side="left", padx=(0, 8))

        self.btn_open_folder = ttk.Button(save_btn_row, text=self.tr("btn_open_save_folder"), style="Secondary.TButton", command=self.open_save_folder)
        self.btn_open_folder.pack(side="left")

        # 7. Bottom Action Bar
        action_bar = tk.Frame(self.root, bg="#0d0e11", padx=20, pady=12)
        action_bar.pack(fill="x", side="bottom")

        self.btn_reset = ttk.Button(action_bar, text=self.tr("btn_reset_defaults"), style="Secondary.TButton", command=self.reset_defaults)
        self.btn_reset.pack(side="left")

        self.btn_save = ttk.Button(action_bar, text=self.tr("btn_save_config"), style="Secondary.TButton", command=self.save_settings)
        self.btn_save.pack(side="left", padx=10)

        self.btn_launch = ttk.Button(action_bar, text=self.tr("btn_launch_game"), style="Launch.TButton", command=self.launch_game)
        self.btn_launch.pack(side="right")

    def refresh_ui_text(self):
        """Updates all UI text according to current_lang"""
        self.title_lbl.config(text=self.tr("title"))
        self.sub_lbl.config(text=self.tr("subtitle"))
        self.lang_label.config(text=self.tr("lang_label"))

        # Game Directory
        self.game_card_header.config(text=self.tr("game_card_title"))
        self.btn_browse.config(text=self.tr("btn_browse"))
        self.update_game_status()

        self.fps_card_header.config(text=self.tr("fps_card_title"))
        self.fps_title_lbl.config(text=self.tr("fps_label"))
        self.update_fps_desc()

        self.disp_card_header.config(text=self.tr("display_card_title"))
        self.res_lbl.config(text=self.tr("resolution_label"))
        self.upscaler_lbl.config(text=self.tr("upscaler_label"))
        self.preset_lbl.config(text=self.tr("preset_label"))
        self.sharp_title_lbl.config(text=self.tr("sharpness_label"))
        self.sharp_tip_lbl.config(text=self.tr("sharpness_tip"))

        # Presets translated values
        preset_items = [self.tr(p[1]) for p in PRESET_KEYS]
        self.preset_combo.config(values=preset_items)
        curr_p_idx = int(self.preset_var.get()) if self.preset_var.get().isdigit() else 0
        if 0 <= curr_p_idx < len(preset_items):
            self.preset_combo.set(preset_items[curr_p_idx])

        # Patches
        self.patch_card_header.config(text=self.tr("patches_card_title"))
        self.c_chroma.config(text=self.tr("chk_chromatic"))
        self.c_mblur.config(text=self.tr("chk_motion_blur"))
        self.c_intro.config(text=self.tr("chk_skip_intro"))
        self.c_dof.config(text=self.tr("chk_dof"))
        self.c_ssao.config(text=self.tr("chk_ssao"))
        self.c_dyn.config(text=self.tr("chk_dyn_shadows"))
        self.c_fps.config(text=self.tr("chk_show_fps"))

        # Hardware
        self.hw_card_header.config(text=self.tr("hardware_card_title"))
        self.c_intel.config(text=self.tr("chk_intel_hybrid"))
        self.c_vram.config(text=self.tr("chk_vram_safe"))
        self.c_jitter.config(text=self.tr("chk_jitter"))

        # Save Manager
        self.save_card_header.config(text=self.tr("save_card_title"))
        self.btn_backup.config(text=self.tr("btn_backup_save"))
        self.btn_restore.config(text=self.tr("btn_restore_save"))
        self.btn_open_folder.config(text=self.tr("btn_open_save_folder"))

        # Bottom Bar
        self.btn_reset.config(text=self.tr("btn_reset_defaults"))
        self.btn_save.config(text=self.tr("btn_save_config"))
        self.btn_launch.config(text=self.tr("btn_launch_game"))

    def browse_game_dir(self):
        initial = self.game_path_var.get() or str(Path.home() / "Desktop")
        chosen = filedialog.askdirectory(title=self.tr("browse_title"), initialdir=initial)
        if chosen:
            self.game_path_var.set(chosen)
            self.update_game_status()
            self.save_settings(silent=True)

    def update_game_status(self):
        path_str = self.game_path_var.get().strip()
        if path_str and (Path(path_str) / "eboot.bin").exists():
            self.game_status_lbl.config(text=self.tr("game_status_found"), fg="#4ade80")
        elif path_str:
            self.game_status_lbl.config(text=self.tr("game_status_missing"), fg="#f87171")
        else:
            self.game_status_lbl.config(text=self.tr("game_status_missing"), fg="#fbbf24")

    def on_language_change(self, event=None):
        selected = self.lang_combo.get()
        code = selected.split(" - ")[0].strip().lower()
        if code in launcher_i18n.LANGUAGES:
            self.current_lang = code
            self.lang_var.set(code)
            self.refresh_ui_text()

    def on_fps_change(self, event=None):
        sel_idx = self.fps_combo.current()
        if 0 <= sel_idx < len(FPS_MODES):
            self.fps_var.set(FPS_MODES[sel_idx][0])
            self.update_fps_desc()

    def update_fps_desc(self):
        curr = self.fps_var.get()
        for mode in FPS_MODES:
            if mode[0] == curr:
                self.fps_desc_lbl.config(text=self.tr(mode[3]))
                break

    def on_upscaler_change(self, event=None):
        sel_idx = self.upscaler_combo.current()
        if 0 <= sel_idx < len(UPSCALER_KEYS):
            self.upscaler_var.set(UPSCALER_KEYS[sel_idx][0])

    def on_preset_change(self, event=None):
        sel_idx = self.preset_combo.current()
        if 0 <= sel_idx < len(PRESET_KEYS):
            self.preset_var.set(PRESET_KEYS[sel_idx][0])

    def load_ini(self):
        if not CONFIG_PATH.exists():
            return
        try:
            content = CONFIG_PATH.read_text(encoding="utf-8")
            for raw_line in content.splitlines():
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    k, v = k.strip().lower(), v.strip()
                    if k == "language" and v in launcher_i18n.LANGUAGES:
                        self.current_lang = v
                    elif k == "output_res":
                        self.res_var.set(v)
                    elif k == "upscaler":
                        self.upscaler_var.set(v)
                    elif k == "preset":
                        self.preset_var.set(v)
                    elif k == "sharpness":
                        try:
                            self.sharpness_val.set(float(v))
                        except ValueError:
                            pass
                    elif k == "fps_limit":
                        self.fps_var.set(v if v != "0" else "uncap")
                    elif k == "effect_chromatic_aberration":
                        self.chk_chromatic.set(v == "0")  # 0 means disabled
                    elif k == "effect_motion_blur":
                        self.chk_motion_blur.set(v == "1")
                    elif k == "effect_dof":
                        self.chk_dof.set(v == "1")
                    elif k == "effect_ssao":
                        self.chk_ssao.set(v == "1")
                    elif k == "effect_dynamic_shadows":
                        self.chk_dyn_shadows.set(v == "1")
                    elif k == "skip_intro":
                        self.chk_skip_intro.set(v == "1")
                    elif k == "show_fps":
                        self.chk_show_fps.set(v == "1")
                    elif k == "intel_hybrid_fix":
                        self.chk_intel_hybrid.set(v == "1")
                    elif k == "vram_safe_mode":
                        self.chk_vram_safe.set(v == "1")
                    elif k == "jitter":
                        self.chk_jitter.set(v != "0")
                    elif k == "game_dir":
                        self.game_path_var.set(v)
        except Exception:
            pass

        if not self.game_path_var.get().strip():
            auto_path = self.find_game_directory()
            if auto_path:
                self.game_path_var.set(auto_path)

    def save_settings(self, silent=False):
        ca_ini = "0" if self.chk_chromatic.get() else "1"
        mb_ini = "1" if self.chk_motion_blur.get() else "0"
        dof_ini = "1" if self.chk_dof.get() else "0"
        ssao_ini = "1" if self.chk_ssao.get() else "0"
        dyn_ini = "1" if self.chk_dyn_shadows.get() else "0"
        skip_ini = "1" if self.chk_skip_intro.get() else "0"
        fps_disp_ini = "1" if self.chk_show_fps.get() else "0"
        intel_ini = "1" if self.chk_intel_hybrid.get() else "0"
        vram_ini = "1" if self.chk_vram_safe.get() else "0"
        jitter_ini = "1" if self.chk_jitter.get() else "0"

        fps_val = self.fps_var.get()
        fps_mode = "30" if fps_val == "30" else "uncap"
        fps_limit = "0" if fps_val == "uncap" else fps_val

        ini_content = f"""# Bloodborne PC Port Configuration (bbport.ini)
# Generated by Bloodborne PC Definitive Launcher

language={self.current_lang}
game_dir={self.game_path_var.get().strip()}
output_res={self.res_var.get()}
live_resolution=0
upscaler={self.upscaler_var.get()}
preset={self.preset_var.get()}
sharpen=1
sharpness={self.sharpness_val.get():.2f}
fps_mode={fps_mode}
fps_limit={fps_limit}

# Motion vectors & temporal stability
jitter={jitter_ini}
reactive=0
object_motion=0
fsr4_invert_jitter=0

# Live HUD
show_fps={fps_disp_ini}

# Visual patches
effect_chromatic_aberration={ca_ini}
effect_dof={dof_ini}
effect_motion_blur={mb_ini}
effect_ssao={ssao_ini}
effect_game_aa=0
effect_dynamic_shadows={dyn_ini}
effect_ssr=0
skip_intro={skip_ini}
debug_camera=0
debug_menu=0
model_lod=0

# Hardware & Stability Optimizations
intel_hybrid_fix={intel_ini}
vram_safe_mode={vram_ini}
"""
        try:
            CONFIG_PATH.write_text(ini_content, encoding="utf-8")
            if not silent:
                messagebox.showinfo(self.tr("msg_saved_title"), self.tr("msg_saved_text"))
            return True
        except Exception as e:
            if not silent:
                messagebox.showerror("Error", f"{e}")
            return False

    def reset_defaults(self):
        self.fps_var.set("144")
        self.res_var.set("1920x1080")
        self.res_combo.set("1920x1080")
        self.upscaler_var.set("dlss")
        self.preset_var.set("0")
        self.sharpness_val.set(0.10)
        self.sharp_val_disp.config(text="0.10")

        self.chk_chromatic.set(True)
        self.chk_motion_blur.set(False)
        self.chk_dof.set(True)
        self.chk_ssao.set(True)
        self.chk_dyn_shadows.set(True)
        self.chk_skip_intro.set(True)
        self.chk_show_fps.set(True)
        self.chk_intel_hybrid.set(True)
        self.chk_vram_safe.set(True)

        self.refresh_ui_text()
        messagebox.showinfo(self.tr("msg_saved_title"), self.tr("msg_defaults_restored"))

    def backup_save_game(self):
        if not SAVES_DIR.exists():
            messagebox.showwarning("Notice", "Save directory not found yet.")
            return

        BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = BACKUPS_DIR / f"bloodborne_save_{timestamp}.zip"

        try:
            with zipfile.ZipFile(backup_file, "w", zipfile.ZIP_DEFLATED) as zf:
                for root_dir, _, files in os.walk(SAVES_DIR):
                    for file in files:
                        full_path = Path(root_dir) / file
                        arcname = full_path.relative_to(SAVES_DIR)
                        zf.write(full_path, arcname)
            messagebox.showinfo(self.tr("msg_saved_title"), f"{self.tr('msg_backup_ok')}{backup_file.name}")
        except Exception as e:
            messagebox.showerror("Backup Error", f"{e}")

    def restore_save_game(self):
        if not BACKUPS_DIR.exists():
            messagebox.showinfo("Notice", self.tr("msg_no_backup"))
            return

        backups = sorted(list(BACKUPS_DIR.glob("*.zip")), key=lambda p: p.stat().st_mtime, reverse=True)
        if not backups:
            messagebox.showinfo("Notice", self.tr("msg_no_backup"))
            return

        latest_backup = backups[0]
        try:
            with zipfile.ZipFile(latest_backup, "r") as zf:
                zf.extractall(SAVES_DIR)
            messagebox.showinfo(self.tr("msg_saved_title"), self.tr("msg_restore_ok"))
        except Exception as e:
            messagebox.showerror("Restore Error", f"{e}")

    def open_save_folder(self):
        SAVES_DIR.mkdir(parents=True, exist_ok=True)
        try:
            os.startfile(str(SAVES_DIR))
        except Exception:
            subprocess.Popen(["explorer.exe", str(SAVES_DIR)])

    def launch_game(self):
        if not self.save_settings(silent=True):
            return

        fps_val = self.fps_var.get()
        chosen_mode = "30" if fps_val == "30" else "uncap"
        chosen_limit = "0" if fps_val == "uncap" else fps_val

        cmd = [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy", "Bypass",
            "-File", str(RUN_PS1),
            "-Fps", chosen_mode,
            "-SaveLog"
        ]

        if self.game_path_var.get().strip():
            cmd.extend(["-GameDir", self.game_path_var.get().strip()])

        child_env = os.environ.copy()
        child_env["BB_LANGUAGE"] = self.current_lang
        child_env["BB_FPS_LIMIT"] = str(chosen_limit)
        child_env["BB_UPSCALER"] = self.upscaler_var.get()
        child_env["BB_UPSCALE_PRESET"] = self.preset_var.get()
        child_env["BB_INTEL_HYBRID_FIX"] = "1" if self.chk_intel_hybrid.get() else "0"
        child_env["BB_VRAM_SAFE_MODE"] = "1" if self.chk_vram_safe.get() else "0"
        child_env["BB_SAVE_LOG"] = "1"

        try:
            subprocess.Popen(
                cmd,
                cwd=str(REPO_ROOT),
                env=child_env,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            self.root.iconify()
        except Exception as e:
            messagebox.showerror("Error", f"{self.tr('msg_launch_error')}{e}")


def main():
    root = tk.Tk()
    app = BBDefinitiveLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
