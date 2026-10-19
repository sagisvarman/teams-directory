import csv, json, re, unicodedata

def clean(s):
    s = (s or "").replace("\u2010", "-").replace("\u2011", "-").replace("\u2019", "'")
    return re.sub(r"\s+", " ", s).strip()

def norm(s):
    s = unicodedata.normalize("NFKD", clean(s)).lower()
    return re.sub(r"[^a-z0-9]", "", s)

def code_of(name):
    m = re.findall(r"\(([^()]*)\)", name)
    return m[0].strip() if m else ""

# ---- teams ----
rows = list(csv.reader(open("Reference Nama Teams SBP - csv_teams.csv", encoding="utf-8")))
hdr = next(i for i, r in enumerate(rows) if r and r[0].strip() == "nama_sekolah")
schools, seen = [], {}
for r in rows[hdr + 1:]:
    if not r or not clean(r[0]):
        continue
    name = clean(r[0])
    teams_raw = r[1] if len(r) > 1 else ""
    alumni = clean(r[2]) if len(r) > 2 else ""
    teams = []
    for t in re.split(r"[,\n]", teams_raw):
        t = clean(t)
        if t and t.upper() not in [x.upper() for x in teams]:
            teams.append(t)
    key = norm(name)
    if key in seen:  # duplicate school row -> merge
        s = seen[key]
        for t in teams:
            if t.upper() not in [x.upper() for x in s["teams"]]:
                s["teams"].append(t)
        if alumni and not s["alumni"]:
            s["alumni"].append(alumni)
        continue
    s = {"school": name, "code": code_of(name), "teams": teams, "alumni": [alumni] if alumni else []}
    seen[key] = s
    schools.append(s)

# ---- alumni ----
arows = list(csv.DictReader(open("Reference Nama Teams SBP - csv_alumni.csv", encoding="utf-8")))
alumni_rows = [(clean(r["alumni_group"]), clean(r["team_name"])) for r in arows if clean(r["alumni_group"])]
alias = {}  # alumni group -> short team name
for g, t in alumni_rows:
    alias[norm(g)] = t

standalone = []
report = []
for g, t in alumni_rows:
    ng = norm(g)
    target = None
    # 1. exact alumni group already listed on a school
    for s in schools:
        if any(norm(a) == ng for a in s["alumni"]):
            target = s; break
    # 2. short name equals a team token or the school code
    if not target:
        for s in schools:
            toks = [norm(x) for x in s["teams"]] + [norm(s["code"])]
            if norm(t) in toks:
                target = s; report.append(f"{t} -> {s['school']} (token)"); break
    # 3. school code appears as a word inside the alumni group name
    if not target:
        for s in schools:
            c = s["code"]
            if c and re.search(r"(?<![A-Za-z0-9])" + re.escape(c) + r"(?![A-Za-z0-9])", g, re.I):
                target = s; report.append(f"{t} -> {s['school']} (code in name)"); break
    # 4. manual links for alumni whose short name matches no team/code
    if not target:
        manual = {"PRASASSTI": "SAKTI", "ANNADI": "SMAPK", "PASPP": "SCIPP", "AITEM": "INSOFT"}
        want = manual.get(t.upper())
        if want:
            target = next((s for s in schools if s["code"].upper() == want), None)
            if target:
                report.append(f"{t} -> {target['school']} (manual)")
    if target:
        if not any(norm(a) == ng for a in target["alumni"]):
            target["alumni"].append(g)
    else:
        standalone.append({"alumni": g, "short": t})

out = {"schools": schools, "alumniOnly": standalone}
json.dump(out, open("data.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("schools:", len(schools), "alumni rows:", len(alumni_rows), "standalone:", len(standalone))
print("\n".join(report))
print("standalone ->", [s["short"] for s in standalone])
print("schools with no teams:", sum(1 for s in schools if not s["teams"]))
