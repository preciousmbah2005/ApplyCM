import sys, unicodedata, re
sys.path.append('backend')
from app.db.database import SessionLocal
from app.models.school import School
from app.models.program import Program

def normalize_text(text):
    if not text:
        return ""
    norm = unicodedata.normalize("NFD", text)
    return "".join(c for c in norm if unicodedata.category(c) != "Mn").lower().strip()

def extract_tuition_number(tuition_str):
    if not tuition_str:
        return None
    digits = re.sub(r'[^0-9]', '', tuition_str)
    return int(digits) if digits else None

def filter_schools(schools_data, params):
    res = []
    norm_type = (params.get("institution_type") or "all").lower()
    norm_city = normalize_text(params.get("city"))
    norm_field = normalize_text(params.get("field_of_study"))
    norm_deg = params.get("degree_type") or "All"
    min_t = params.get("min_tuition")
    max_t = params.get("max_tuition")
    norm_lang = (params.get("language") or "all").lower()
    norm_mode = (params.get("delivery_mode") or "all").lower()
    norm_search = normalize_text(params.get("search"))
    include_unlisted = params.get("include_unlisted", False)

    for s in schools_data:
        # 1. Type
        if norm_type != "all":
            if (s.get("institution_type") or "").lower() != norm_type:
                continue

        # 2. City
        if norm_city and norm_city != "all":
            scity = normalize_text(s.get("city"))
            sloc = normalize_text(s.get("location"))
            if norm_city not in scity and norm_city not in sloc:
                continue

        # 3. Field of Study
        if norm_field:
            is_comp = any(k in norm_field for k in ["comput", "softw", "informati", "cyber"])
            progs = s.get("programs", [])
            match_field = False
            for p in progs:
                pf = normalize_text(p.get("field_of_study"))
                pd = normalize_text(p.get("description"))
                if norm_field in pf or norm_field in pd:
                    match_field = True
                    break
                if is_comp:
                    if any(k in pf or k in pd for k in ["comput", "softw", "informati", "cyber"]):
                        match_field = True
                        break
            if not match_field:
                continue

        # 4. Degree Type
        if norm_deg != "All":
            d = normalize_text(norm_deg)
            match_deg = False
            for p in s.get("programs", []):
                deg = normalize_text(p.get("degree_type"))
                if "bachelor" in d or "licence" in d:
                    if any(k in deg for k in ["bachelor", "licence", "bsc", "ll.b"]):
                        match_deg = True
                        break
                elif "master" in d or "mba" in d:
                    if any(k in deg for k in ["master", "mba", "dipes ii"]):
                        match_deg = True
                        break
                elif "engineer" in d or "ingenieur" in d:
                    if "engineer" in deg or "ingenieur" in deg:
                        match_deg = True
                        break
                elif "bts" in d or "hnd" in d:
                    if any(k in deg for k in ["bts", "hnd", "technicien"]):
                        match_deg = True
                        break
                elif any(k in deg for k in [d]):
                    match_deg = True
                    break
            if not match_deg:
                continue

        # 5. Tuition
        if min_t is not None or max_t is not None:
            fees = [extract_tuition_number(p.get("tuition_fee")) for p in s.get("programs", [])]
            fees = [f for f in fees if f is not None]
            if not fees:
                if not include_unlisted:
                    continue
            else:
                match_fee = False
                for f in fees:
                    if min_t is not None and f < min_t:
                        continue
                    if max_t is not None and f > max_t:
                        continue
                    match_fee = True
                    break
                if not match_fee:
                    continue

        # 6. Language
        if norm_lang != "all":
            match_lang = False
            for p in s.get("programs", []):
                pl = normalize_text(p.get("language_of_instruction"))
                if norm_lang == "english":
                    if "english" in pl or "bilingual" in pl:
                        match_lang = True
                        break
                elif norm_lang == "french":
                    if "french" in pl or "francais" in pl or "bilingual" in pl:
                        match_lang = True
                        break
                elif norm_lang == "bilingual":
                    if "bilingual" in pl:
                        match_lang = True
                        break
                elif norm_lang in pl:
                    match_lang = True
                    break
            if not match_lang:
                continue

        # 7. Delivery Mode
        if norm_mode != "all":
            match_mode = False
            for p in s.get("programs", []):
                pm = normalize_text(p.get("delivery_mode"))
                if norm_mode in pm:
                    match_mode = True
                    break
            if not match_mode:
                continue

        # 8. Search
        if norm_search:
            s_text = " ".join([
                normalize_text(s.get("name")),
                normalize_text(s.get("location")),
                normalize_text(s.get("description")),
                normalize_text(s.get("city")),
            ])
            p_text = " ".join([
                normalize_text(p.get("field_of_study")) + " " + normalize_text(p.get("description"))
                for p in s.get("programs", [])
            ])
            if norm_search not in s_text and norm_search not in p_text:
                continue

        res.append(s)
    return res

db = SessionLocal()
try:
    schools = db.query(School).all()
    schools_data = []
    for s in schools:
        progs = db.query(Program).filter(Program.school_id == s.id).all()
        schools_data.append({
            "name": s.name,
            "institution_type": s.institution_type,
            "city": s.city,
            "location": s.location,
            "description": s.description,
            "programs": [
                {
                    "field_of_study": p.field_of_study,
                    "degree_type": p.degree_type,
                    "tuition_fee": p.tuition_fee,
                    "language_of_instruction": p.language_of_instruction,
                    "delivery_mode": p.delivery_mode,
                    "description": p.description,
                }
                for p in progs
            ]
        })
    print(f"Loaded {len(schools_data)} schools from DB.")

    # RUN ALL 8 TEST CASES
    print("\n--- TEST CASE 1: Institution Type = IUP only ---")
    t1 = filter_schools(schools_data, {"institution_type": "iup"})
    print(f"Count: {len(t1)}")
    for s in t1:
        print(f"  - {s['name']} (type: {s['institution_type']})")
    assert all(s['institution_type'] == 'iup' for s in t1) and len(t1) > 0, "Test 1 failed!"

    print("\n--- TEST CASE 2: City = Douala ---")
    t2 = filter_schools(schools_data, {"city": "Douala"})
    print(f"Count: {len(t2)}")
    assert len(t2) == 0, "Test 2 failed (Douala should have 0 institutions)!"

    print("\n--- TEST CASE 3: Field of Study = 'Computer' ---")
    t3 = filter_schools(schools_data, {"field_of_study": "Computer"})
    print(f"Count: {len(t3)}")
    for s in t3:
        print(f"  - {s['name']}")
    assert len(t3) > 0 and len(t3) < 15, "Test 3 failed!"

    print("\n--- TEST CASE 4: Tuition <= 500k FCFA ---")
    t4 = filter_schools(schools_data, {"max_tuition": 500000})
    print(f"Count: {len(t4)}")
    for s in t4:
        print(f"  - {s['name']}")
    assert len(t4) > 0 and not any("The ICT University" in s['name'] for s in t4), "Test 4 failed!"

    print("\n--- TEST CASE 5: Language = English + Delivery Mode = Hybrid ---")
    t5 = filter_schools(schools_data, {"language": "English", "delivery_mode": "Hybrid"})
    print(f"Count: {len(t5)}")
    for s in t5:
        print(f"  - {s['name']}")
    assert len(t5) == 1 and "The ICT University" in t5[0]['name'], "Test 5 failed!"

    print("\n--- TEST CASE 6: Degree Level = Master / MBA ---")
    t6 = filter_schools(schools_data, {"degree_type": "Master"})
    print(f"Count: {len(t6)}")
    for s in t6:
        print(f"  - {s['name']}")
    assert len(t6) > 0 and len(t6) < 15, "Test 6 failed!"

    print("\n--- TEST CASE 7: All 6 filters combined (IUP, Yaounde, Computer, Tuition <= 100k, English, Hybrid) ---")
    t7 = filter_schools(schools_data, {
        "institution_type": "iup",
        "city": "Yaoundé",
        "field_of_study": "Computer",
        "max_tuition": 100000,
        "language": "English",
        "delivery_mode": "Hybrid",
    })
    print(f"Count: {len(t7)}")
    assert len(t7) == 0, "Test 7 failed (should be empty state)!"

    print("\n--- TEST CASE 8: Clear All ---")
    t8 = filter_schools(schools_data, {})
    print(f"Count: {len(t8)}")
    assert len(t8) == 15, "Test 8 failed (should restore all 15)!"

    print("\n>>> ALL 8 TEST CASES PASSED SUCCESSFULLY! <<<")
finally:
    db.close()
