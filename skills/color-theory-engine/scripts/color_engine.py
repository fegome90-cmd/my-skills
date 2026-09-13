#!/usr/bin/env python3
"""
Color Theory Engine - Mathematical processing for UI color harmonies and accessibility.
Optimized for Claude invocation following python-patterns.
"""

import colorsys
import json
import sys
from typing import Dict, List, NamedTuple, Tuple, Union


class ContrastResult(NamedTuple):
    """Structured result for WCAG contrast validation."""
    ratio: float
    passes_AA_normal: bool
    passes_AA_large: bool
    passes_AAA_normal: bool
    passes_AAA_large: bool


class ColorEngine:
    """
    A deterministic engine for color manipulation using HSL and Relative Luminance.
    """

    @staticmethod
    def validate_hex(hex_code: str) -> str:
        """Ensures the hex code is in a valid #RRGGBB format."""
        hex_code = hex_code.lstrip('#').upper()
        if len(hex_code) != 6:
            raise ValueError(f"Invalid HEX length: '{hex_code}'. Expected 6 characters.")
        # Check if it's a valid hexadecimal
        int(hex_code, 16)
        return f"#{hex_code}"

    @classmethod
    def hex_to_rgb(cls, hex_code: str) -> Tuple[float, float, float]:
        """Converts HEX to RGB normalized (0.0 to 1.0)."""
        valid_hex = cls.validate_hex(hex_code).lstrip('#')
        return tuple(int(valid_hex[i:i+2], 16) / 255.0 for i in (0, 2, 4)) # type: ignore

    @staticmethod
    def rgb_to_hex(r: float, g: float, b: float) -> str:
        """Converts normalized RGB back to HEX."""
        return f"#{int(round(r * 255)):02X}{int(round(g * 255)):02X}{int(round(b * 255)):02X}"

    @staticmethod
    def calculate_relative_luminance(rgb: Tuple[float, float, float]) -> float:
        """
        Calculates relative luminance using WCAG 2.1 formula.
        L = 0.2126 * R + 0.7152 * G + 0.0722 * B
        """
        def linearize(c: float) -> float:
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

        r, g, b = (linearize(c) for c in rgb)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    @classmethod
    def check_contrast(cls, foreground_hex: str, background_hex: str) -> Dict[str, Union[float, bool]]:
        """Calculates contrast ratio between two colors."""
        try:
            lum1 = cls.calculate_relative_luminance(cls.hex_to_rgb(foreground_hex))
            lum2 = cls.calculate_relative_luminance(cls.hex_to_rgb(background_hex))
            
            # Formula: (L1 + 0.05) / (L2 + 0.05) where L1 is lighter
            l1, l2 = max(lum1, lum2), min(lum1, lum2)
            ratio = (l1 + 0.05) / (l2 + 0.05)
            r_ratio = round(ratio, 2)
            
            result = ContrastResult(
                ratio=r_ratio,
                passes_AA_normal=ratio >= 4.5,
                passes_AA_large=ratio >= 3.0,
                passes_AAA_normal=ratio >= 7.0,
                passes_AAA_large=ratio >= 4.5
            )
            return result._asdict()
        except Exception as e:
            return {"error": str(e)}

    @classmethod
    def generate_harmony(cls, base_hex: str, harmony_type: str) -> List[str]:
        """Generates harmonies rotating the Hue in HSL space."""
        try:
            r, g, b = cls.hex_to_rgb(base_hex)
            h, l, s = colorsys.rgb_to_hls(r, g, b)
            
            rotations = {
                'complementary': [0.5],
                'analogous': [30/360.0, -30/360.0],
                'triadic': [120/360.0, 240/360.0]
            }
            
            h_type = harmony_type.lower()
            if h_type not in rotations:
                raise ValueError(f"Harmony '{h_type}' not supported. Use: {list(rotations.keys())}")

            palette = [base_hex.upper()]
            for rot in rotations[h_type]:
                new_h = (h + rot) % 1.0
                nr, ng, nb = colorsys.hls_to_rgb(new_h, l, s)
                palette.append(cls.rgb_to_hex(nr, ng, nb))
            return palette
        except Exception as e:
            return [f"Error: {str(e)}"]


def main():
    """CLI Entry point for skill invocation."""
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: python color_engine.py <harmony|contrast> <args>"}))
        sys.exit(1)
    
    command = sys.argv[1].lower()
    engine = ColorEngine()
    
    if command == "harmony" and len(sys.argv) == 4:
        # Args: base_hex, type
        print(json.dumps(engine.generate_harmony(sys.argv[2], sys.argv[3])))
    elif command == "contrast" and len(sys.argv) == 4:
        # Args: hex1, hex2
        print(json.dumps(engine.check_contrast(sys.argv[2], sys.argv[3])))
    else:
        print(json.dumps({"error": "Invalid command or arguments."}))

if __name__ == "__main__":
    main()
