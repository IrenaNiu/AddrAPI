from flask import Flask, request, jsonify

import os

app = Flask(__name__)

country_format = {
 
  "Spain": {
    "address": {
      "street_lv": { "name": "street_lv", "type": "string", "note": "address (street name, house/building number, etc.)" },
      "city_lv":   { "name": "city_lv", "type": "string", "note": "city/town/locality"},
      "postcode":  { "name": "postcode", "type": "numeric", "title": "xxxxx", "pattern": "[0-9]{5}", "note": "postal code"}
    },
    "format": {
      "line_1": ["street_lv"],
      "line_2": ["postcode", "city_lv"] 
    }
  },
  "Sweden": {
    "address": {
      "street_lv": { "name": "street_lv", "type": "string", "note": "address (street name, house/building number, etc.)" },
      "city_lv":   { "name": "city_lv", "type": "string", "note": "city/town" },
      "postcode":  { "name": "postcode", "type": "numeric", "title": "xxx xx", "pattern": "[0-9]{3} [0-9]{2}", "note": "postal code" }
    },
    "format": { 
      "line_1": ["street_lv"],
      "line_2": ["postcode", "city_lv"] 
    }
  },
  "Switzerland": {
    "address": {
      "street_lv": { "name": "street_lv", "type": "string", "note": "address (street name, house/building number,etc.)" },
      "city_lv":   { "name": "city_lv", "type": "string" ,"note": "city/town"},
      "postcode":  { "name": "postcode", "type": "numeric", "title": "xxxx", "pattern":"[0-9]{4}", "note": "postal code" }
    },
    "format": { 
      "line_1": ["street_lv"],
      "line_2": ["postcode", "city_lv"] 
    }
  },
  "Taiwan (RoC)": {
    "address": {
      "street_lv": { "name": "street_lv", "type": "string", "note": "address (house/building number, street name, section of street,etc.)" },
      "city_lv":   { "name": "city_lv", "type": "string", "note":"city" },
      "postcode":  { "name": "postcode", "type": "numeric", "title": "xxxxx", "pattern":"[0-9]{5}", "note":"postal code" }
    },
    "format": { 
      "line_1": ["street_lv"],
      "line_2": ["city_lv", "postcode"] 
    }
  },
  "Ukraine": {
    "address": {
      "street_lv": { "name": "street_lv", "type": "string", "note": "address (street name, house/building number, apartment,etc.)" },
      "city_lv":   { "name": "city_lv", "type": "string", "note":"town/city/locality" },
      "postcode":  { "name": "postcode", "type": "numeric", "title": "xxxxx", "pattern":"[0-9]{5}", "note":"postal code" }
    },
    "format": { 
      "line_1": ["street_lv"],
      "line_2": ["city_lv"], 
      "line_3": ["postcode"] 
    }
  },
  "United Kingdom": {
    "address": {
      "street_lv": { "name": "street_lv", "type": "string", "note": "address (house/building number, street name,etc.)" },
      "city_lv":   { "name": "city_lv", "type": "string", "note":"town/city" },
      "postcode":  { "name": "postcode", "type": "string", "title": "xxxx xxx", "pattern":"[0-9]{4} [0-9]{3}", "note":"postal code" }
    },
    "format": { 
      "line_1": ["street_lv"],
      "line_2": ["city_lv"], 
      "line_3": ["postcode"] 
    }
  },
  "United States": {
    "address": {
      "street_lv": { "name": "street_lv", "type": "string", "note": "address (house/building number, street name,etc.)" },
      "city_lv":   { "name": "city_lv", "type": "string", "note": "city" },
      "state_lv": { "name": "state_lv", "type": "string", "note": "state" },
      "postcode":  { "name": "postcode", "type": "numeric", "title": "xxxxx", "pattern":"[0-9]{5}", "note":"zip code" }
    },
    "format": { 
      "line_1": ["street_lv"],
      "line_2": ["city_lv", "state_lv", "postcode"]
    }
  },
  "Uruguay": {
    "address": {
      "street_lv": { "name": "street_lv", "type": "string", "note": "address(street name, house/building number, apartment, floor, etc.)" },
      "city_lv":   { "name": "city_lv", "type": "string", "note": "town/city" },
      "state_lv": { "name": "state_lv", "type": "string", "note": "province" },
      "postcode":  { "name": "postcode", "type": "numeric", "title": "xxxxx", "pattern": "[0-9]{5}", "note": "postal code" }
    },
    "format": { 
      "line_1": ["street_lv"],
      "line_2": ["postcode", "city_lv", "state_lv"]
    }
  },
  "Wales": {
    "address": {
      "street_lv": { "name": "street_lv", "type": "string", "note": "address(house/building number, street name, etc.)" },
      "city_lv":   { "name": "city_lv", "type": "string", "note": "town/city" },
      "postcode":  { "name": "postcode", "type": "string", "title": "xxxx xxx", "pattern":"[0-9]{4} [0-9]{3}", "note": "postal code" }
    },
    "format": { 
      "line_1": ["street_lv"],
      "line_2": ["city_lv"], 
      "line_3": ["postcode"] 
    }
  },

  "Netherlands":{
    "address":{
      "street_lv": { "name": "street_lv", "type": "string", "note": "address(house/building number, street name, etc.)" },
      "city_lv":   { "name": "city_lv", "type": "string", "note": "town/locality" },
      "postcode":  { "name": "postcode", "type": "string", "title": "xxxx xx", "pattern":"[0-9]{4} [0-9]{2}", "note": "postal code" }
    },
    "format":{
      "line_1": ["street_lv"],
      "line_2": ["postcode","city_lv"]
    }
  },
  
  "New Zealand":{
    "address":{
      "street_lv": { "name": "street_lv", "type": "string", "note": "address(house/building number, street name, etc.)" },
      "city_lv":   { "name": "city_lv", "type": "string", "note": "town/city" },
      "postcode":  { "name": "postcode", "type": "string", "title": "xxxx", "pattern":"[0-9]{4}", "note": "postal code" }
    },
    "format":{
      "line_1": ["street_lv"],
      "line_2": ["city_lv","postcode"]
    }
  },
  
  "Norway":{
    "address":{
      "street_lv": { "name": "street_lv", "type": "string", "note": "address (house/building number, street name, etc.)" },
      "city_lv":   { "name": "city_lv", "type": "string", "note":"town/city" },
      "postcode":  { "name": "postcode", "type": "string", "title": "xxx", "pattern": "[0-9]{3}", "note": "postal code" }
    },
    "format":{
      "line_1": ["street_lv"],
      "line_2": ["postcode","city_lv"]
    }
  },

  "Oman":{
    "address":{
      "street_lv": { "name": "street_lv", "type": "string", "note": "address (house/building number, street name, etc.)" },
      "city_lv":   { "name": "city_lv", "type": "string", "note":"town/city" },
      "postcode":  { "name": "postcode", "type": "string", "title": "xxx", "pattern": "[0-9]{3}", "note": "postcode" }
    },
    "format":{
      "line_1": ["street_lv"],
      "line_2": ["postcode"], 
      "line_3": ["city_lv"]
    }
  },
 
  "Pakistan":{
    "address":{
      "street_lv": { "name": "street_lv", "type": "string", "note": "address( house/building number,etc.)" },
      "street_lv2": { "name": "street_lv2", "type": "string", "note": "address2 (street name, etc.)"},
      "subdiv_lv": { "name": "subdiv_lv", "type": "string","note": "sector"},
      "city_lv":   { "name": "city_lv", "type": "string", "note": "town/city"},
      "postcode":  { "name": "postcode", "type": "string", "title": "xxxxx", "pattern": "[0-9]{5}", "note": "postal code" }
    },
    "format":{
      "line_1": ["street_lv"],
      "line_2": ["street_lv2"],
      "line_3": ["subdiv_lv"], 
      "line_3": ["city_lv","postcode"]
    }
  },
  
  "Poland":{
    "address":{
      "street_lv": { "name": "street_lv", "type": "string", "note": "address (house/building number, street name, etc.)" },
      "city_lv":   { "name": "city_lv", "type": "string", "note": "town/locality" },
      "postcode":  { "name": "postcode", "type": "string", "title": "xx-xxx", "pattern": "[0-9]{2}-[0-9]{3}", "note": "postal code" }
    },
    "format":{
      "line_1": ["street_lv"],
      "line_2": ["postcode","city_lv"]
    }
  },
  
  "Portugal":{
    "address":{
      "street_lv": { "name": "street_lv", "type": "string", "note": "address (street name, house/building number, etc.)" },
      "city_lv":   { "name": "city_lv", "type": "string", "note":"town/city" },
      "state_lv":  { "name": "state_lv", "type": "string", "note": "territorial subdivision" },
      "postcode":  { "name": "postcode", "type": "string", "title": "xxxx-xxx", "pattern": "[0-9]{4}-[0-9]{3}", "note": "postal code" }
    },
    "format":{
      "line_1": ["street_lv"],
      "line_2": ["city_lv"],
      "line_3": ["postcode", "state_lv"]
    }
  },
    
  "Puerto Rico":{
    "address":{
      "street_lv": { "name": "street_lv", "type": "string", "note": "address (street name, house/building number, etc.)" },
      "city_lv":   { "name": "city_lv", "type": "string", "note": "town/city" },
      "state_lv":  { "name": "state_lv", "type": "string", "note": "state" },
      "postcode":  { "name": "postcode", "type": "string", "title": "xxxxx", "pattern": "[0-9]{5}", "note": "zip code" }
    },
    "format":{
      "line_1": [ "street_lv"],
      "line_2": [ "city_lv"],
      "line_3": [ "state_lv","postcode" ]
    }
  }, 
    
  "Romania":{
    "address":{
      "street_lv": { "name": "street_lv", "type": "string", "note": "address (street name, house/building number, etc.)" },
      "city_lv":   { "name": "city_lv", "type": "string", "note": "town/city" },
      "state_lv":  { "name": "state_lv", "type": "string", "note": "sector" },
      "postcode":  { "name": "postcode", "type": "string", "title": "xxxxx", "pattern": "[0-9]{5}", "note": "postal code" }
    },
    "format":{
      "line_1": [ "street_lv"],
      "line_2": [ "postcode", "city_lv"],
      "line_3": [ "state_lv" ]
    }
  },  
   
  "Russia":{
    "address":{
      "street_lv": { "name": "street_lv", "type": "string", "note": "address (street name, house/building number, etc.)" },
      "city_lv":   { "name": "city_lv", "type": "string", "note": "town/city" },
      "state_lv":  { "name": "state_lv", "type": "string", "note": "province" },
      "postcode":  { "name": "postcode", "type": "string", "title": "xxxxxx", "pattern": "[0-9]{6}", "note": "postal code" }
    },
    "format":{
      "line_1": [ "street_lv"],
      "line_2": [ "city_lv"],
      "line_3": [ "state_lv" ],
      "line_4": [ "postcode"]
    }
  }, 
    
  "Singapore":{
    "address":{
      "street_lv": { "name": "street_lv", "type": "string", "note": "address (street name, house/building number, etc.)" },
      "city_lv":   { "name": "city_lv", "type": "string", "note": "town/city" },
      "postcode":  { "name": "postcode", "type": "string", "title": "xxxxxx", "pattern": "[0-9]{6}", "note":"post code" }
    },
    "format":{
      "line_1": [ "street_lv"],
      "line_2": [ "city_lv","postcode"]   
    }
  },  
    
  "South Africa":{
    "address":{
      "street_lv": { "name": "street_lv", "type": "string", "note": "address (street name, house/building number, etc.)" },
      "city_lv":   { "name": "city_lv", "type": "string", "note": "town/city" },
      "postcode":  { "name": "postcode", "type": "string", "title": "xx", "pattern": "[0-9]{2}", "note":"post code" }
    },
    "format":{
      "line_1": [ "street_lv"],
      "line_2": [ "city_lv"],
      "line_3": [ "postcode"]
    }
  },    
    
  "South Korea":{
    "address":{
      "street_lv": { "name": "street_lv", "type": "string", "note": "address (house/building number, street name, etc.)" },
      "subdiv_lv": { "name": "subdiv_lv", "type": "string", "note":"subdivision"},
      "city_lv":   { "name": "city_lv", "type": "string", "note": "town/city" },
      "postcode":  { "name": "postcode", "type": "string", "title": "xxx-xxx", "pattern": "[0-9]{3}-[0-9]{3}", "note":"post code" }
    },
    "format":{
      "line_1": [ "street_lv"],
      "line_2": [ "subdiv_lv"],
      "line_3": [ "city_lv","postcode"]
    }
  } 
    
    
 }

@app.route('/country', methods =['GET'])
def get_countries():
    try:
      countries = list(country_format.keys())
      result = {'countries' : countries}
      print(result)
    except Exception as a:
        return jsonify({"error":str(a)})
    return result

@app.route('/format/<string:country>',methods =['GET'])
def search_format(country):
    try:
      print(country)

      result = country_format[country]

      print(result)
    except Exception as a:
        return jsonify({"error":str(a)})
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 8000, debug = True)

