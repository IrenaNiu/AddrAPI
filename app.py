from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

country_format = [{"name":"China", "format":"Street address+City|Postcode+Province"},
                  {"name":"Austria", "format":"Street address|Postal code+City/Town/Locality"},
                  {"name":"New Zealand", "format":"Apartment number|House number+Street name|Suburb|City+Postal code"}]; 

@app.route('/')
def home():
	return render_template('home.html')


@app.route('/result', methods=['POST', 'GET'])
def showResult():

    info = request.form
    selected_country = info['country']
    address = []

    for country in country_format:
        if country['name'] == selected_country:
            mail_format = country['format']
    
    for key in info.keys():
        for val in info.getlist(key):
            address.append(val);
            address.append(', ');

    address = address[2:]
    address.append(selected_country)

    return render_template('result.html', data=address)




if __name__ == '__main__':
	app.run(debug=True)

