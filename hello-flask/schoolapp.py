from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALQUEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), unique=False)
    summary = db.Column(db.String(244), unique=False)

    def __init__(self, subject, summary, test):
        self.subject = subject
        self.summary = summary
        self.test = test


class EvaluationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'subject', 'summary', 'test')


evaluation_schema = EvaluationSchema()
evaluations_schema = EvaluationSchema(many=True)

@app.route('/evaluation', methods=["POST"])
def add_guide():
    subject = request.json['subject']
    summary = request.json['summary']
    test = request.json['test']

    new_evaluation = Evaluation(subject, summary, test)

    db.session.add(new_evaluation)
    db.session.commit()

    evaluation = Evaluation.query.get(new_evaluation)

    return evaluation_schema.jsonify(evaluation)

@app.route('/evaluations', methods=["GET"])
def get_evaluations():
    all_evaluations = Evaluation.query.all()
    result = evaluations_schema.dump(all_evaluations)
    return jsonify(result)

@app.route('/evaluation/<id>', methods=["GET"])
def get_evaluation(id):
    evaluation = Evaluation.query.get(id)
    return evaluation_schema(evaluation)

@app.route('/evaluation/<id>', methods=["PUT"])
def evaluation_update(id):
    evaluation = Evaluation.query.get(id)
    subject = request.json['subject']
    summary = request.json['summary']
    test = request.json['test']

    evaluation.subject = subject
    evaluation.summary = summary
    evaluation.test = test
    
    db.session.commit()
    return evaluation_schema.jsonify(evaluation)

@app.route('/evaluation/<id>', methods=["DELETE"])
def evaluation_delete(id):
    evaluation = Evaluation.query.get(id)
    if guide:
        db.session.delete(evaluation)
        db.session.commit()
        return f"Evaluation {id} deleted"

@app.route('/evaluation/<start>-<stop>', methods=['DELETE'])
def evaluation_delete_range(start, stop):
    for id in range(int(start), int(stop)):
        evaluation = Evaluation.query.get(id)
        if evaluation:
            db.session.delete(evaluation)
            db.session.commit()
    
    return f'Evaluations {start} to {stop} deleted'


if __name__ == '__main__':
    app.run(debug=True)
