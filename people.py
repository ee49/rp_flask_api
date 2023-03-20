
from flask import abort, make_response

from config import db
from models import Person, person_schema,people_schema,PersonSchema

def read_all():
    people = Person.query.all()
    return people_schema.dump(people)

#deserialize the JSON struction sent from the HTTP to python object and to DB
# using marshmellow and SqlAlchemy respectively
def create(person):
    lname=person.get("lname")
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person is None:
        new_person = person_schema.load(person,session=db.session)
        db.session.add(new_person)
        db.session.commit()
        return person_schema.dump(new_person), 201
    else:
        abort(406,f"Person with last name {lname} already exist",)

def read_one(lname):
    #get one person or return None if no match is found
    person = Person.query.filter(Person.lname == lname).one_or_none()
    #return the serialized object for the matching name.
    if person is not None:
        return person_schema.dump(person)
    else:
        abort(404, f"person with last name {lname} not found")

def update(lname,person):
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person:
        update_person = person_schema.load(person, session=db.session)
        existing_person.fname = update_person.fname
        db.session.merge(existing_person)
        db.session.commit()
        return person_schema.dump(existing_person), 201
    else:
        abort(404, f"Person with last name {lname} not found")

def delete(lname):
    print(f"person to be deleted:{lname}")
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()
    print(f"Existing person value: {existing_person}")
    if existing_person:
        db.session.delete(existing_person)
        db.session.commit()
        return make_response(f"{lname} successfully deleted", 200)
    else:
        abort(404,f"Person with last name {lname} not found")

