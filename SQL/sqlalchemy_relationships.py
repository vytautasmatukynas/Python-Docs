# ONE TO MANY <----------------------------------

# In SQLAlchemy, one-to-many relationships are defined using a Foreign Key on the many side of the relationship, which
# points to the primary key of the one side. In the example above, the “order” table would have a foreign key column
# that refers to the primary key of the “customer” table.
# In this example, the relationship() function is used to define the relationship between the Customer and Order classes.
# The first argument is the name of the class on the other side of the relationship, and the back_populates argument
# is used to define the reverse side of the relationship. This allows us to access the related objects from either side
# of the relationship:
class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    orders = relationship("Order", back_populates="customer")

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    customer = relationship("Customer", back_populates="orders")

# With the one-to-many relationship defined, we can now easily query the related objects.
# For example, to get the orders for a customer, we can write:
customer = session.query(Customer).get(1)
orders = customer.orders

######################################################################################################################

# MANY TO ONE <------------------------

# In SQLAlchemy, many-to-one relationships are defined using a Foreign Key on the many side of the relationship,
# which points to the primary key of the one side. In the example above, the “order” table would have a foreign key
# column that refers to the primary key of the “customer” table.
# To define a many-to-one relationship in SQLAlchemy, we use the relationship() function, which creates a new
# relationship property on the many side of the relationship. This property provides access to the related object
# in the one side of the relationship. For example, to define the relationship between orders and customers,
# we could write:
class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    customer = relationship("Customer")

# With the many-to-one relationship defined, we can now easily query the related object. For example, to get the
# customer for an order, we can write:
order = session.query(Order).get(1)
customer = order.customer

######################################################################################################################

# MANY TO MANY <-------------------------

# In SQLAlchemy, many-to-many relationships are implemented using an intermediate table, also known as an association
# table, that maps the relationships between the two entities. The intermediate table contains foreign keys to both of
# the related tables and serves as a mapping between them.
# To define a many-to-many relationship in SQLAlchemy, we create a new class for the intermediate table, which will
# contain the foreign keys to both related tables. We then use the relationship() function to define the relationships
# on both sides of the relationship. For example, to define the relationship between students and courses, we could write:
class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    courses = relationship("Course", secondary="student_course", back_populates="students")

class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    students = relationship("Student", secondary="student_course", back_populates="courses")

class StudentCourse(Base):
    __tablename__ = 'student_course'
    student_id = Column(Integer, ForeignKey('student.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'), primary_key=True)

# With the many-to-many relationship defined, we can now easily query the related objects. For example, to get the
# courses for a student, we can write:
student = session.query(Student).get(1)
courses = student.courses

######################################################################################################################

# Implementing Relationships in SQLAlchemy <----------------------------
customer = session.query(Customer).get(1)
order = Order(customer=customer)
session.add(order)
session.commit()

# To query the related objects, we simply access the relationship property on the related object. For example, to get
# all orders for a customer, we can write:
customer = session.query(Customer).get(1)
orders = customer.orders

######################################################################################################################

# BACKREF <-------------------------------

# backref is a shortcut for configuring both parent.children and child.parent relationships at one place only on
# the parent or the child class (not both). That is, instead of having
children = relationship("Child", back_populates="parent")  # on the parent class
# and
parent = relationship("Parent", back_populates="children")  # on the child class
# you only need one of this:
children = relationship("Child", backref="parent")  # only on the parent class
# or
parent = relationship("Parent", backref="children")  # only on the child class

# 'children = relationship("Child", backref="parent")' will create the .parent relationship on the child class
# automatically. On the other hand, if you use 'back_populates' you must explicitly create the relationships in both
# parent and child classes.

# This onfiguration establishes a collection of Address objects on User called User.addresses. It also establishes
# a .user attribute on Address which will refer to the parent User object:
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    addresses = relationship("Address", backref="user")

class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))

######################################################################################################################