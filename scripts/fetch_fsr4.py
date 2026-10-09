#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download FSR 4 (v07 INT8) Vulkan SPIR-V assets into fsr4_shaders/
"""

import os
import sys
import urllib.request
from pathlib import Path

COMMIT = "ae8d628fae208813172446d1e49ed94150b04658"
BASE_URL = f"https://raw.githubusercontent.com/FireBurn/Q2RTX/{COMMIT}/baseq2/fsr4_shaders"

DEST_DIR = Path(__file__).resolve().parent.parent / "fsr4_shaders"
DEST_DIR.mkdir(parents=True, exist_ok=True)

MODELS = ["native", "quality", "balanced", "performance", "ultraperf", "drs"]
TIERS = ["1080", "2160"]

files_to_download = [
    "LICENSE-FSR4-v07.txt",
    "rcas.spv",
    "spd_auto_exposure.spv"
]

for model in MODELS:
    files_to_download.append(f"fsr4_model_v07_i8_{model}_initializers.bin")
    files_to_download.append(f"fsr4_model_v07_i8_{model}_pre_weights.bin")
    files_to_download.append(f"fsr4_model_v07_i8_{model}_shader_manifest.json")
    for tier in TIERS:
        files_to_download.append(f"fsr4_model_v07_i8_{model}_{tier}_pre.spv")
        files_to_download.append(f"fsr4_model_v07_i8_{model}_{tier}_post.spv")
        for p in range(1, 13):
            files_to_download.append(f"fsr4_model_v07_i8_{model}_{tier}_pass{p}.spv")

print(f"Total FSR 4 asset files to check/download: {len(files_to_download)}")

downloaded = 0
already_present = 0

for i, filename in enumerate(files_to_download, 1):
    dest_path = DEST_DIR / filename
    if dest_path.exists() and dest_path.stat().st_size > 0:
        already_present += 1
        continue

    url = f"{BASE_URL}/{filename}"
    try:
        urllib.request.urlretrieve(url, dest_path)
        downloaded += 1
        if downloaded % 10 == 0 or downloaded == 1:
            print(f"[{i}/{len(files_to_download)}] Downloaded: {filename}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

print(f"\nFinished! Downloaded: {downloaded}, Already present: {already_present}")
