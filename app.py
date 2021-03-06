from flask import Flask, render_template, request, redirect, url_for
import requests
import json

app = Flask(__name__)

VALIDATOR_API_ADDR = 'http://0.0.0.0:8000' 
DBCRUD_API_ADDR = 'http://0.0.0.0:7000' 

@app.route('/', methods=['GET'])
def home():
    response = requests.get(VALIDATOR_API_ADDR + '/country')
    countries = json.loads(response.text).get('countries')
    print(countries)
    return render_template('home.html', countries=countries)

@app.route('/format', methods=['POST'])
def get_format():
    country = request.form['country']
    response = requests.get(VALIDATOR_API_ADDR + '/format/' + country)
    country_format = json.loads(response.text)
    print(country_format)

    address = country_format.get('address')
    lines = country_format.get('format')
    print(address)
    print(lines)

    info = []
    for i in range(1, len(lines) + 1):
        info_line = []
        line = lines.get('line_' + str(i))
        for item in line:
            info_line.append(address.get(item))
        info.append(info_line)
        for i in info:
            print(i)
        print(type({country : info}))
    return {country : info}


@app.route('/result', methods=['POST'])
def search_address():

    info = request.form
    country = info['country']

    print('-----')
    print(info)
    print(country)
    for k in info:
        print(k + ': ' + info[k])

    address = info

    # TO-DO call crud API
    # response = requests.post(DBCRUD_API_ADDR + '/format/' + country)

    return render_template('result.html', data=address)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)

