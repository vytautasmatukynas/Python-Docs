from main import app, db, SampleTable

# converts all models in to tables. Have to use app_context()
with app.app_context():
    db.create_all()

    one = SampleTable('oooo', 4, "uuuu")
    two = SampleTable('aaaa', 4, "yyyyy")

    # add objects to db
    db.session.add_all([one, two])
    # # or this for adding one item
    # db.session.add(one)
    # db.session.add(two)

    db.session.commit()

    print(one.id)
    print(two.id)