from flask import Flask, render_template, request, redirect, url_for
import requests
import json

app = Flask(__name__)

VALIDATOR_AKI_ADDR = 'http://0.0.0.0:8000' 

@app.route('/')
def home():
    response = requests.get(VALIDATOR_AKI_ADDR + '/country')
    countries = json.loads(response.text).get('countries')
    print(countries)
    print(type(countries))
    return render_template('home.html', countries=countries)

@app.route('/result', methods=['POST', 'GET'])
def showResult():

    info = request.form
    country = info['country']
    address = []

    response = requests.get(VALIDATOR_AKI_ADDR + '/format/' + 'SouthKorea')
    country_info = json.loads(response.text)
    print(country_info)

    # for country in country_format:
    #     if country['name'] == selected_country:
    #         mail_format = country['format']

    print(country_info.get('address'))
    print('-----')
    print(country_info.get('format'))
    
    # for key in info.keys():
    #     for val in info.getlist(key):
    #         address.append(val);
    #         address.append(', ');

    # address = address[2:]
    # address.append(selected_country)

    address = ['1', '2', '3']

    return render_template('result.html', data=address)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)

