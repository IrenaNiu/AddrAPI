from flask import Flask, request, jsonify

import os

app = Flask(__name__)

country_format = {
 
  "Spain": {
    "address": {
      "street_lv": { "name": "address", "type": "string", "note": "street name, house/building number" },
      "city_lv":   { "name": "city/town/locality", "type": "string" },
      "postcode":  { "name": "postal code", "type": "numeric", "pattern": "xxxxx" }
    },
    "format": { 
      "line_1": ["street_lv"],
      "line_2": ["postcode", "city_lv"] 
    }
  },
  "Sweden": {
    "address": {
      "street_lv": { "name": "address", "type": "string", "note": "street name, house/building number" },
      "city_lv":   { "name": "city/town", "type": "string" },
      "postcode":  { "name": "postal code", "type": "numeric", "pattern": "xxx xx" }
    },
    "format": { 
      "line_1": ["street_lv"],
      "line_2": ["postcode", "city_lv"] 
    }
  },
  "Switzerland": {
    "address": {
      "street_lv": { "name": "address", "type": "string", "note": "street name, house/building number" },
      "city_lv":   { "name": "city/town/village", "type": "string" },
      "postcode":  { "name": "postal code", "type": "numeric", "pattern": "xxxx" }
    },
    "format": { 
      "line_1": ["street_lv"],
      "line_2": ["postcode", "city_lv"] 
    }
  },
  "Taiwan (RoC)": {
    "address": {
      "street_lv": { "name": "address", "type": "string", "note": "(house/building number), street name, section of street" },
      "city_lv":   { "name": "city", "type": "string" },
      "postcode":  { "name": "postal code", "type": "numeric", "pattern": "xxxxx" }
    },
    "format": { 
      "line_1": ["street_lv"],
      "line_2": ["city_lv", "postcode"] 
    }
  },
  "Ukraine": {
    "address": {
      "street_lv": { "name": "address", "type": "string", "note": "street name, house/building number, apartment" },
      "city_lv":   { "name": "town/city/locality", "type": "string" },
      "postcode":  { "name": "postal code", "type": "numeric", "pattern": "xxxxx" }
    },
    "format": { 
      "line_1": ["street_lv"],
      "line_2": ["city_lv"], 
      "line_3": ["postcode"] 
    }
  },
  "United Kingdom": {
    "address": {
      "street_lv": { "name": "address", "type": "string", "note": "house/building number, street name" },
      "city_lv":   { "name": "town/city", "type": "string" },
      "postcode":  { "name": "postal code", "type": "string", "pattern": "xxxx xxx" }
    },
    "format": { 
      "line_1": ["street_lv"],
      "line_2": ["city_lv"], 
      "line_3": ["postcode"] 
    }
  },
  "United States": {
    "address": {
      "street_lv": { "name": "address", "type": "string", "note": "house/building number, street name" },
      "city_lv":   { "name": "city", "type": "string" },
      "state_lv": { "name": "state", "type": "string" },
      "postcode":  { "name": "zip code", "type": "numeric", "pattern": "xxxxx" }
    },
    "format": { 
      "line_1": ["street_lv"],
      "line_2": ["city_lv", "state_lv", "postcode"]
    }
  },
  "Uruguay": {
    "address": {
      "street_lv": { "name": "address", "type": "string", "note": "street name, house/building number, apartment, floor" },
      "city_lv":   { "name": "town/city", "type": "string" },
      "state_lv": { "name": "province", "type": "string" },
      "postcode":  { "name": "postal code", "type": "numeric", "pattern": "xxxxx" }
    },
    "format": { 
      "line_1": ["street_lv"],
      "line_2": ["postcode", "city_lv", "state_lv"]
    }
  },
  "Wales": {
    "address": {
      "street_lv": { "name": "address", "type": "string", "note": "house/building number, street name" },
      "city_lv":   { "name": "town/city", "type": "string" },
      "postcode":  { "name": "postal code", "type": "string", "pattern": "xxxx xxx" }
    },
    "format": { 
      "line_1": ["street_lv"],
      "line_2": ["city_lv"], 
      "line_3": ["postcode"] 
    }
  },

  "Netherlands":{
    "address":{
      "street_lv": { "name": "address", "type": "string", "note": "house/building number, street name" },
      "city_lv":   { "name": "town/locality", "type": "string" },
      "postcode":  { "name": "postal code", "type": "string", "pattern": "xxxx xx" }
    },
    "format":{
      "line_1": ["street_lv"],
      "line_2": ["postcode","city_lv"]
    }
  },
  
  "New Zealand":{
    "address":{
      "street_lv": { "name": "address", "type": "string", "note": "house/building number, street name" },
      "city_lv":   { "name": "town/city", "type": "string" },
      "postcode":  { "name": "postal code", "type": "string", "pattern": "xxxx" }
    },
    "format":{
      "line_1": ["street_lv"],
      "line_2": ["city_lv","postcode"]
    }
  },
  
  "Norway":{
    "address":{
      "street_lv": { "name": "address", "type": "string", "note": "house/building number, street name" },
      "city_lv":   { "name": "town/city", "type": "string" },
      "postcode":  { "name": "postal code", "type": "string", "pattern": "xxx" }
    },
    "format":{
      "line_1": ["street_lv"],
      "line_2": ["postcode","city_lv"]
    }
  },

  "Oman":{
    "address":{
      "street_lv": { "name": "address", "type": "string", "note": "house/building number, street name" },
      "city_lv":   { "name": "town/city", "type": "string" },
      "postcode":  { "name": "postcode", "type": "string", "pattern": "xxx" }
    },
    "format":{
      "line_1": ["street_lv"],
      "line_2": ["postcode"], 
      "line_3": ["city_lv"]
    }
  },
 
  "Pakistan":{
    "address":{
      "street_lv": { "name": "address", "type": "string", "note": "house/building number" },
      "street_lv2": { "name": "address2", "type": "string", "note": "street name"},
      "subdiv_lv": { "name": "sector", "type": "string"},
      "city_lv":   { "name": "town/city", "type": "string" },
      "postcode":  { "name": "postal code", "type": "string", "pattern": "xxxxx" }
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
      "street_lv": { "name": "address", "type": "string", "note": "house/building number, street name" },
      "city_lv":   { "name": "town/locality", "type": "string" },
      "postcode":  { "name": "postal code", "type": "string", "pattern": "xx-xxx" }
    },
    "format":{
      "line_1": ["street_lv"],
      "line_2": ["postcode","city_lv"]
    }
  },
  
  "Portugal":{
    "address":{
      "street_lv": { "name": "address", "type": "string", "note": "street name, house/building number" },
      "city_lv":   { "name": "town/city", "type": "string" },
      "state_lv":  { "name": "territorial subdivision", "type": "string" },
      "postcode":  { "name": "postal code", "type": "string", "pattern": "xxxx-xxx" }
    },
    "format":{
      "line_1": ["street_lv"],
      "line_2": ["city_lv"],
      "line_3": ["postcode", "state_lv"]
    }
  },
    
  "Puerto Rico":{
    "address":{
      "street_lv": { "name": "address", "type": "string", "note": "street name, house/building number" },
      "city_lv":   { "name": "town/city", "type": "string" },
      "state_lv":  { "name": "state", "type": "string" },
      "postcode":  { "name": "zip code", "type": "string", "pattern": "xxxxx" }
    },
    "format":{
      "line_1": [ "street_lv"],
      "line_2": [ "city_lv"],
      "line_3": [ "state_lv","postcode" ]
    }
  }, 
    
  "Romania":{
    "address":{
      "street_lv": { "name": "address", "type": "string", "note": "street name, house/building number" },
      "city_lv":   { "name": "town/city", "type": "string" },
      "state_lv":  { "name": "sector", "type": "string" },
      "postcode":  { "name": "postal code", "type": "string", "pattern": "xxxxx" }
    },
    "format":{
      "line_1": [ "street_lv"],
      "line_2": [ "postcode", "city_lv"],
      "line_3": [ "state_lv" ]
    }
  },  
   
  "Russia":{
    "address":{
      "street_lv": { "name": "address", "type": "string", "note": "street name, house/building number" },
      "city_lv":   { "name": "town/city", "type": "string" },
      "state_lv":  { "name": "province", "type": "string" },
      "postcode":  { "name": "postal code", "type": "string", "pattern": "xxxxxx" }
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
      "street_lv": { "name": "address", "type": "string", "note": "street name, house/building number" },
      "city_lv":   { "name": "town/city", "type": "string" },
      "postcode":  { "name": "post code", "type": "string", "pattern": "xxxxxx" }
    },
    "format":{
      "line_1": [ "street_lv"],
      "line_2": [ "city_lv","postcode"]   
    }
  },  
    
  "SouthAfrica":{
    "address":{
      "street_lv": { "name": "address", "type": "string", "note": "street name, house/building number" },
      "city_lv":   { "name": "town/city", "type": "string" },
      "postcode":  { "name": "post code", "type": "string", "pattern": "xx" }
    },
    "format":{
      "line_1": [ "street_lv"],
      "line_2": [ "city_lv"],
      "line_3": [ "postcode"]
    }
  },    
    
  "SouthKorea":{
    "address":{
      "street_lv": { "name": "address", "type": "string", "note": "house/building number, street name" },
      "subdiv_lv": { "name": "subdivision", "type": "string"},
      "city_lv":   { "name": "town/city", "type": "string" },
      "postcode":  { "name": "post code", "type": "string", "pattern": "xxx-xxx" }
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
      result = country_format[country]
      print(result)
    except Exception as a:
        return jsonify({"error":str(a)})
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 8000, debug = True)

