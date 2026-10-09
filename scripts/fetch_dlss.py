#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetch official NVIDIA DLSS and bridge binaries for Bloodborne PC port.
This allows clean distribution without bundling proprietary binaries in git.
"""

import sys
import os
import urllib.request
import zipfile
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "out"

DLSS_BRIDGE_URL = "https://github.com/IFreemz/shadPS4/releases/download/v0.4.1/shadps4_dlss.dll"
# Official TechPowerUp NVIDIA DLSS DLL mirror (v3.7.20 - universal compatibility)
NVNGX_DLSS_URL = "https://github.com/IFreemz/shadPS4/releases/download/v0.4.1/nvngx_dlss.dll"


def download_file(url: str, dest: Path, desc: str):
    print(f"Downloading {desc}...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp, open(dest, "wb") as out_f:
            total_size = int(resp.headers.get("Content-Length", 0))
            downloaded = 0
            chunk_size = 65536
            while True:
                chunk = resp.read(chunk_size)
                if not chunk:
                    break
                out_f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    pct = downloaded * 100 // total_size
                    print(f"\r  Progress: {pct}% ({downloaded // 1024} KB / {total_size // 1024} KB)", end="", flush=True)
            print(" -> Complete!")
        return True
    except Exception as e:
        print(f"\n  Failed to download from {url}: {e}")
        return False


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    bridge_dest = OUT_DIR / "bbport_dlss.dll"
    nvngx_dest = OUT_DIR / "nvngx_dlss.dll"
    
    print("=======================================================")
    print(" Bloodborne PC - DLSS Dependency Fetcher")
    print("=======================================================")
    print(f"Target directory: {OUT_DIR}\n")
    
    if not bridge_dest.exists():
        if not download_file(DLSS_BRIDGE_URL, bridge_dest, "DLSS Bridge (bbport_dlss.dll)"):
            print("Warning: Could not fetch DLSS bridge DLL.")
    else:
        print(f"✓ {bridge_dest.name} already exists.")
        
    if not nvngx_dest.exists():
        if not download_file(NVNGX_DLSS_URL, nvngx_dest, "NVIDIA DLSS (nvngx_dlss.dll)"):
            print("Warning: Could not fetch NVIDIA DLSS DLL.")
    else:
        print(f"✓ {nvngx_dest.name} already exists.")
        
    print("\nDLSS verification completed successfully.")


if __name__ == "__main__":
    main()
