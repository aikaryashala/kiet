"""Generates the three SQL files for kiet-bootcamp-3/data/.
Deterministic (fixed seed). Run once; the SQL files are the artifact."""
import random, os, collections

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "kiet-bootcamp-3", "data"))
os.makedirs(OUT, exist_ok=True)

CREATE = """CREATE TABLE students (
    student_name TEXT,
    inter_college TEXT,
    inter_city TEXT
);
"""

def q(s):
    return "'" + s.replace("'", "''") + "'"

def insert(name, college, city):
    return f"INSERT INTO students VALUES ({q(name)}, {q(college)}, {q(city)});\n"

# ---------- schema.sql ----------
open(f"{OUT}/schema.sql", "w").write(
    "-- The one table used in every stage of this bootcamp.\n"
    "-- Three text columns, no id. Same text in sample_team_details.sql and all_students.sql.\n"
    + CREATE)

# ---------- sample_team_details.sql ----------
SAMPLE = [
    ("Ravi Teja Kanchi",         "Sri Chaitanya Junior College", "Visakhapatnam"),
    ("Lakshmi Prasanna Gudla",   "Narayana Junior College",      "Vijayawada"),
    ("Sai Kiran Bommu",          "Sri Chaitanya Junior College", "Visakhapatnam"),
    ("Divya Sree Pothula",       "Narayana Junior College",      "Vijayawada"),
]
s = ("-- A 4-student example team: 2 colleges, 2 cities.\n"
     "-- Every Expected output in the material uses exactly these rows.\n"
     "-- Use this only if you skipped Stage 1:\n"
     "--     sqlite3 team_details.db < sample_team_details.sql\n"
     + CREATE + "\n")
for r in SAMPLE:
    s += insert(*r)
open(f"{OUT}/sample_team_details.sql", "w").write(s)

# ---------- all_students.sql ----------

COLLEGES = [
    "Sri Chaitanya Junior College", "Narayana Junior College", "NRI Junior College",
    "Bhashyam Junior College", "Tirumala Junior College", "Vignan Junior College",
    "Sri Gayatri Junior College", "Krishnaveni Junior College", "Sasi Junior College",
    "Sri Prakash Junior College", "Aditya Junior College", "Government Junior College",
]
CITIES = ["Visakhapatnam", "Vijayawada", "Guntur", "Kakinada",
          "Rajahmundry", "Nellore", "Tirupati", "Kurnool"]

ONLY_ONE_CITY_COLLEGE = "Sri Prakash Junior College"   # appears only in Kakinada
ONLY_ONE_COLLEGE_CITY = "Kurnool"                      # has only Narayana Junior College

# Which colleges exist in which city (uneven on purpose).
PRESENCE = {
    "Visakhapatnam": ["Sri Chaitanya Junior College", "Narayana Junior College", "Bhashyam Junior College",
                      "Tirumala Junior College", "Sri Gayatri Junior College", "Government Junior College"],
    "Vijayawada":    ["Sri Chaitanya Junior College", "Narayana Junior College", "NRI Junior College",
                      "Bhashyam Junior College", "Krishnaveni Junior College", "Vignan Junior College"],
    "Guntur":        ["Sri Chaitanya Junior College", "Narayana Junior College", "NRI Junior College",
                      "Vignan Junior College", "Government Junior College", "Sasi Junior College"],
    "Kakinada":      ["Sri Chaitanya Junior College", "Aditya Junior College", "Sri Prakash Junior College",
                      "Government Junior College"],
    "Rajahmundry":   ["Sri Chaitanya Junior College", "Narayana Junior College", "Aditya Junior College",
                      "Sasi Junior College"],
    "Nellore":       ["Narayana Junior College", "Sri Chaitanya Junior College", "Krishnaveni Junior College"],
    "Tirupati":      ["Sri Chaitanya Junior College", "Narayana Junior College", "Sri Gayatri Junior College",
                      "Tirumala Junior College"],
    "Kurnool":       ["Narayana Junior College"],
}
# City weights: how many of the 200 go to each city (uneven).
CITY_ROWS = {"Visakhapatnam": 46, "Vijayawada": 41, "Guntur": 30, "Kakinada": 24,
             "Rajahmundry": 20, "Nellore": 16, "Tirupati": 14, "Kurnool": 9}
assert sum(CITY_ROWS.values()) == 200

M_FIRST = ["Ravi", "Sai", "Kiran", "Harsha", "Chaitanya", "Deepak", "Eswar", "Gowtham", "Hemanth",
           "Karthik", "Manoj", "Naveen", "Nikhil", "Pavan", "Pradeep", "Rajesh", "Sandeep", "Santhosh",
           "Srinivas", "Suresh", "Tarun", "Uday", "Vamsi", "Varun", "Venkat", "Vijay", "Vinay", "Akhil",
           "Bhargav", "Charan", "Dinesh", "Ganesh", "Praveen", "Rohith", "Siva", "Yaswanth", "Ashok",
           "Girish", "Jagadeesh", "Mahesh", "Phani", "Rakesh", "Arun", "Balaji", "Gopi", "Hari", "Kishore",
           "Murali", "Nagendra", "Prakash", "Ramesh", "Sekhar", "Sudheer", "Teja", "Yugandhar"]
M_TAIL  = ["Kumar", "Teja", "Krishna", "Prasad", "Babu", "Sai", "Chandra", "Surya", "Satya", "Venkata",
           "Naga", "Vardhan", "Kiran", "Rama", "Mohan", "Anand", "Reddy", "Charan"]
F_FIRST = ["Lakshmi", "Divya", "Anusha", "Bhavani", "Indu", "Jyothi", "Lavanya", "Madhavi", "Ramya",
           "Sowmya", "Swathi", "Yamini", "Harika", "Keerthi", "Mounika", "Nandini", "Pooja", "Sahithi",
           "Sruthi", "Tejaswini", "Bindu", "Kavya", "Neelima", "Sindhu", "Aishwarya", "Chandana", "Deepika",
           "Gayathri", "Hima", "Jahnavi", "Manasa", "Meghana", "Navya", "Pallavi", "Rashmi", "Sirisha",
           "Sneha", "Srilatha", "Supriya", "Usha", "Vasavi", "Vennela"]
F_TAIL  = ["Prasanna", "Sree", "Priya", "Devi", "Sri", "Lakshmi", "Durga", "Bhavani", "Kumari", "Rani",
           "Sai", "Varshini", "Harini", "Madhuri", "Sindhu"]
SUR = ["Kanchi", "Gudla", "Bommu", "Pothula", "Reddy", "Naidu", "Chowdary", "Yadav", "Rao", "Varma",
       "Sharma", "Gupta", "Kumar", "Prasad", "Murthy", "Sastry", "Babu", "Achari", "Goud", "Setty",
       "Pilla", "Pothana", "Vemula", "Kota", "Peddi", "Nalluri", "Tadi", "Kondapalli", "Boddu", "Mallela",
       "Gorantla", "Chintala", "Puli", "Bhimavarapu", "Dasari", "Jampala", "Kakarla", "Lanka", "Meka",
       "Nadella", "Palla", "Ravella", "Sunkara", "Tummala", "Uppala", "Vasireddy", "Yarlagadda", "Zilla",
       "Annam", "Bezawada"]

def generate(seed):
    random.seed(seed)
    used = set(n for n, _, _ in SAMPLE)
    rows = []
    for city, n in CITY_ROWS.items():
        cols = PRESENCE[city]
        weights = [len(cols) - i for i in range(len(cols))]   # first listed college gets the biggest share
        for _ in range(n):
            college = random.choices(cols, weights=weights)[0]
            while True:
                if random.random() < 0.55:
                    name = f"{random.choice(M_FIRST)} {random.choice(M_TAIL)} {random.choice(SUR)}"
                else:
                    name = f"{random.choice(F_FIRST)} {random.choice(F_TAIL)} {random.choice(SUR)}"
                if name not in used and len(set(name.split())) == 3:
                    used.add(name); break
            rows.append((name, college, city))
    random.shuffle(rows)
    return rows

def ok(rows):
    per_college = collections.Counter(c for _, c, _ in rows)
    per_city = collections.Counter(c for _, _, c in rows)
    cities_of = collections.defaultdict(set); colleges_in = collections.defaultdict(set)
    for _, c, t in rows:
        cities_of[c].add(t); colleges_in[t].add(c)
    if len(rows) != 200 or len(set(n for n, _, _ in rows)) != 200: return False
    if set(per_college) != set(COLLEGES) or set(per_city) != set(CITIES): return False
    if [c for c in COLLEGES if len(cities_of[c]) == 1] != [ONLY_ONE_CITY_COLLEGE]: return False
    if [t for t in CITIES if len(colleges_in[t]) == 1] != [ONLY_ONE_COLLEGE_CITY]: return False
    if len(set(per_college.values())) != len(per_college): return False
    if len(set(per_city.values())) != len(per_city): return False
    if min(per_college.values()) < 3: return False
    pairs = collections.Counter((c, t) for _, c, t in rows)
    if pairs[(ONLY_ONE_CITY_COLLEGE, "Kakinada")] < 3: return False
    return True

seed = 20260921
while True:
    rows = generate(seed)
    if ok(rows): break
    seed += 1
print("seed", seed)
per_college = collections.Counter(c for _, c, _ in rows)
per_city = collections.Counter(c for _, _, c in rows)
pairs = collections.Counter((c, t) for _, c, t in rows)

hdr = ["-- all_students.sql — 200 students across 12 intermediate colleges and 8 cities.",
       "-- Build the database:   sqlite3 all_students.db < all_students.sql",
       "--",
       "-- Exact counts (quoted by the material's Expected output blocks):",
       "--   total rows: 200",
       "--",
       "--   per college (SELECT inter_college, COUNT(*) FROM students GROUP BY inter_college ORDER BY inter_college):"]
for c in sorted(COLLEGES):
    hdr.append(f"--     {c:<32} {per_college[c]:>3}")
hdr.append("--")
hdr.append("--   per city (SELECT inter_city, COUNT(*) FROM students GROUP BY inter_city ORDER BY inter_city):")
for t in sorted(CITIES):
    hdr.append(f"--     {t:<32} {per_city[t]:>3}")
hdr.append("--")
hdr.append(f"--   {ONLY_ONE_CITY_COLLEGE} appears in exactly one city: Kakinada ({pairs[(ONLY_ONE_CITY_COLLEGE, 'Kakinada')]} rows).")
hdr.append(f"--   {ONLY_ONE_COLLEGE_CITY} has exactly one college: Narayana Junior College ({pairs[('Narayana Junior College', ONLY_ONE_COLLEGE_CITY)]} rows).")
hdr.append("--")
hdr.append("--   college x city (rows):")
for c in sorted(COLLEGES):
    cells = ", ".join(f"{t} {pairs[(c, t)]}" for t in CITIES if pairs[(c, t)])
    hdr.append(f"--     {c}: {cells}")
hdr.append("")

s = "\n".join(hdr) + CREATE + "\n"
for r in rows:
    s += insert(*r)
open(f"{OUT}/all_students.sql", "w").write(s)
print("written", len(rows), "rows")
