#!/usr/bin/env python3
import json
import os
import sys

# Discover the directory where the 'script' is located
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "magic_bytes.json")

# Load JSON using an obsolute path
try:
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        magic_numbers = json.load(f)
except FileNotFoundError:
    print(f"Erro: Arquivo {JSON_PATH} não encontrado.")
    sys.exit(1)

# Load Signatures JSON
# with open("magic_bytes.json", "r", encoding="utf-8") as f:
#    magic_numbers = json.load(f)


def check_type(filepath):
    _, extension = os.path.splitext(filepath)
    extension = extension.lstrip(".").lower()

    if not extension or extension not in magic_numbers:
        print(f"Extension '{extension}' was not found in database")
        return False

    # 1. PROTECTION AGAINST "TOUCH" IN LINUX: Ignore Files with 0 Bytes
    if os.path.getsize(filepath) == 0:
        print(f"✗ File '{filepath}' is empty (0 bytes).")
        return False

    with open(filepath, "rb") as f:
        for signature in magic_numbers[extension]:
            # 2. PROBLEMATIC OFFSETS TREATMENT ("any" or empty)
            offset_raw = str(signature["offset"]).strip().lower()
            is_any_offset = offset_raw == "any"

            if offset_raw in ("any", ""):
                offset = 0
            else:
                offset = (
                    int(offset_raw.replace("0x", ""), 16)
                    if offset_raw.startswith("0x")
                    else int(offset_raw)
                )
            # 3. HEX WITH "JOKER" TRETMENT IN magic_bytes.json file("nn")
            hex_parts = signature["hex"].strip().split()

            if is_any_offset:
                # If the offset can be anywhere, search in the first 8Kb
                f.seek(0)
                content = f.read(8192)
                # Look just the start of the HEX(Before the "nn")
                primeira_parte = signature["hex"].split(" nn")[0].replace(" ", "")
                if primeira_parte and bytes.fromhex(primeira_parte) in content:
                    print(f"✓ Match with type declared: .{extension}")
                    print(f"  Description: {signature['description']}")
                    return True
            else:
                f.seek(offset)
                header = f.read(len(hex_parts))
                # It compares every byte, so it can ignore the "nn"
                match = True
                for i, hex_byte in enumerate(hex_parts):
                    if hex_byte.lower() == "nn":
                        continue  # Ignore the verification of this specific byte
                    if i >= len(header) or header[i] != int(hex_byte, 16):
                        match = False
                        break

                if match:
                    print(f"✓ Match with type declared: .{extension}")
                    print(f"  Description: {signature['description']}")
                    return True

    print(f"✗ Does not match with type declared: .{extension}")
    return False


# Verify if the user passed the file name
if len(sys.argv) < 2:
    print("Error: Inform the file name.")
    sys.exit(1)

print(1 if check_type(sys.argv[1]) else 0)
