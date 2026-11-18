import sys
sys.path.append('backend')
from app.db.database import SessionLocal
from app.models.school import School
from app.models.program import Program

db = SessionLocal()
try:
    schools = db.query(School).all()
    print("=== SCHOOLS MATCHING 'Computer' ===")
    for s in schools:
        progs = db.query(Program).filter(Program.school_id == s.id).all()
        comp_progs = [
            p for p in progs
            if 'comput' in (p.field_of_study or '').lower()
            or 'software' in (p.field_of_study or '').lower()
            or 'informatique' in (p.field_of_study or '').lower()
        ]
        if comp_progs:
            print(f"* {s.name} ({s.institution_type})")
            for cp in comp_progs:
                print(f"    - {cp.field_of_study} ({cp.degree_type}) | mode: {cp.delivery_mode} | lang: {cp.language_of_instruction} | tuition: {cp.tuition_fee}")
finally:
    db.close()
