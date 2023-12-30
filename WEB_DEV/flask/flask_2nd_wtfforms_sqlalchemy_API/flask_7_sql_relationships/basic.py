# Entries in to the tables

from main import db, Puppy, Owner, Toy, app

with app.app_context():
    rufus = Puppy("Rufus")
    fido = Puppy("Fido")

    # add puppies to db

    db.session.add_all([rufus,fido])
    db.session.commit()

    print(Puppy.query.all())
    
    # grab first item
    rufus = Puppy.query.filter_by(name="Rufus").first()
    # # gets back list items
    # rufus = Puppy.query.filter_by(name="Rufus").all()
    # rufus = Puppy.query.filter_by(name="Rufus").all()[0]
    
    # OWNER object. Create owner for rufus, with rufus.id
    jose = Owner('Jose', rufus.id)
    
    # TOYS object
    toy_1 = Toy("Chew toy", rufus.id)
    toy_2 = Toy("Ball", rufus.id)
    
    db.session.add_all([jose, toy_1, toy_2])
    db.session.commit()
    
    rufus = Puppy.query.filter_by(name="Rufus").first()
    
    print(Puppy.query.all())
    rufus.report_toys()
    
    db.session.delete()
    
    