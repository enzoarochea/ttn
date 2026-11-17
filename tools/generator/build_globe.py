"""Build compact globe data from Natural Earth (world-atlas countries-50m TopoJSON).
Outputs js/globe-data.js with:
  - land dots (lat/lon, Int16 x100) denser near Central America
  - flag per dot (1 = in a country where Teltech operates)
  - border rings of GT, SV, NI, CR (simplified)
Also returns the arrays for the static SVG fallback (see render_static)."""
import json, math, base64, struct, sys

TOPO = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "package/countries-50m.json"))
OP_COUNTRIES = {"320": "Guatemala", "222": "El Salvador", "558": "Nicaragua", "188": "Costa Rica"}
USA = "840"
CENTER = (15.5, -86.0)  # lat, lon of view centre

sx, sy = TOPO["transform"]["scale"]
tx, ty = TOPO["transform"]["translate"]
arcs = []
for arc in TOPO["arcs"]:
    x = y = 0
    pts = []
    for dx, dy in arc:
        x += dx; y += dy
        pts.append((x * sx + tx, y * sy + ty))  # lon, lat
    arcs.append(pts)


def ring(idx_list):
    out = []
    for i in idx_list:
        a = arcs[i] if i >= 0 else arcs[~i][::-1]
        out.extend(a if not out else a[1:])
    return out


countries = {}
for g in TOPO["objects"]["countries"]["geometries"]:
    polys = []
    if g["type"] == "Polygon":
        polys.append([ring(r) for r in g["arcs"]])
    elif g["type"] == "MultiPolygon":
        for p in g["arcs"]:
            polys.append([ring(r) for r in p])
    countries[str(g.get("id"))] = polys


def bbox(poly):
    xs = [p[0] for p in poly[0]]; ys = [p[1] for p in poly[0]]
    return min(xs), min(ys), max(xs), max(ys)


index = []  # (bbox, polygon, country id)
for cid, polys in countries.items():
    for p in polys:
        index.append((bbox(p), p, cid))


def inside_ring(lon, lat, r):
    c = False
    j = len(r) - 1
    for i in range(len(r)):
        xi, yi = r[i]; xj, yj = r[j]
        if (yi > lat) != (yj > lat) and lon < (xj - xi) * (lat - yi) / (yj - yi + 1e-12) + xi:
            c = not c
        j = i
    return c


def country_at(lon, lat):
    for (x0, y0, x1, y1), poly, cid in index:
        if x0 <= lon <= x1 and y0 <= lat <= y1:
            if inside_ring(lon, lat, poly[0]) and not any(inside_ring(lon, lat, h) for h in poly[1:]):
                return cid
    return None


def ang_dist(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    return math.degrees(math.acos(max(-1, min(1, math.sin(p1) * math.sin(p2) + math.cos(p1) * math.cos(p2) * math.cos(dl)))))


dots = []
seen = set()


def sample(step, max_d, min_d=0):
    lat = -75.0
    while lat <= 80:
        cl = max(0.15, math.cos(math.radians(lat)))
        lstep = step / cl
        lon = -180.0
        while lon < 180:
            d = ang_dist(lat, lon, *CENTER)
            if min_d <= d < max_d:
                key = (round(lat, 2), round(lon, 2))
                if key not in seen:
                    cid = country_at(lon, lat)
                    if cid:
                        seen.add(key)
                        hot = 1 if cid in OP_COUNTRIES else (2 if cid == USA and 24 <= lat <= 31 and -88 <= lon <= -79 else 0)
                        dots.append((lat, lon, hot))
            lon += lstep
        lat += step


sample(0.42, 14)          # Central America: fine detail
sample(0.9, 34, 14)       # surrounding region
sample(1.7, 95, 34)       # rest of the visible hemisphere
print("dots", len(dots), "hot", sum(1 for d in dots if d[2]), file=sys.stderr)


def simplify(r, tol=0.06):
    out = [r[0]]
    for p in r[1:]:
        if math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) >= tol:
            out.append(p)
    return out


borders = []
for cid in OP_COUNTRIES:
    for poly in countries[cid]:
        r = simplify(poly[0])
        if len(r) > 8:
            borders.append(r)
print("border rings", len(borders), "pts", sum(len(b) for b in borders), file=sys.stderr)

# Pack: dots as Int16 (lat*100, lon*100), flags as bytes; borders as Int16 with ring lengths
dot_bytes = b"".join(struct.pack("<hh", round(d[0] * 100), round(d[1] * 100)) for d in dots)
flag_bytes = bytes(d[2] for d in dots)
border_bytes = b"".join(struct.pack("<hh", round(p[1] * 100), round(p[0] * 100)) for b in borders for p in b)
ring_lens = [len(b) for b in borders]

js = (
    "/* Globe data generated from Natural Earth 1:50m (public domain) via world-atlas (ISC).\n"
    "   dots: Int16 pairs [lat*100, lon*100]; flags: 1 = country where Teltech operates, 2 = Florida;\n"
    "   borders: Int16 pairs for GT, SV, NI, CR outlines. Regenerate with tools/generator/build_globe.py. */\n"
    "window.TELTECH_GLOBE = {\n"
    f'  dots: "{base64.b64encode(dot_bytes).decode()}",\n'
    f'  flags: "{base64.b64encode(flag_bytes).decode()}",\n'
    f'  borders: "{base64.b64encode(border_bytes).decode()}",\n'
    f"  rings: {json.dumps(ring_lens)}\n"
    "};\n"
)
open(sys.argv[2] if len(sys.argv) > 2 else "globe-data.js", "w").write(js)
json.dump({"dots": dots, "borders": [[(p[1], p[0]) for p in b] for b in borders]}, open("globe-cache.json", "w"))
print("js bytes", len(js), file=sys.stderr)
