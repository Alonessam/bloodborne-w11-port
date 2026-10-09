#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build fixed and guarded FSR 4 passes into fsr4_shaders/opt/
Fixes the known pass11 data race / out-of-bounds writes that crash NVIDIA GPUs (TDR).
"""

import os
import sys
import glob
import tempfile
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "fsr4_shaders"
DEST_DIR = SRC_DIR / "opt"
DEST_DIR.mkdir(parents=True, exist_ok=True)

SPIRV_CROSS = r"C:\msys64\ucrt64\bin\spirv-cross.exe"
GLSLANG = r"C:\msys64\ucrt64\bin\glslangValidator.exe"
PERL = r"C:\msys64\usr\bin\perl.exe"

POST_REWRITE = REPO_ROOT / "tools" / "fsr4_post_lds.pl"
PASS11_REWRITE = REPO_ROOT / "tools" / "fsr4_pass11_guard.pl"


def build_pass(spv_path: Path, rewrite_pl: Path, entry: str):
    out_spv = DEST_DIR / spv_path.name
    with tempfile.TemporaryDirectory() as tmpdir:
        in_comp = Path(tmpdir) / "in.comp"
        out_comp = Path(tmpdir) / "out.comp"
        tmp_spv = Path(tmpdir) / "out.spv"

        # 1. spirv-cross decompile
        cmd1 = [SPIRV_CROSS, str(spv_path), "--vulkan-semantics", "--entry", entry, "--output", str(in_comp)]
        res1 = subprocess.run(cmd1, capture_output=True, text=True)
        if res1.returncode != 0:
            print(f"Error decompiling {spv_path.name}: {res1.stderr}")
            return False

        # 2. Normalize CRLF to LF for perl regexes
        comp_text = in_comp.read_text(encoding="utf-8").replace("\r\n", "\n")
        in_comp.write_text(comp_text, encoding="utf-8", newline="\n")

        # 3. perl rewrite
        cmd2 = [PERL, str(rewrite_pl)]
        with open(in_comp, "rb") as fin, open(out_comp, "wb") as fout:
            res2 = subprocess.run(cmd2, stdin=fin, stdout=fout, stderr=subprocess.PIPE, cwd=str(REPO_ROOT / "tools"))
            if res2.returncode != 0:
                print(f"Error rewriting {spv_path.name}: {res2.stderr.decode()}")
                return False

        # 3. glslangValidator recompile
        cmd3 = [GLSLANG, "-V", "--target-env", "vulkan1.3", "-S", "comp", "-e", entry, "--source-entrypoint", "main",
                str(out_comp), "-o", str(tmp_spv)]
        res3 = subprocess.run(cmd3, capture_output=True, text=True)
        if res3.returncode != 0:
            print(f"Error recompiling {spv_path.name}: {res3.stderr}")
            return False

        # Move to destination
        out_spv.write_bytes(tmp_spv.read_bytes())
        return True


def main():
    print("Building guarded and optimized FSR 4 passes...")
    post_files = sorted(SRC_DIR.glob("fsr4_model_v07_i8_*_post.spv"))
    pass11_files = sorted(SRC_DIR.glob("fsr4_model_v07_i8_*_pass11.spv"))

    built = 0
    for p in post_files:
        print(f"Optimizing post pass: {p.name}")
        if build_pass(p, POST_REWRITE, "main"):
            built += 1

    for p in pass11_files:
        print(f"Applying boundary guard to pass 11: {p.name}")
        if build_pass(p, PASS11_REWRITE, "fsr4_model_v07_i8_pass11"):
            built += 1

    print(f"\nSuccessfully built {built} optimized FSR 4 passes in {DEST_DIR}!")


if __name__ == "__main__":
    main()
