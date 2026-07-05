"""Generates assets/icon.ico — a polished TF2-orange app icon: crossed wrench
and screwdriver (a "multi-tool / swiss army knife" motif) on a glossy rounded
tile. Rendered at high resolution and downscaled for clean edges at every size.

    python assets/make_icon.py
"""

import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

R = 1024                      # supersampled work canvas
S = R / 256.0                 # coords below are in 256-space, scaled by S

BG_TOP = (255, 172, 76)
BG_BOTTOM = (198, 92, 28)
RIM = (128, 58, 18)
CREAM = (247, 242, 230)
RED = (210, 64, 52)


def _sc(coords):
    """Scale a flat [x0,y0,x1,y1,...] list or a list of (x, y) point tuples."""
    if coords and isinstance(coords[0], (tuple, list)):
        return [(x * S, y * S) for x, y in coords]
    return [v * S for v in coords]


def _rounded_mask(size, radius):
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size - 1, size - 1],
                                        radius=radius, fill=255)
    return m


def _gradient_bg(size, top, bottom):
    ramp = np.linspace(0.0, 1.0, size)[:, None]
    rows = (np.array(top) * (1 - ramp) + np.array(bottom) * ramp)
    arr = np.repeat(rows[:, None, :], size, axis=1).astype(np.uint8)
    return Image.fromarray(arr, "RGB")


def _wrench_layer():
    """Upright open-end wrench (cream) on its own RGBA layer, rotated. Jaw
    opens at the top so it reads unmistakably as a wrench, not a ring."""
    mask = Image.new("L", (R, R), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse(_sc([86, 24, 170, 108]), fill=255)                 # head disc
    d.rounded_rectangle(_sc([116, 60, 140, 214]), radius=12 * S, fill=255)
    d.ellipse(_sc([106, 44, 150, 88]), fill=0)                   # jaw hole
    d.polygon(_sc([(110, 20), (146, 20), (140, 66), (116, 66)]), fill=0)  # mouth
    layer = Image.new("RGBA", (R, R), (0, 0, 0, 0))
    layer.paste(Image.new("RGBA", (R, R), CREAM + (255,)), (0, 0), mask)
    return layer.rotate(35, resample=Image.BICUBIC, center=(R / 2, R / 2))


def _screwdriver_layer():
    """Upright screwdriver: steel shaft/tip + red grip, rotated the other way."""
    steel = Image.new("L", (R, R), 0)
    ds = ImageDraw.Draw(steel)
    ds.rectangle(_sc([122, 58, 134, 150]), fill=255)                 # shaft
    ds.polygon(_sc([(118, 46), (138, 46), (133, 60), (123, 60)]), fill=255)  # tip
    ds.rectangle(_sc([119, 142, 137, 154]), fill=255)               # collar

    grip = Image.new("L", (R, R), 0)
    ImageDraw.Draw(grip).rounded_rectangle(_sc([107, 150, 149, 216]),
                                           radius=15 * S, fill=255)

    layer = Image.new("RGBA", (R, R), (0, 0, 0, 0))
    layer.paste(Image.new("RGBA", (R, R), RED + (255,)), (0, 0), grip)
    layer.paste(Image.new("RGBA", (R, R), CREAM + (255,)), (0, 0), steel)
    return layer.rotate(-32, resample=Image.BICUBIC, center=(R / 2, R / 2))


def build() -> Image.Image:
    mask = _rounded_mask(R, int(R * 0.225))
    icon = Image.new("RGBA", (R, R), (0, 0, 0, 0))

    # gradient body
    icon.paste(_gradient_bg(R, BG_TOP, BG_BOTTOM), (0, 0), mask)

    # top gloss highlight
    gloss = Image.new("L", (R, R), 0)
    ImageDraw.Draw(gloss).ellipse(_sc([26, 10, 230, 150]), fill=70)
    gloss = gloss.filter(ImageFilter.GaussianBlur(R / 60))
    gloss = Image.composite(gloss, Image.new("L", (R, R), 0), mask)
    icon.paste(Image.new("RGBA", (R, R), (255, 255, 255, 255)), (0, 0), gloss)

    wrench = _wrench_layer()
    screw = _screwdriver_layer()
    tools_alpha = Image.new("L", (R, R), 0)
    tools_alpha = Image.composite(Image.new("L", (R, R), 255), tools_alpha,
                                  Image.alpha_composite(wrench, screw).split()[3])

    # drop shadow under the tools
    shadow = tools_alpha.point(lambda a: a * 42 // 100)
    shadow = shadow.filter(ImageFilter.GaussianBlur(R / 90))
    shadow_rgba = Image.new("RGBA", (R, R), (40, 18, 6, 0))
    shadow_rgba.putalpha(shadow)
    shadow_rgba = Image.composite(
        shadow_rgba, Image.new("RGBA", (R, R), (0, 0, 0, 0)), mask)
    icon = Image.alpha_composite(icon, _offset(shadow_rgba, int(6 * S), int(8 * S)))

    icon = Image.alpha_composite(icon, screw)
    icon = Image.alpha_composite(icon, wrench)

    # inner rim
    rim = Image.new("RGBA", (R, R), (0, 0, 0, 0))
    ImageDraw.Draw(rim).rounded_rectangle(
        [int(3 * S), int(3 * S), R - int(3 * S), R - int(3 * S)],
        radius=int(R * 0.2), outline=RIM + (255,), width=int(4 * S))
    icon = Image.alpha_composite(icon, rim)
    return icon


def _offset(img, dx, dy):
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.paste(img, (dx, dy))
    return out


def main():
    icon = build().resize((256, 256), Image.LANCZOS)
    here = os.path.dirname(os.path.abspath(__file__))
    icon.save(os.path.join(here, "icon.png"))  # handy for README/preview
    icon.save(os.path.join(here, "icon.ico"),
              sizes=[(16, 16), (24, 24), (32, 32), (48, 48),
                     (64, 64), (128, 128), (256, 256)])
    print(f"yazildi: {os.path.join(here, 'icon.ico')}")


if __name__ == "__main__":
    main()
