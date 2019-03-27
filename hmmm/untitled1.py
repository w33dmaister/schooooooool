import json, urllib2, datetime, os
from flask import Flask, render_template, jsonify, make_response
from dicttoxml import dicttoxml

app = Flask(__name__)

def wpjson(mesto):
    r = urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?id='+mesto+'&appid=61afef4737d2b6a1483bf59e94d705fd&lang=cz')
    data=json.load(r)
    return data

def loadCities():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "cities.json")
    data = json.load(open(json_url))
    return data

def iservery():
    r=urllib2.urlopen('https://blog.iservery.com/wp-json/wp/v2/posts')
    data=json.load(r)
    pole=[]
    for radek in data:
        inradek=dict(content=radek['content']['rendered'],title=radek['title']['rendered'])
        pole.append(inradek)
    return pole

@app.route('/show/<string:mesto>')
def mesto(mesto):
    data=wpjson(mesto)
    data['sys']['sunrise']=datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%-M')
    data['sys']['sunset'] = datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%-M')
    data['dt'] = datetime.datetime.fromtimestamp(data['dt']).strftime('%-d.%-m.%Y %-H:%-M:%-S')
    return render_template('index.jinja2',data=data)

@app.route('/')
def index():
    data=loadCities()
    pole=[]

    for m in data:
        if(m['country'] == 'CZ'):
            pole.append(m)
        #pole.append(m)
    return render_template('mesta.jinja2',data=pole)

@app.route('/blog/<string:type>')
def blog(type):
    if (type=="xml"):
        response = make_response(dicttoxml(iservery(), attr_type=False))
        response.headers["Content-Type"] = "application/xml"
        return response
    elif (type=="json"):
        return jsonify(iservery())
    elif (type=="csv"):
        data=iservery()
        output = make_response(jsonify(data))
        #output.headers["Content-type"] = "text/csv"
        return output
    else:
        return "404"

if __name__ == '__main__':
    app.run()
