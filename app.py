from flask import Flask, render_template, redirect, url_for, request
from controller import controller
import json
app = Flask(__name__)

API_KEY = "AIzaSyBqzhFzwq7FvtAFnoEc7SD-eenOWC4_luU"


@app.route('/', methods=["POST", "GET"])
def hello_world():
    if request.method == "GET":
        context = {}
        context['newsFeed'] = controller.getNewsHeading(5)
        context['cityList'] = controller.getPlaces()
        context['unesco'] = controller.getUNESCOPlaces()
        context['popular_dest'] = controller.popularDest(5)
        context['safe_states'] = controller.safestStates(5)
        return render_template('index.html', context=context)
    else:
        return 'Hello Govind'


@app.route('/admin', methods=["POST", "GET"])
def admin():
    if request.method == "GET":
        context = {}
        return render_template('admin.html', context=context)
    else:
        return 'Hello Govind'


@app.route('/page', methods=["POST", "GET"])
def hello():
    print('************ Find Path ********************')
    try:
        src, sstate = request.form['srcCity'].split(',')
        dest, dstate = request.form['destCity'].split(',')
        src,sstate,dest,dstate = src.strip(),sstate.strip(),dest.strip(),dstate.strip()
        print("^^^^^^^^^", src, dest)
        foundPath, data = controller.safePath(src, dest)
    except Exception as e:
        print("Exception ", e)
        foundPath = []
        data = {}

    if len(foundPath) > 1:
        waypoint = '|'.join(foundPath)
    elif len(foundPath) == 1:
        waypoint = foundPath[0]
    else:
        waypoint = None

    # print("waypoint", " ", waypoint)

    src = src +'+' + sstate
    dest = dest +'+' + dstate

    ret = {}
    
    # make google map API call here
        waypoint = []
    ret['url'] = url
    ret['foundPath'] = '-->'.join(foundPath)
    ret['foundPath1'] = foundPath
    ret['data'] = data
    return ret


@app.route('/login', methods=["POST", "GET"])
def login():
    uname = request.form['uname'].strip()
    psw = request.form['psw'].strip()
    print('********** ', uname, " pass ", psw)
    ret = {}
    if controller.isAdmin(uname, psw):
        ret['status'] = 'pass'
        ret['msg'] = 'Welcome:'  + uname
    else:
        ret['status'] = 'fail'
        ret['msg'] = uname + ' Does Not exits'
    return ret


@app.route('/createUser', methods=["POST", "GET"])
def createUser():
    uname = request.form['uname']
    psw = request.form['psw']
    ret = {}
    if controller.createUser(uname, psw):
        ret['status'] = 'pass'
        ret['msg'] = uname + ' Successfully Created'
    else:
        ret['status'] = 'fail'
        ret['msg'] = uname + ' Cannot create user'
    return ret


@app.route('/createNews', methods=["POST", "GET"])
def createNews():
    newsTag = request.form['newsTag']
    newsHeading = request.form['newsHeading']
    newsDetails = ""
    print('^^^^^^^^^^ ', newsTag,  newsHeading, newsDetails)
    ret = {}
    if controller.createNews(newsTag, newsHeading,newsDetails):
        ret['status'] = 'pass'
        ret['msg'] = newsHeading + ' Successfully Created News'
    else:
        ret['status'] = 'fail'
        ret['msg'] = newsHeading + ' Cannot create News'
    return ret



@app.route('/createPlace', methods=["POST", "GET"])
def createPlace():
    district = request.form['district']
    state = request.form['state']
    lat = request.form['lat']
    longi = request.form['longi']
    print('^^^^^^^^^^ ', district,  state, lat, longi)
    ret = {}
    if controller.createPlace(district, state, lat, longi):
        ret['status'] = 'pass'
        ret['msg'] = district + ' Successfully Created New Place'
    else:
        ret['status'] = 'fail'
        ret['msg'] = district + ' Cannot create Place'
    return ret


@app.route('/createUnesco', methods=["POST", "GET"])
def createUnesco():
    unesco_site_name = request.form['unesco_site_name']
    district = request.form['district']
    state = request.form['state']
    print('^^^^^^^^^^ ', unesco_site_name, district,  state)
    ret = {}
    if controller.createUnesco(unesco_site_name, district, state):
        ret['status'] = 'pass'
        ret['msg'] = district + ' Successfully Created New Unesco Site'
    else:
        ret['status'] = 'fail'
        ret['msg'] = district + ' Cannot create Unesco Site'
    return ret

@app.route('/insertActiveCases', methods=["POST", "GET"])
def insertActiveCases():
    district = request.form['district']
    active_cases = request.form['active_cases']
    active_cases_date = request.form['active_cases_date']

    print('^^^^^^^^^^ ', district, active_cases,  active_cases_date)
    ret = {}
    if controller.insertActiveCases(district, active_cases, active_cases_date):
        ret['status'] = 'pass'
        ret['msg'] = district + ' Active Cases Successfully Stored'
    else:
        ret['status'] = 'fail'
        ret['msg'] = district + ' Active Cases Cannot Store'
    return ret


@app.route('/getPlaceDataList', methods=["POST", "GET"])
def getPlaceDataList():
    context = {}
    context['list'] = controller.getPlaceDataList()
    return context

@app.route('/getUserDataList', methods=["POST", "GET"])
def getUserDataList():
    print("*******************************")
    context = {}
    context['list'] = controller.getUserDataList()
    return context

@app.route('/getUnescoDataList', methods=["POST", "GET"])
def getUnescoDataList():
    context = {}
    context['list'] = controller.getUnescoDataList()
    print("*******************************", context)

    return context

@app.route('/getNewsDataList', methods=["POST", "GET"])
def getNewsDataList():
    print("*******************************")
    context = {}
    context['list'] = controller.getNewsDataList()
    return context


@app.route('/deleteFiled', methods=["POST", "GET"])
def deleteFiled():
    type1 = request.form['type']
    key = request.form['key']
    print(type1, " ", key)
    ret = {}
    ret['status'] = 'pass'
    ret['msg'] = 'Deletion Successfully Performed'
    if type1 == 'user':
        if(controller.deleteUser(key)): return ret
    if type1 == 'news':
        if(controller.deleteNews(key)): return ret
    if type1 == 'place':
        if(controller.deletePlace(key)): return ret
    if type1 == 'unesco':
        if(controller.deleteUnesco(key)): return ret

    ret['status'] = 'fail'
    ret['msg'] = "deletion of " + type1 + " failed"
    return ret

if __name__ == "__main__":
    app.run(debug=True, port=8000)