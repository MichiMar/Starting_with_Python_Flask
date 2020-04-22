from flask import Flask, request, jsonify      # capital word = class
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os          # operate system

app = Flask(__name__)  # instantiation

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)        #inherited
ma = Marshmallow(app)

class Guide(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False)
    content = db.Column(db.String(144), unique=False)

    def __init__(self, title, content, another):
        self.title = title
        self.content = content
        self.another = another


class GuideSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content', 'another')


guide_schema = GuideSchema()
guides_schema = GuideSchema(many=True)

# Endpoint to create a new guide
@app.route('/guide', methods=["POST"])
def add_guide():
    title = request.json['title']
    content = request.json['content']

    new_guide = Guide(title, content)

    db.session.add(new_guide)
    db.session.commit()

    guide = Guide.query.get(new_guide.id)

    return guide_schema.jsonify(guide)


# Endpoint to query all guides
@app.route('/guides', methods=["GET"])
def get_guides():
    all_guides = Guide.query.all()
    result = guides_schema.dump(all_guides)
    return jsonify(result)


# Endpoint for query a single guide
@app.route('/guide/<id>', methods=["GET"])
def get_guide(id):
    guide = Guide.query.get(id)
    return guide_schema.jsonify(guide)


# Endpoint for updating a guide
@app.route("/guide/<id>", methods=["PUT"])
def guide_update(id):
    guide = Guide.query.get(id)
    title = request.json['title']
    content = request.json['content']

    guide.title = title
    guide.content = content

    db.session.commit()
    return guide_schema.jsonify(guide)


# Endpoint for deleting a record
@app.route("/guide/<id>", methods=["DELETE"])
def guide_delete(id):
    guide = Guide.query.get(id)
    db.session.delete(guide)
    db.session.commit()

# Endpoint for deleting a range of records
@app.route("/guides/<start>/<stop>", methods=["DELETE"])
def guide_delete_range(start, stop):
    for id in range(int(start), int(stop)):
        guide = Guide.query.get(id)
        if guide:            
            db.session.delete(guide)
            db.session.commit()

    return f"Guides from {start} to {stop} were succesfully deleted"


if __name__ == '__main__':
    app.run(debug=True)