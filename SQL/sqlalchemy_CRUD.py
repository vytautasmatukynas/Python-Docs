
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, func, create_engine, or_, and_
from sqlalchemy.orm import sessionmaker

""" SQLALCHEMY CRUD ACTIONS """

##################################### SAMPLE DB MODEL ####################################
# Replace these values with your PostgreSQL database connection details
db_url = 'postgresql://username:password@localhost:5432/your_database_name'

# # Replace these values with your SQLite database connection details
# db_url = 'sqlite:///path/to/your_database.db'
# # Replace these values with your MySQL database connection details
# db_url = 'mysql://username:password@localhost:3306/your_database_name'

# Create a database engine
engine = create_engine(db_url)

# Declarative classes are the primary classes you define to
# represent database tables, and they inherit from the Base class
Base = declarative_base()

# Sample MODEL of DB
class SampleModel(Base):
    __tablename__ = 'samples'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), index=True, nullable=False, default='xx')
    email = Column(String(32), unique=True)
    create_time = Column(DateTime, default=datetime.datetime.now)
    extra = Column(Text, nullable=True)

# create the table in the database by calling the Base.metadata.create_all()
# method and passing in the engine as an argument
Base.metadata.create_all(engine)

# Create a Session class to interact with the database
Session = sessionmaker(bind=engine)
# Create a session
session = Session()

##################################### INSERT ####################################
""" INSERT INTO [table_name] (name, email, password) VALUES ('test_name', 'test@qq.com', '123456'); """
action = SampleModel(email='test_name@email.com',
                     name='test_name')

session.add(action)
session.commit()

# <OR>

model = SampleModel()
model.name = 'test_name'

session.add(model)
session.commit()

################################## UPDATE #####################################
""" UPDATE SampleModel
SET name = 'New Name', email = 'new@example.com', password = 'new_password'
WHERE id = [id] """
action = SampleModel.query.get(id)

new_name = "New Name"
new_email = "new@example.com"
new_password = "new_password"

action.name = new_name
action.email = new_email
action.password = new_password

session.commit()

############################# DELETE ####################################
""" DELETE FROM blog_post WHERE id = [id]; """
action = SampleModel.query(id).first()

session.delete(action)
session.commit()

# <OR>

SampleModel.query.filter(SampleModel.id == id).delete()

# <OR>

action = SampleModel.query.filter_by(id=id).first()

session.delete(action)
session.commit()

# <OR>

actions = SampleModel.query.filter_by(id=id).all()

for action in actions:
    session.delete(action)

session.commit()

################################## SELECT ######################################
""" SELECT * FROM [table_name] WHERE id = [id] LIMIT 1; """
action = SampleModel.query.filter(SampleModel.id == id).first()

""" SELECT * FROM [table_name] WHERE age >= 18 AND gender = 'Female' LIMIT 1; """
action = SampleModel.query.filter(SampleModel.age >= 18,
                                SampleModel.gender == 'Female'
                                ).first()

""" SELECT * FROM [table_name] WHERE email = [value] LIMIT 1; """
action = SampleModel.query.filter_by(email='email@sample.com').first()

""" SELECT * FROM [table_name] WHERE id = [id]; """
action = SampleModel.query.filter(SampleModel.id == id).all()

""" SELECT * FROM sample_model WHERE email = [value]; """
action = SampleModel.query.filter_by(email='email@sample.com').all()

################################# SELECT SAMPLE WITH LESS ##########################
""" SELECT sample_model.user_id FROM sample_model WHERE sample_model.user_id > 0; """
user_ids = SampleModel.query(SampleModel.user_id).filter(SampleModel.user_id > 0).all()

for user_id in user_ids:
    print(f"user_id: {user_id[0]}")

session.close()

################################# SELECT ONE AND UPDATE ##########################
""" UPDATE [table_name] SET is_finish=1 WHERE [table_name].id = [id]; """
action = SampleModel.query.filter(SampleModel.id == id).update({
    'is_finish': 1
}, synchronize_session=False)

""" SELECT id FROM [table_name] WHERE [table_name].id = [id]; """
""" UPDATE [table_name] SET is_finish=1 WHERE [table_name].id = [id]; """
action = SampleModel.query.filter(SampleModel.id == id).update({
    'is_finish': 1
}, synchronize_session="fetch")

""" UPDATE [table_name] SET count=([table_name].count + 1) WHERE [table_name].id = [id]; """
action = SampleModel.query.filter(SampleModel.id == id).update({
    'count': SampleModel.count + 1
}, synchronize_session="evaluate")

################################# SELECT VALUES WITH "IN" RANGE ##########################
""" SELECT * FROM [table_name] WHERE id IN (1, 2, 3); """
filter_ids = [1, 2, 3]
action = SampleModel.query.filter(SampleModel.id.in_(filter_ids)).all()

""" SELECT * FROM [table_name] WHERE id NOT IN (1, 2, 3); """
filter_ids = [1, 2, 3]
action = SampleModel.query.filter(SampleModel.id.notin_(filter_ids)).all()

#################################### SELECT VALUES WITH "OR" ####################################
""" SELECT * FROM [table_name] WHERE id = [id] OR name = [name]; """
action = SampleModel.query.filter(or_(
                                    SampleModel.id == id,
                                    SampleModel.name == "name"
                                    )).first()

#################################### SELECT VALUES WITH "AND" ####################################
""" SELECT * FROM [table_name] WHERE id = [id] AND name = [name]; """
action = SampleModel.query.filter(and_(
                                    SampleModel.id == id,
                                    SampleModel.name == "name"
                                    )).first()

################################ ORDER BY ##################################
""" SELECT * FROM [table_name] ORDER BY name DESC; """
action = SampleModel.query.order_by(SampleModel.name.desc()).all()

""" SELECT * FROM [table_name] ORDER BY name DESC, email ASC; """
action = SampleModel.query.order_by(SampleModel.name.desc(), SampleModel.email.asc()).all()

########################### LIMIT ###################################
""" SELECT * FROM sample_model ORDER BY sample_model.name DESC LIMIT 10; """
action = SampleModel.query.order_by(SampleModel.name.desc()).limit(10).all()

########################### ROW LOCK ###################################
""" SELECT * FROM [table_name] WHERE [table_name].id = [id] LIMIT 1 FOR UPDATE; """
action = SampleModel.query.filter(SampleModel.id == id).with_for_update().first()

########################### SELECT BY LABEL ###################################
""" SELECT [table_name].name AS alias_name FROM [table_name] LIMIT 1; """
action = session.query(SampleModel.name.label('alias_name')).first()

""" SELECT [table_name].name AS alias_name FROM [table_name]; """
action = session.query(SampleModel.name.label('alias_name')).all()

########################### HAVING ###################################
""" SELECT user.user_id FROM user HAVING user.user_id > 0 LIMIT 1 """
action = SampleModel.query.having(SampleModel.user_id > 0).first()

""" SELECT user.user_id FROM user HAVING user.user_id > 0 """
results = SampleModel.query.having(SampleModel.user_id > 0).all()

for result in results:
    print(f"Category: {result.category}, Count: {result.count}")

########################### COUNT ###################################
""" SELECT COUNT(*) FROM sample_model WHERE id = [id]; """
action = SampleModel.query.filter(SampleModel.id == id).count()

""" SELECT COUNT(*) FROM sample_model WHERE email = [value]; """
action = SampleModel.query.filter_by(email="email@email.com").count()

########################### GROUP BY, COUNT AND AVG ##################################
""" SELECT sample_model.category, count(*) AS count FROM sample_model GROUP BY sample_model.category """
results = (SampleModel.query
           .with_entities(SampleModel.category, func.count().label('count'))
           .group_by(SampleModel.category)
           .all())

for result in results:
    print(f"Category: {result.category}, Count: {result.count}")
