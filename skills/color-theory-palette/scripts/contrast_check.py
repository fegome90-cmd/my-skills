#!/usr/bin/env python3
"""Verificador de contraste WCAG 2.2 y generador de rampas 100-900 (+150).

Sin dependencias (solo biblioteca estandar). Uso:

  python3 contrast_check.py pair <fg> <bg>
      Calcula el ratio de contraste entre dos colores HEX e indica que
      umbrales WCAG cumple (texto normal 4.5:1 / 7:1, texto grande y UI 3:1).

  python3 contrast_check.py ramp <base>
      Genera la rampa 100-900 (+150) mezclando la base con blanco (100-400)
      y con negro (600-900) segun la tabla de la skill, y reporta el
      contraste de cada paso contra blanco y contra el paso 900.
      Marca en que pasos el texto blanco alcanza 4.5:1, para elegir el
      paso de CTA en vez de asumirlo.

Los colores se aceptan como #RRGGBB, RRGGBB o #RGB.
"""
import sys

# Porcentaje de color base en cada paso (resto: blanco hasta 400, negro desde 600)
MIX = [
    ("100", 0.10, "white"),
    ("150", 0.16, "white"),
    ("200", 0.25, "white"),
    ("300", 0.45, "white"),
    ("400", 0.70, "white"),
    ("500", 1.00, None),
    ("600", 0.82, "black"),
    ("700", 0.64, "black"),
    ("800", 0.42, "black"),
    ("900", 0.22, "black"),
]


def parse_hex(value):
    h = value.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError(f"Color HEX invalido: {value}")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def to_hex(rgb):
    return "#" + "".join(f"{round(c):02X}" for c in rgb)


def luminance(rgb):
    def channel(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def verdict(r):
    marks = []
    marks.append("AA texto" if r >= 4.5 else "falla AA texto")
    if r >= 7:
        marks.append("AAA texto")
    marks.append("AA grande/UI" if r >= 3 else "falla grande/UI")
    return ", ".join(marks)


def mix(base, amount, other):
    if other is None:
        return base
    target = (255, 255, 255) if other == "white" else (0, 0, 0)
    return tuple(round(amount * b + (1 - amount) * t) for b, t in zip(base, target))


def cmd_pair(fg, bg):
    r = ratio(parse_hex(fg), parse_hex(bg))
    print(f"{fg} sobre {bg}: {r:.2f}:1 -> {verdict(r)}")


def cmd_ramp(base_hex):
    base = parse_hex(base_hex)
    steps = [(name, mix(base, amt, other)) for name, amt, other in MIX]
    ink = dict(steps)["900"]
    white = (255, 255, 255)
    print(f"Rampa desde {base_hex.upper()} (paso 500)")
    print(f"{'paso':<5} {'hex':<8} {'vs blanco':>10} {'vs 900':>8}  texto blanco 4.5:1")
    first_ok = None
    for name, rgb in steps:
        rw, rk = ratio(rgb, white), ratio(rgb, ink)
        ok = rw >= 4.5
        if ok and first_ok is None:
            first_ok = name
        print(f"{name:<5} {to_hex(rgb):<8} {rw:>9.2f} {rk:>8.2f}  {'si' if ok else 'no'}")
    if first_ok:
        print(f"\nPrimer paso con texto blanco >= 4.5:1: {first_ok}. Usalo como CTA de Light Mode.")
    else:
        print("\nNingun paso alcanza 4.5:1 con texto blanco: usa texto oscuro (paso 900).")


def main(argv):
    if len(argv) == 4 and argv[1] == "pair":
        cmd_pair(argv[2], argv[3])
    elif len(argv) == 3 and argv[1] == "ramp":
        cmd_ramp(argv[2])
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
