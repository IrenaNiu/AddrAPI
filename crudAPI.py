from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import yaml

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
db_config = yaml.load(open('database.yaml'))
app.config['SQLALCHEMY_DATABASE_URI'] = db_config['uri'] 
db = SQLAlchemy(app)
CORS(app)

class Address(db.Model):
    __tablename__ = "address"
    adid = db.Column(db.Integer, primary_key=True)
    country_lv = db.Column(db.String(255))
    state_lv = db.Column(db.String(255))
    city_lv = db.Column(db.String(255))
    subdiv_lv = db.Column(db.String(255))
    postcode = db.Column(db.String(255))
    street_lv = db.Column(db.String(255))
    
    def __init__(self, country, state, city, subdiv, postcode, street):
        self.country_lv = country
        self.state_lv = state
        self.city_lv = city
        self.subdiv_lv = subdiv
        self.postcode = postcode
        self.street_lv = street
     
    def __repr__(self):
        return '%s/%s/%s/%s/%s/%s/%s' % (self.adid, self.country_lv, self.state_lv, self.city_lv, self.subdiv_lv, self.postcode, self.street_lv)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/address', methods=['POST', 'GET'])
def data():
    
    # POST an address to database
    if request.method == 'POST':
        body = request.json
        # print(body)
        country_lv = body['country_lv']
        state_lv = body['state_lv']
        city_lv = body['city_lv']
        subdiv_lv = body['subdiv_lv']
        postcode = body['postcode']
        street_lv = body['street_lv']

        data = Address(country_lv, state_lv, city_lv, subdiv_lv, postcode, street_lv)
        db.session.add(data)
        db.session.commit()

        return jsonify({
            'status': 'Address is added to PostgreSQL!',
            'country_lv': country_lv,
            'state_lv': state_lv,
            'city_lv': city_lv,
            'subdiv_lv': subdiv_lv,
            'postcode': postcode,
            'street_lv': street_lv
        })
    
    # GET all addresses from database & sort by id
    if request.method == 'GET':
        # data = User.query.all()
        data = Address.query.order_by(Address.adid).all()
        # print(data)
        dataJson = []
        for i in range(len(data)):
            # print(str(data[i]).split('/'))
            dataDict = {
                'adid': str(data[i]).split('/')[0],
                'country_lv': str(data[i]).split('/')[1],
                'state_lv': str(data[i]).split('/')[2],
                'city_lv': str(data[i]).split('/')[3],
                'subdiv_lv': str(data[i]).split('/')[4],
                'postcode': str(data[i]).split('/')[5],
                'street_lv': str(data[i]).split('/')[6]
            }
            dataJson.append(dataDict)
        return jsonify(dataJson)

@app.route('/address/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata(id):

    # GET a specific address by id
    if request.method == 'GET':
        data = Address.query.get(id)
        print(data)
        dataDict = {
            'adid': str(data).split('/')[0],
            'country_lv': str(data).split('/')[1],
            'state_lv': str(data).split('/')[2],
            'city_lv': str(data).split('/')[3],
            'subdiv_lv': str(data).split('/')[4],
            'postcode': str(data).split('/')[5],
            'street_lv': str(data).split('/')[6]
        }
        return jsonify(dataDict)
        
    # DELETE an address
    if request.method == 'DELETE':
        delData = Address.query.filter_by(adid=id).first()
        db.session.delete(delData)
        db.session.commit()
        return jsonify({'status': 'Address '+id+' is deleted from PostgreSQL!'})

    # UPDATE an address by id
    if request.method == 'PUT':
        body = request.json
        newCountry = body['country_lv']
        newState = body['state_lv']
        newCity = body['city_lv']
        newSubdiv = body['subdiv_lv']
        newPostcode = body['postcode']
        newStreet = body['street_lv']
        editData = Address.query.filter_by(adid=id).first()
        editData.country_lv = newCountry
        editData.state_lv = newState
        editData.city_lv = newCity
        editData.subdiv_lv = newSubdiv
        editData.postcode = newPostcode
        editData.street_lv = newStreet
        db.session.commit()
        return jsonify({'status': 'Address '+id+' is updated from PostgreSQL!'})

if __name__ == '__main__':
    app.debug = True
    app.run()
