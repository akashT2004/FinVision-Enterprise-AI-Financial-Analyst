from app.models.database import SessionLocal
from app.models.orm import User, Role

def seed_admin():
    db = SessionLocal()
    # 1. Create Roles if they don't exist
    admin_role = db.query(Role).filter(Role.name == "Admin").first()
    if not admin_role:
        admin_role = Role(name="Admin")
        db.add(admin_role)
        db.add(Role(name="Analyst"))
        db.add(Role(name="Auditor"))
        db.add(Role(name="Client"))
        db.commit()
        db.refresh(admin_role)
        print("Roles created.")

    # 2. Find the 'admin' user and assign the role
    user = db.query(User).filter(User.username == "admin").first()
    if user:
        user.role_id = admin_role.id
        db.commit()
        print(f"User '{user.username}' is now an Admin.")
    else:
        print("User 'admin' not found.")
    db.close()

if __name__ == "__main__":
    seed_admin()
