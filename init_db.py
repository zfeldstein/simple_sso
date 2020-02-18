from app import db
from app.models import Users

# Bootstrap admin user
admin = Users(username="admin")
admin.hash_password("cubs2020")
admin.expiration = 90
admin.is_admin = True

# Create all imported models + admin user
db.create_all()
db.session.add(admin)
db.session.commit()
