"""sRGB, OKLab, OKLCH, sRGB gamut mapping, and relative tonal scales.

The OKLab equations and published matrix bridge are from Björn Ottosson,
“A perceptual color space for image processing,” updated 2021-01-25:
https://bottosson.github.io/posts/oklab/ . The linear-sRGB matrices are published
as public-domain/MIT reference coefficients. CSS Color 4 is used for color-space
terminology and definitions: https://www.w3.org/TR/css-color-4/ . The bounded
chroma bisection below is this engine's specified mapper; it does not claim
browser CSS gamut-mapping algorithm equivalence.
"""

from __future__ import annotations

import math
import re
from typing import Dict, NamedTuple, Optional, Sequence, Tuple


RGB_GAMUT_EPSILON = 1e-7
CHROMA_TOLERANCE = 1e-7
MAX_GAMUT_ITERATIONS = 32
ACHROMATIC_CHROMA = 1e-7
STEP_ORDER = ("50", "100", "200", "300", "400", "500", "600", "700", "800", "900", "950")
LIGHT_FACTORS = {"50": 0.96, "100": 0.88, "200": 0.72, "300": 0.52, "400": 0.28}
DARK_FACTORS = {"600": 0.15, "700": 0.30, "800": 0.45, "900": 0.60, "950": 0.75}
HEX_PATTERN = re.compile(r"#[0-9A-F]{6}\Z")


class GamutMapResult(NamedTuple):
    rgb: Tuple[float, float, float]
    chroma: float
    lower_chroma: float
    upper_chroma: float
    iterations: int
    was_mapped: bool


def _finite_triplet(values: Sequence[float], name: str) -> Tuple[float, float, float]:
    if (
        not isinstance(values, Sequence)
        or isinstance(values, (str, bytes))
        or len(values) != 3
    ):
        raise ValueError(f"{name} must contain exactly three finite numbers.")
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in values):
        raise ValueError(f"{name} must contain exactly three finite numbers.")
    result = (float(values[0]), float(values[1]), float(values[2]))
    if not all(math.isfinite(value) for value in result):
        raise ValueError(f"{name} values must be finite.")
    return result


def _signed_cuberoot(value: float) -> float:
    return math.copysign(abs(value) ** (1.0 / 3.0), value)


def _lab_from_lms_roots(l_root: float, m_root: float, s_root: float) -> Tuple[float, float, float]:
    return (
        0.2104542553 * l_root + 0.7936177850 * m_root - 0.0040720468 * s_root,
        1.9779984951 * l_root - 2.4285922050 * m_root + 0.4505937099 * s_root,
        0.0259040371 * l_root + 0.7827717662 * m_root - 0.8086757660 * s_root,
    )


def xyz_to_oklab(xyz: Sequence[float]) -> Tuple[float, float, float]:
    """Convert D65 XYZ to OKLab using the published independent matrix bridge."""
    x, y, z = _finite_triplet(xyz, "XYZ")
    l_root = _signed_cuberoot(
        0.8190224432164319 * x + 0.3619062562801221 * y - 0.12887378261216414 * z
    )
    m_root = _signed_cuberoot(
        0.0329836671980271 * x + 0.9292868468965546 * y + 0.03614466816999844 * z
    )
    s_root = _signed_cuberoot(
        0.048177199566046255 * x + 0.26423952494422764 * y + 0.6335478258136937 * z
    )
    return _finite_triplet(_lab_from_lms_roots(l_root, m_root, s_root), "OKLab result")


def linear_srgb_to_oklab(rgb: Sequence[float]) -> Tuple[float, float, float]:
    """Convert linear-light sRGB to OKLab with the published 2021 matrices."""
    red, green, blue = _finite_triplet(rgb, "linear sRGB")
    l_root = _signed_cuberoot(
        0.4122214708 * red + 0.5363325363 * green + 0.0514459929 * blue
    )
    m_root = _signed_cuberoot(
        0.2119034982 * red + 0.6806995451 * green + 0.1073969566 * blue
    )
    s_root = _signed_cuberoot(
        0.0883024619 * red + 0.2817188376 * green + 0.6299787005 * blue
    )
    return _finite_triplet(_lab_from_lms_roots(l_root, m_root, s_root), "OKLab result")


def srgb_to_oklab(rgb: Sequence[float]) -> Tuple[float, float, float]:
    """Convert normalized gamma-encoded sRGB channels in [0, 1] to OKLab."""
    channels = _finite_triplet(rgb, "sRGB")
    if any(channel < 0.0 or channel > 1.0 for channel in channels):
        raise ValueError("sRGB channels must be within [0, 1].")

    def to_linear(channel: float) -> float:
        return (
            channel / 12.92
            if channel <= 0.04045
            else ((channel + 0.055) / 1.055) ** 2.4
        )

    return linear_srgb_to_oklab(
        (to_linear(channels[0]), to_linear(channels[1]), to_linear(channels[2]))
    )


def oklab_to_srgb(lab: Sequence[float]) -> Tuple[float, float, float]:
    """Convert OKLab to gamma-encoded sRGB; out-of-gamut values stay unclipped."""
    lightness, a, b = _finite_triplet(lab, "OKLab")
    l_root = lightness + 0.3963377774 * a + 0.2158037573 * b
    m_root = lightness - 0.1055613458 * a - 0.0638541728 * b
    s_root = lightness - 0.0894841775 * a - 1.2914855480 * b
    try:
        l_value, m_value, s_value = l_root**3, m_root**3, s_root**3
    except OverflowError as exc:
        raise ValueError("OKLab values exceed the finite conversion range.") from exc
    linear_rgb = (
        4.0767416621 * l_value - 3.3077115913 * m_value + 0.2309699292 * s_value,
        -1.2684380046 * l_value + 2.6097574011 * m_value - 0.3413193965 * s_value,
        -0.0041960863 * l_value - 0.7034186147 * m_value + 1.7076147010 * s_value,
    )

    def to_srgb(channel: float) -> float:
        return (
            12.92 * channel
            if channel <= 0.0031308
            else 1.055 * channel ** (1.0 / 2.4) - 0.055
        )

    encoded = (
        to_srgb(linear_rgb[0]),
        to_srgb(linear_rgb[1]),
        to_srgb(linear_rgb[2]),
    )
    if not all(math.isfinite(channel) for channel in encoded):
        raise ValueError("OKLab conversion produced non-finite sRGB channels.")
    return encoded


def oklab_to_oklch(lab: Sequence[float]) -> Tuple[float, float, Optional[float]]:
    """Convert OKLab to OKLCH; near-achromatic colors have hue=None."""
    lightness, a, b = _finite_triplet(lab, "OKLab")
    chroma = math.hypot(a, b)
    if not math.isfinite(chroma):
        raise ValueError("OKLab chroma must be finite.")
    if chroma <= ACHROMATIC_CHROMA:
        return lightness, chroma, None
    hue = math.degrees(math.atan2(b, a)) % 360.0
    return lightness, chroma, hue


def oklch_to_oklab(lch: Sequence[Optional[float]]) -> Tuple[float, float, float]:
    """Convert OKLCH (hue in degrees) to OKLab, canonicalizing achromatics."""
    if (
        not isinstance(lch, Sequence)
        or isinstance(lch, (str, bytes))
        or len(lch) != 3
    ):
        raise ValueError("OKLCH must contain finite L/C and a finite hue or None.")
    lightness, chroma = lch[0], lch[1]
    hue = lch[2]
    if (
        isinstance(lightness, bool)
        or not isinstance(lightness, (int, float))
        or isinstance(chroma, bool)
        or not isinstance(chroma, (int, float))
    ):
        raise ValueError("OKLCH lightness and chroma must be finite numbers.")
    lightness = float(lightness)
    chroma = float(chroma)
    if not math.isfinite(lightness) or not math.isfinite(chroma):
        raise ValueError("OKLCH lightness and chroma must be finite.")
    if not 0.0 <= lightness <= 1.0:
        raise ValueError("OKLCH lightness must be within [0, 1].")
    if chroma < 0.0:
        raise ValueError("OKLCH chroma must be non-negative.")
    if chroma <= ACHROMATIC_CHROMA:
        return lightness, 0.0, 0.0
    if hue is None or isinstance(hue, bool) or not isinstance(hue, (int, float)):
        raise ValueError("A finite hue is required when OKLCH chroma exceeds 1e-7.")
    hue = float(hue)
    if not math.isfinite(hue):
        raise ValueError("OKLCH hue must be finite.")
    radians = math.radians(hue)
    return lightness, chroma * math.cos(radians), chroma * math.sin(radians)


def oklch_to_srgb(lch: Sequence[Optional[float]]) -> Tuple[float, float, float]:
    """Convert OKLCH to unclipped gamma-encoded sRGB."""
    return oklab_to_srgb(oklch_to_oklab(lch))


def is_in_srgb_gamut(rgb: Sequence[float]) -> bool:
    """Test sRGB gamut with the contract's channel noise epsilon only."""
    channels = _finite_triplet(rgb, "sRGB gamut candidate")
    return all(
        -RGB_GAMUT_EPSILON <= channel <= 1.0 + RGB_GAMUT_EPSILON
        for channel in channels
    )


def _clamp_gamut_noise(rgb: Sequence[float]) -> Tuple[float, float, float]:
    red, green, blue = _finite_triplet(rgb, "sRGB gamut result")
    if not is_in_srgb_gamut((red, green, blue)):
        raise ValueError("Cannot clamp an sRGB channel outside the gamut tolerance.")
    return (
        min(1.0, max(0.0, red)),
        min(1.0, max(0.0, green)),
        min(1.0, max(0.0, blue)),
    )


def gamut_map_oklch(lch: Sequence[Optional[float]]) -> GamutMapResult:
    """Reduce chroma at fixed L/h with a bounded in-gamut/out-of-gamut bracket."""
    if (
        not isinstance(lch, Sequence)
        or isinstance(lch, (str, bytes))
        or len(lch) != 3
    ):
        raise ValueError("OKLCH must contain finite L/C and a finite hue or None.")
    lightness, chroma, hue = lch
    if (
        isinstance(lightness, bool)
        or not isinstance(lightness, (int, float))
        or isinstance(chroma, bool)
        or not isinstance(chroma, (int, float))
    ):
        raise ValueError("OKLCH lightness and chroma must be finite numbers.")
    lightness = float(lightness)
    chroma = float(chroma)
    if not math.isfinite(lightness) or not math.isfinite(chroma):
        raise ValueError("OKLCH lightness and chroma must be finite.")
    if not 0.0 <= lightness <= 1.0:
        raise ValueError("OKLCH lightness must be within [0, 1].")
    if chroma < 0.0:
        raise ValueError("OKLCH chroma must be non-negative.")
    if chroma <= ACHROMATIC_CHROMA:
        hue = None
    elif hue is None or isinstance(hue, bool) or not isinstance(hue, (int, float)):
        raise ValueError("A finite hue is required when OKLCH chroma exceeds 1e-7.")
    elif not math.isfinite(float(hue)):
        raise ValueError("OKLCH hue must be finite.")
    normalized_hue = None if hue is None else float(hue) % 360.0
    target = (lightness, chroma, normalized_hue)
    target_rgb = oklch_to_srgb(target)
    if is_in_srgb_gamut(target_rgb):
        return GamutMapResult(
            _clamp_gamut_noise(target_rgb), chroma, chroma, chroma, 0, False
        )

    lower = 0.0
    upper = chroma
    lower_rgb = oklch_to_srgb((lightness, lower, None))
    if not is_in_srgb_gamut(lower_rgb):
        raise ValueError("Neutral OKLCH color is outside sRGB gamut; cannot map chroma.")

    iterations = 0
    while upper - lower > CHROMA_TOLERANCE and iterations < MAX_GAMUT_ITERATIONS:
        midpoint = lower + (upper - lower) / 2.0
        midpoint_rgb = oklch_to_srgb((lightness, midpoint, normalized_hue))
        if is_in_srgb_gamut(midpoint_rgb):
            lower = midpoint
            lower_rgb = midpoint_rgb
        else:
            upper = midpoint
        iterations += 1

    if upper - lower > CHROMA_TOLERANCE:
        raise ValueError(
            "OKLCH gamut mapping did not converge within 32 iterations and 1e-7 chroma."
        )
    if not is_in_srgb_gamut(lower_rgb):
        raise ValueError("OKLCH gamut mapping lost its in-gamut lower bound.")
    if is_in_srgb_gamut(oklch_to_srgb((lightness, upper, normalized_hue))):
        raise ValueError("OKLCH gamut mapping lost its out-of-gamut upper bound.")
    return GamutMapResult(
        _clamp_gamut_noise(lower_rgb), lower, lower, upper, iterations, True
    )


def srgb_to_hex(rgb: Sequence[float]) -> str:
    """Quantize in-gamut normalized sRGB to nearest 8-bit channels via round()."""
    red, green, blue = _clamp_gamut_noise(rgb)
    return "#" + "".join(f"{round(channel * 255):02X}" for channel in (red, green, blue))


def scale_targets(
    base_lab: Sequence[float],
) -> Dict[str, Tuple[float, float, Optional[float]]]:
    """Return the frozen plan-relative OKLCH curve for all eleven scale steps."""
    base_lightness, base_chroma, base_hue = oklab_to_oklch(base_lab)
    targets: Dict[str, Tuple[float, float, Optional[float]]] = {}
    for step in ("50", "100", "200", "300", "400"):
        factor = LIGHT_FACTORS[step]
        targets[step] = (
            base_lightness + (1.0 - base_lightness) * factor,
            base_chroma * (1.0 - factor),
            base_hue,
        )
    targets["500"] = (base_lightness, base_chroma, base_hue)
    for step in ("600", "700", "800", "900", "950"):
        factor = DARK_FACTORS[step]
        targets[step] = (
            base_lightness * (1.0 - factor),
            base_chroma * (1.0 - factor),
            base_hue,
        )
    return targets


def generate_scale(base_hex: str, base_lab: Sequence[float]) -> Dict[str, object]:
    """Build a base-anchored, gamut-mapped OKLCH scale from validated inputs."""
    if not isinstance(base_hex, str) or not HEX_PATTERN.fullmatch(base_hex):
        raise ValueError("Scale base must be a normalized uppercase #RRGGBB color.")
    base_values = _finite_triplet(base_lab, "base OKLab")
    targets = scale_targets(base_values)
    steps: Dict[str, str] = {}
    collapsed_steps = []
    seen = set()
    for step in STEP_ORDER:
        if step == "500":
            output = base_hex
        else:
            mapped = gamut_map_oklch(targets[step])
            output = srgb_to_hex(mapped.rgb)
        steps[step] = output
        if output in seen:
            collapsed_steps.append(step)
        seen.add(output)
    return {
        "base": base_hex,
        "space": "oklch",
        "anchor": 500,
        "steps": steps,
        "collapsed_steps": collapsed_steps,
    }
