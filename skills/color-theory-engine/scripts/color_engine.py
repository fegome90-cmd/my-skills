#!/usr/bin/env python3
"""Portable color palette and contrast utilities for the color-theory-engine skill."""

from __future__ import annotations

import argparse
import colorsys
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, NoReturn, Optional, Sequence, Tuple, Union, cast


HEX_PATTERN = re.compile(r"[0-9A-Fa-f]+\Z")


def _load_color_spaces() -> Any:
    """Load the sibling math module when this file runs as a standalone script."""
    path = Path(__file__).resolve().with_name("color_spaces.py")
    spec = importlib.util.spec_from_file_location("_color_theory_engine_color_spaces", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load color-space module at '{path}'.")
    module = cast(Any, importlib.util.module_from_spec(spec))
    spec.loader.exec_module(module)
    return module


color_spaces = _load_color_spaces()


class ContrastResult(NamedTuple):
    """Structured result for WCAG contrast validation."""

    ratio: float
    passes_AA_normal: bool
    passes_AA_large: bool
    passes_AAA_normal: bool
    passes_AAA_large: bool


class ColorEngine:
    """Deterministic color operations with legacy HSL harmony compatibility."""

    @staticmethod
    def validate_hex(hex_code: str) -> str:
        """Normalize #RGB/RGB/#RRGGBB/RRGGBB to uppercase #RRGGBB."""
        if not isinstance(hex_code, str) or not hex_code:
            raise ValueError("HEX color must be a non-empty string.")
        if hex_code != hex_code.strip():
            raise ValueError("HEX color must not contain surrounding whitespace.")

        value = hex_code[1:] if hex_code.startswith("#") else hex_code
        if "#" in value:
            raise ValueError("HEX color may contain at most one leading '#'.")
        if len(value) == 3 and HEX_PATTERN.fullmatch(value):
            value = "".join(channel * 2 for channel in value)
        elif len(value) != 6 or not HEX_PATTERN.fullmatch(value):
            raise ValueError(
                f"Invalid HEX color '{hex_code}'. Use 3 or 6 hexadecimal digits, "
                "with at most one leading '#'."
            )
        return f"#{value.upper()}"

    @classmethod
    def hex_to_rgb(cls, hex_code: str) -> Tuple[float, float, float]:
        """Convert a supported HEX form to normalized sRGB channels."""
        value = cls.validate_hex(hex_code)[1:]
        return tuple(int(value[index : index + 2], 16) / 255.0 for index in (0, 2, 4))  # type: ignore[return-value]

    @staticmethod
    def rgb_to_hex(red: float, green: float, blue: float) -> str:
        """Convert normalized sRGB channels to uppercase 8-bit HEX."""
        return "#" + "".join(
            f"{int(round(channel * 255)):02X}" for channel in (red, green, blue)
        )

    @staticmethod
    def calculate_relative_luminance(rgb: Tuple[float, float, float]) -> float:
        """Calculate legacy WCAG relative luminance for normalized sRGB."""

        def linearize(channel: float) -> float:
            return (
                channel / 12.92
                if channel <= 0.03928
                else ((channel + 0.055) / 1.055) ** 2.4
            )

        red, green, blue = (linearize(channel) for channel in rgb)
        return 0.2126 * red + 0.7152 * green + 0.0722 * blue

    @classmethod
    def check_contrast(
        cls, foreground_hex: str, background_hex: str
    ) -> Dict[str, Union[float, bool]]:
        """Return five WCAG fields; invalid colors raise ValueError."""
        foreground_luminance = cls.calculate_relative_luminance(
            cls.hex_to_rgb(foreground_hex)
        )
        background_luminance = cls.calculate_relative_luminance(
            cls.hex_to_rgb(background_hex)
        )
        lighter = max(foreground_luminance, background_luminance)
        darker = min(foreground_luminance, background_luminance)
        raw_ratio = (lighter + 0.05) / (darker + 0.05)
        return ContrastResult(
            ratio=round(raw_ratio, 2),
            passes_AA_normal=raw_ratio >= 4.5,
            passes_AA_large=raw_ratio >= 3.0,
            passes_AAA_normal=raw_ratio >= 7.0,
            passes_AAA_large=raw_ratio >= 4.5,
        )._asdict()

    @classmethod
    def generate_scale(cls, base_hex: str) -> Dict[str, object]:
        """Generate the canonical eleven-step OKLCH scale anchored at 500."""
        normalized = cls.validate_hex(base_hex)
        lab = color_spaces.srgb_to_oklab(cls.hex_to_rgb(normalized))
        return color_spaces.generate_scale(normalized, lab)

    @classmethod
    def wada_palette(
        cls, palette_id: int, dataset_path: Optional[Union[str, Path]] = None
    ) -> Dict[str, Any]:
        """Return the colors in a Wada Sanzo palette, in dataset order."""
        data = load_wada_dataset(dataset_path)
        all_ids = sorted({palette for color in data for palette in color["combinations"]})
        if palette_id not in all_ids:
            raise ValueError(
                f"Palette id {palette_id} not found. Available ids: "
                f"{all_ids[0]}..{all_ids[-1]} ({len(all_ids)} palettes)."
            )
        colors = [
            {"name": color["name"], "hex": color["hex"], "rgb": color["rgb"]}
            for color in data
            if palette_id in color["combinations"]
        ]
        return {
            "palette": palette_id,
            "color_count": len(colors),
            "colors": colors,
        }

    @classmethod
    def wada_color(
        cls,
        name: str,
        exact: bool = False,
        dataset_path: Optional[Union[str, Path]] = None,
    ) -> Dict[str, Any]:
        """Find exact names first, then all substring matches unless exact-only."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Wada color name must be a non-empty string.")
        data = load_wada_dataset(dataset_path)
        target = name.strip().casefold()
        exact_matches = [
            color for color in data if color["name"].casefold() == target
        ]
        if exact:
            matches = exact_matches
        else:
            exact_ids = {id(color) for color in exact_matches}
            substring_matches = [
                color for color in data if target in color["name"].casefold()
            ]
            matches = exact_matches + [
                color for color in substring_matches if id(color) not in exact_ids
            ]
        if not matches:
            raise ValueError(f"No Wada color matches '{name}'.")

        results = []
        for color in matches:
            palettes = []
            for palette_id in color["combinations"]:
                members = [
                    {"name": member["name"], "hex": member["hex"]}
                    for member in data
                    if palette_id in member["combinations"] and member is not color
                ]
                palettes.append({"palette": palette_id, "members": members})
            results.append(
                {
                    "name": color["name"],
                    "hex": color["hex"],
                    "rgb": color["rgb"],
                    "swatch": color["swatch"],
                    "palettes": palettes,
                }
            )
        return {"matches": results}

    @classmethod
    def generate_harmony(
        cls, base_hex: str, harmony_type: str, space: Optional[str] = None
    ) -> List[str]:
        """Generate legacy HSL or opt-in OKLCH rotations and monochromatic steps."""
        if space is not None and not isinstance(space, str):
            raise ValueError("Harmony space must be a string or None.")
        if not isinstance(harmony_type, str):
            raise ValueError("Harmony type must be a string.")
        normalized_type = harmony_type.lower()
        cardinalities = {"complementary": 2, "analogous": 3, "triadic": 3}
        supported = (*cardinalities, "monochromatic")
        if normalized_type not in supported:
            raise ValueError(
                f"Harmony '{normalized_type}' is unsupported. Use: {', '.join(supported)}."
            )

        normalized_hex = cls.validate_hex(base_hex)
        if normalized_type == "monochromatic":
            if space is not None and space.lower() != "oklch":
                raise ValueError(
                    "Monochromatic harmony uses the canonical OKLCH scale; --space hsl is unsupported."
                )
            scale = cls.generate_scale(normalized_hex)
            steps = scale["steps"]
            return [steps[step] for step in ("100", "300", "500", "700", "900")]  # type: ignore[index]

        selected_space = "hsl" if space is None else space.lower()
        if selected_space not in ("hsl", "oklch"):
            raise ValueError("Harmony space must be 'hsl' or 'oklch'.")

        red, green, blue = cls.hex_to_rgb(normalized_hex)
        rotations = {
            "complementary": (180.0,),
            "analogous": (30.0, -30.0),
            "triadic": (120.0, 240.0),
        }
        lab = color_spaces.srgb_to_oklab((red, green, blue))
        lightness, chroma, hue = color_spaces.oklab_to_oklch(lab)
        if chroma <= color_spaces.ACHROMATIC_CHROMA:
            return [normalized_hex] * cardinalities[normalized_type]

        if selected_space == "hsl":
            hsl_hue, hsl_lightness, saturation = colorsys.rgb_to_hls(red, green, blue)
            palette = [normalized_hex]
            for rotation in rotations[normalized_type]:
                channels = colorsys.hls_to_rgb(
                    (hsl_hue + rotation / 360.0) % 1.0, hsl_lightness, saturation
                )
                palette.append(cls.rgb_to_hex(*channels))
            return palette

        if hue is None:
            return [normalized_hex] * cardinalities[normalized_type]
        palette = [normalized_hex]
        for rotation in rotations[normalized_type]:
            mapped = color_spaces.gamut_map_oklch((lightness, chroma, hue + rotation))
            palette.append(color_spaces.srgb_to_hex(mapped.rgb))
        return palette


def load_wada_dataset(
    dataset_path: Optional[Union[str, Path]] = None,
) -> List[Dict[str, Any]]:
    """Load and validate an explicitly supplied external Wada dataset."""
    if dataset_path is None:
        raise ValueError("Wada dataset is not bundled; provide --dataset PATH.")
    path = Path(dataset_path)
    try:
        with path.open(encoding="utf-8") as source:
            data = json.load(source)
    except FileNotFoundError as exc:
        raise ValueError(
            f"Wada dataset not found at '{path}'. Provide --dataset PATH."
        ) from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Wada dataset at '{path}' is not valid JSON: {exc}") from exc
    except OSError as exc:
        raise ValueError(f"Unable to read Wada dataset at '{path}': {exc}") from exc

    if not isinstance(data, list) or not data:
        raise ValueError("Wada dataset must be a non-empty JSON array.")
    required = {"name", "hex", "rgb", "swatch", "combinations"}
    for index, color in enumerate(data):
        if not isinstance(color, dict):
            raise ValueError(f"Wada dataset record {index} must be an object.")
        missing = required.difference(color)
        if missing:
            fields = ", ".join(sorted(missing))
            raise ValueError(f"Wada dataset record {index} is missing fields: {fields}.")
        if not isinstance(color["name"], str) or not color["name"].strip():
            raise ValueError(f"Wada dataset record {index} has an invalid name.")
        try:
            ColorEngine.validate_hex(color["hex"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Wada dataset record {index} has an invalid hex value.") from exc
        rgb = color["rgb"]
        if (
            not isinstance(rgb, list)
            or len(rgb) != 3
            or any(type(channel) is not int or not 0 <= channel <= 255 for channel in rgb)
        ):
            raise ValueError(f"Wada dataset record {index} has an invalid rgb value.")
        if type(color["swatch"]) is not int:
            raise ValueError(f"Wada dataset record {index} has an invalid swatch value.")
        combinations = color["combinations"]
        if (
            not isinstance(combinations, list)
            or not combinations
            or any(type(palette) is not int or palette < 1 for palette in combinations)
        ):
            raise ValueError(
                f"Wada dataset record {index} has invalid palette combinations."
            )
    return data


class JsonArgumentParser(argparse.ArgumentParser):
    """Argument parser that lets main emit the JSON error contract."""

    def error(self, message: str) -> NoReturn:
        raise ValueError(message)


def build_parser() -> JsonArgumentParser:
    parser = JsonArgumentParser(
        prog="color_engine.py",
        description="Generate color harmonies, contrast results, and Wada palette lookups.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    contrast = commands.add_parser("contrast", help="Calculate WCAG contrast.")
    contrast.add_argument("foreground")
    contrast.add_argument("background")

    harmony = commands.add_parser("harmony", help="Generate a color harmony.")
    harmony.add_argument("base_hex")
    harmony.add_argument(
        "harmony_type",
        type=str.lower,
        choices=("complementary", "analogous", "triadic", "monochromatic"),
    )
    harmony.add_argument("--space", choices=("hsl", "oklch"), default=None)

    scale = commands.add_parser("scale", help="Generate an eleven-step OKLCH scale.")
    scale.add_argument("base_hex")

    wada = commands.add_parser("wada", help="Query an external Wada Sanzo dataset.")
    query = wada.add_mutually_exclusive_group(required=True)
    query.add_argument("--id", type=int, dest="palette_id")
    query.add_argument("--name", nargs="+", dest="color_name")
    wada.add_argument("--exact", action="store_true", help="Only return exact color-name matches.")
    wada.add_argument("--dataset", type=Path, help="Path to an external Wada dataset JSON file.")
    return parser


def _write_error(message: str) -> int:
    print(json.dumps({"error": message}), file=sys.stderr)
    return 1


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run the CLI and return its process exit code."""
    parser = build_parser()
    cli_args = list(sys.argv[1:] if argv is None else argv)
    if cli_args and not cli_args[0].startswith("-"):
        cli_args[0] = cli_args[0].lower()
    try:
        arguments = parser.parse_args(cli_args)
        if arguments.command == "contrast":
            result = ColorEngine.check_contrast(arguments.foreground, arguments.background)
        elif arguments.command == "harmony":
            result = ColorEngine.generate_harmony(
                arguments.base_hex, arguments.harmony_type, arguments.space
            )
        elif arguments.command == "scale":
            result = ColorEngine.generate_scale(arguments.base_hex)
        elif arguments.command == "wada":
            if arguments.exact and arguments.color_name is None:
                raise ValueError("--exact is only valid with --name.")
            if arguments.palette_id is not None:
                result = ColorEngine.wada_palette(
                    arguments.palette_id, dataset_path=arguments.dataset
                )
            else:
                result = ColorEngine.wada_color(
                    " ".join(arguments.color_name),
                    exact=arguments.exact,
                    dataset_path=arguments.dataset,
                )
        else:
            raise ValueError(f"Unsupported command: {arguments.command}")
    except (argparse.ArgumentError, ValueError, OSError) as exc:
        return _write_error(str(exc))

    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
