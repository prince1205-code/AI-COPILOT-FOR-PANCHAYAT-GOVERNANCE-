"""
Test EligibilityEngine on 25 real-world citizen profiles.
Run: python scripts/test_recommendations.py
"""
import sys
sys.path.insert(0, ".")

from src.recommendation.eligibility_engine import EligibilityEngine

engine = EligibilityEngine()

TEST_PROFILES = [
    # --- FARMERS ---
    {"id": 1,  "label": "Young farmer, UP, low income",         "age": 24, "state": "Uttar Pradesh",  "occupation": "Farmer",  "income": 80000,  "gender": "male"},
    {"id": 2,  "label": "Senior farmer, Punjab, medium income", "age": 62, "state": "Punjab",          "occupation": "Farmer",  "income": 150000, "gender": "male"},
    {"id": 3,  "label": "Female farmer, Bihar, very low income","age": 35, "state": "Bihar",           "occupation": "Farmer",  "income": 60000,  "gender": "female"},
    {"id": 4,  "label": "Farmer, Rajasthan, no income given",   "age": 45, "state": "Rajasthan",       "occupation": "Farmer",  "income": None,   "gender": "male"},
    {"id": 5,  "label": "Farmer, Maharashtra, above threshold", "age": 50, "state": "Maharashtra",     "occupation": "Farmer",  "income": 350000, "gender": "male"},

    # --- STUDENTS ---
    {"id": 6,  "label": "Student, Delhi, male",                 "age": 19, "state": "Delhi",           "occupation": "Student", "income": 120000, "gender": "male"},
    {"id": 7,  "label": "Student, Tamil Nadu, female",          "age": 21, "state": "Tamil Nadu",      "occupation": "Student", "income": 90000,  "gender": "female"},
    {"id": 8,  "label": "Student, West Bengal, low income",     "age": 17, "state": "West Bengal",     "occupation": "Student", "income": 50000,  "gender": "male"},
    {"id": 9,  "label": "Student, Gujarat, no income",          "age": 22, "state": "Gujarat",         "occupation": "Student", "income": None,   "gender": "female"},
    {"id": 10, "label": "Student, Rajasthan, senior age edge",  "age": 30, "state": "Rajasthan",       "occupation": "Student", "income": 100000, "gender": "male"},

    # --- LABOUR ---
    {"id": 11, "label": "Labourer, UP, low income",             "age": 32, "state": "Uttar Pradesh",  "occupation": "Labour",  "income": 70000,  "gender": "male"},
    {"id": 12, "label": "Labourer, Odisha, female",             "age": 28, "state": "Odisha",          "occupation": "Labour",  "income": 55000,  "gender": "female"},
    {"id": 13, "label": "Labourer, Bihar, senior",              "age": 61, "state": "Bihar",           "occupation": "Labour",  "income": 40000,  "gender": "male"},
    {"id": 14, "label": "Labourer, Karnataka, no state match",  "age": 38, "state": "Karnataka",       "occupation": "Labour",  "income": 90000,  "gender": "male"},
    {"id": 15, "label": "Labourer, Jharkhand, very low income", "age": 25, "state": "Jharkhand",       "occupation": "Labour",  "income": 30000,  "gender": "female"},

    # --- WOMEN (occupation = Women) ---
    {"id": 16, "label": "Women, MP, low income",                "age": 30, "state": "Madhya Pradesh",  "occupation": "Women",   "income": 80000,  "gender": "female"},
    {"id": 17, "label": "Women, Haryana, medium income",        "age": 42, "state": "Haryana",         "occupation": "Women",   "income": 180000, "gender": "female"},
    {"id": 18, "label": "Women, Assam, young",                  "age": 22, "state": "Assam",           "occupation": "Women",   "income": 60000,  "gender": "female"},

    # --- BUSINESS ---
    {"id": 19, "label": "Business, Gujarat, medium income",     "age": 35, "state": "Gujarat",         "occupation": "Business","income": 500000, "gender": "male"},
    {"id": 20, "label": "Business, Delhi, young",               "age": 27, "state": "Delhi",           "occupation": "Business","income": 300000, "gender": "male"},

    # --- EDGE CASES ---
    {"id": 21, "label": "No occupation given, UP",              "age": 40, "state": "Uttar Pradesh",  "occupation": "",        "income": 100000, "gender": "male"},
    {"id": 22, "label": "All None fields",                      "age": None,"state": None,             "occupation": "",        "income": None,   "gender": ""},
    {"id": 23, "label": "Senior citizen, no occupation",        "age": 65, "state": "Kerala",          "occupation": "",        "income": 80000,  "gender": "male"},
    {"id": 24, "label": "Female, senior, farmer, low income",   "age": 63, "state": "Bihar",           "occupation": "Farmer",  "income": 50000,  "gender": "female"},
    {"id": 25, "label": "Young female student, low income",     "age": 16, "state": "Uttar Pradesh",  "occupation": "Student", "income": 40000,  "gender": "female"},
]

SEP  = "=" * 70
SEP2 = "-" * 70

print(SEP)
print("  ELIGIBILITY ENGINE — 25 PROFILE TEST")
print(SEP)

issues = []

for p in TEST_PROFILES:
    profile = {k: v for k, v in p.items() if k not in ("id", "label")}
    results = engine.recommend(profile, top_k=5)

    print(f"\n[{p['id']:02d}] {p['label']}")
    print(f"     Profile : age={p['age']} | state={p['state']} | occ={p['occupation']} | income={p['income']} | gender={p['gender']}")

    if not results:
        flag = "⚠️  NO RESULTS"
        issues.append(f"[{p['id']:02d}] {p['label']} → No results")
        print(f"     {flag}")
    else:
        print(f"     Results  : {len(results)} schemes found")
        for i, r in enumerate(results, 1):
            print(f"     {i}. {r['scheme_name'][:55]:<55} score={r['score']:>4}  conf={r['confidence']:>5}  | {r['reason'][:60]}")

    print(SEP2)

# Summary
print(f"\n{'=' * 70}")
print("  SUMMARY")
print(f"{'=' * 70}")
print(f"  Total profiles tested : {len(TEST_PROFILES)}")
print(f"  Profiles with results : {len(TEST_PROFILES) - len(issues)}")
print(f"  Profiles with NO results : {len(issues)}")
if issues:
    print("\n  ⚠️  Issues:")
    for issue in issues:
        print(f"     {issue}")
print()
