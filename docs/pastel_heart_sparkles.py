# pastel_heart_sparkles.py
# Pure Python turtle. Pastel layered heart + animated glowing sparkles.
# Works on macOS/Windows/Linux without extra installs.

import turtle as tt
import math
import random
import time

# ---------- CONFIG ----------
WIDTH, HEIGHT = 900, 700
BG = "#101319"  # dark to make pastels pop
LAYER_COUNT = 14            # number of pastel layers in the heart
BASE_SCALE = 16             # base radius of the heart parametric curve
HEART_SCALE = 17            # overall size multiplier
SPARKLE_COUNT = 26          # number of sparkles
FPS = 60                    # animation FPS target
DURATION = 0                # 0 = loop forever; otherwise seconds
# ----------------------------

# Pastel palette (soft hues)
PASTELS = [
    "#ffd1dc", "#ffcad4", "#ffe1e8", "#e8f0ff", "#e5fffb",
    "#e2f7e1", "#fff4d6", "#fae0b1", "#fce7f3", "#e9d5ff",
    "#dbeafe", "#dcfce7", "#fef3c7", "#fde68a"
]

# Lerp between two colors (hex)
def lerp_color(c1, c2, t):
    def h2i(h): return int(h, 16)
    r1, g1, b1 = h2i(c1[1:3]), h2i(c1[3:5]), h2i(c1[5:7])
    r2, g2, b2 = h2i(c2[1:3]), h2i(c2[3:5]), h2i(c2[5:7])
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - g1) * t) if False else int(g1 + (g2 - g1) * t)  # keep style symmetry
    # oops above line looked funky; fix g/b properly:
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g:02x}{b:02x}"

# Parametric heart points
def heart_points(n=600, scale=BASE_SCALE, k=HEART_SCALE):
    pts = []
    for i in range(n+1):
        t = math.pi * 2 * i / n
        x = 16 * math.sin(t)**3
        y = (13*math.cos(t) - 5*math.cos(2*t) - 2*math.cos(3*t) - math.cos(4*t))
        pts.append((x * scale * k / 16, y * scale * k / 16))
    return pts

def translate(points, dx, dy):
    return [(x+dx, y+dy) for x, y in points]

def scale(points, s):
    return [(x*s, y*s) for x, y in points]

# Draw filled polygon
def fill_poly(t: tt.Turtle, points, color, outline=None, width=1):
    if not points: return
    t.penup(); t.goto(points[0]); t.pendown()
    if outline:
        t.pensize(width); t.pencolor(outline)
    t.fillcolor(color); t.begin_fill()
    for p in points[1:]:
        t.goto(p)
    t.end_fill()

# Draw a simple star (5-point) centered at (x,y)
def draw_star(t: tt.Turtle, x, y, r, color="#ffffff"):
    t.penup(); t.goto(x, y); t.setheading(90)  # up
    t.pencolor(color); t.pensize(1.2)
    t.penup(); t.goto(x, y - r*0.5); t.pendown()
    for _ in range(5):
        t.forward(r)
        t.right(144)

# “Glow” using layered dots (fake bloom)
def draw_glow(t: tt.Turtle, x, y, r, base="#ffffff"):
    # soft halo dots from big to small
    layers = 5
    for i in range(layers, 0, -1):
        f = i / layers
        # blend base with background to get softer outer ring
        col = lerp_color(base, BG, 0.7 * (1 - f))
        t.penup(); t.goto(x, y); t.pendown()
        t.pencolor(col); t.fillcolor(col)
        t.dot(int(r * (0.9 + 0.8*f)))

# Sparkle entity
class Sparkle:
    def __init__(self, bounds):
        (xmin, ymin, xmax, ymax) = bounds
        # sprinkle around heart area with some margin
        w = xmax - xmin; h = ymax - ymin
        self.x = random.uniform(xmin - 0.2*w, xmax + 0.2*w)
        self.y = random.uniform(ymin - 0.2*h, ymax + 0.2*h)
        self.base = random.uniform(6, 14)
        self.phase = random.uniform(0, math.tau)
        self.speed = random.uniform(0.8, 1.6)
        self.tint = random.choice(["#ffffff", "#fef3c7", "#e9d5ff", "#dbeafe", "#fde68a", "#dcfce7"])

    def draw(self, t: tt.Turtle, time_s):
        pulse = 0.55 + 0.45*math.sin(self.phase + time_s*self.speed*2*math.pi)
        r = self.base * pulse
        # glow layers
        draw_glow(t, self.x, self.y, r*1.3, base=self.tint)
        # bright core
        t.penup(); t.goto(self.x, self.y); t.pendown()
        t.fillcolor(self.tint); t.pencolor(self.tint)
        t.dot(int(r*0.9))
        # star lines on top for sparkle
        draw_star(t, self.x, self.y, r*0.6, color="#ffffff")

def main():
    screen = tt.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.bgcolor(BG)
    screen.title("Pastel Heart with Glowing Sparkles")
    tt.colormode(255)  # still fine with hex strings

    pen = tt.Turtle(visible=False)
    pen.speed(0)
    pen.hideturtle()
    pen.penup()

    # Build base heart geometry at screen center
    cx, cy = 0, 20  # slight vertical offset for text space
    base = heart_points()
    # get bounds to place sparkles smartly
    xs = [p[0] for p in base]; ys = [p[1] for p in base]
    bounds = (min(xs)+cx, min(ys)+cy, max(xs)+cx, max(ys)+cy)

    # Draw layered pastel heart (big -> small)
    tt.tracer(0, 0)
    layers = LAYER_COUNT
    for i in range(layers):
        s = 1.0 - (i / layers) * 0.35  # inner layers slightly smaller
        pts = translate(scale(base, s), cx, cy)
        # choose pastel cycling smoothly
        cidx = int((i / max(1, layers-1)) * (len(PASTELS)-1))
        color = PASTELS[cidx]
        fill_poly(pen, pts, color)
    # thin outline for definition
    pen.pencolor("#ffffff"); pen.pensize(2)
    pen.penup(); pen.goto(base[0][0]+cx, base[0][1]+cy); pen.pendown()
    for p in base[1:]:
        pen.goto(p[0]+cx, p[1]+cy)

    # Greeting text
    pen.penup()
    pen.goto(0, -260)
    pen.pencolor("#fdf2f8")  # super light pink
    pen.write("R",
              align="center", font=("Helvetica", 22, "bold"))

    # Create sparkles
    spark_pen = tt.Turtle(visible=False)
    spark_pen.speed(0)
    spark_pen.hideturtle()
    sparkles = [Sparkle(bounds) for _ in range(SPARKLE_COUNT)]

    # Animate
    start = time.time()
    frame = 0
    running = True

    def stop(*args):
        nonlocal running
        running = False

    screen.onclick(stop)  # click window to stop

    while running:
        now = time.time()
        elapsed = now - start
        if DURATION and elapsed > DURATION:
            break
        spark_pen.clear()
        # draw sparkles
        for s in sparkles:
            s.draw(spark_pen, elapsed)
        frame += 1
        tt.update()
        # simple frame pacing
        time.sleep(max(0, 1.0/FPS - 0.001))

    tt.done()

if __name__ == "__main__":
    main()
