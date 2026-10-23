#!/usr/bin/env python3
"""Contrast ratio for two opaque, uniform sRGB HEX colors; no dependencies."""

import argparse
import json
import math
import re


def hex_color(value):
    if not re.fullmatch(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})", value):
        raise argparse.ArgumentTypeError("use opaque #RGB or #RRGGBB; alpha is unsupported")
    digits = value[1:]
    if len(digits) == 3:
        digits = "".join(char * 2 for char in digits)
    return "#" + digits.lower()


def threshold_value(value):
    try:
        result = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("threshold must be a finite number from 1 to 21") from error
    if not math.isfinite(result) or not 1 <= result <= 21:
        raise argparse.ArgumentTypeError("threshold must be a finite number from 1 to 21")
    return result


def luminance(color):
    channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4 for channel in channels]
    return sum(channel * weight for channel, weight in zip(linear, (0.2126, 0.7152, 0.0722)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("foreground", type=hex_color)
    parser.add_argument("background", type=hex_color)
    parser.add_argument("--threshold", type=threshold_value, default=4.5)
    args = parser.parse_args()
    light, dark = sorted((luminance(args.foreground), luminance(args.background)), reverse=True)
    ratio = (light + 0.05) / (dark + 0.05)
    passed = ratio >= args.threshold
    print(json.dumps({
        "foreground": args.foreground,
        "background": args.background,
        "ratio": ratio,
        "threshold": args.threshold,
        "status": "PASS" if passed else "FAIL",
        "scope": "Two opaque, uniform sRGB colors only; no compositing, text-size assessment or overall accessibility claim."
    }, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
