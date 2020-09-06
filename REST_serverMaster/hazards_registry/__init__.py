#i try to avoid using shelve here

import markdown
import os
import shelve

# Import the framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse


from socket import * 
import sys
import threading
import time
import queue


import argparse
import json 

parser = argparse.ArgumentParser()
parser.add_argument("server_ID", help="type the server ID (s1,s2...)")
args = parser.parse_args()

App_ID=args.server_ID #the given Vehicle ID must match with the one of the scenario



server_ports_path="/home/jaime/Desktop/code/AdvantEDGE/2020-04-11/code/scenarios/server_ports.json"

#Opens the scenario file specified in <scenario_path>
with open(server_ports_path) as json_file:
    server_ports = json.load(json_file)


#print (server_ports[App_ID]['port_tcp'])
#print (server_ports[App_ID]['port_udp'])




server_port=server_ports[App_ID]['port_tcp']
downlink_port= (server_ports[App_ID]['port_downlink'])



q_hazard = queue.Queue()
id_hazard_db=0
id_vehicle_db=0

def init_db():
    global db
    db = g._database = shelve.open("vehicles.db")
def create_app():
    app = Flask(__name__)

    with app.app_context():
        pass
		#init_db()

    return app

app = create_app()

api = Api(app)
shelf = {}
Vehicles_in_server = {}
def get_db():
    global db
    """# check if _database attribute exist
    db = getattr(g, '_database', None)
	# if doesnt, establish a new connection and save _database attribute
    # this prevents multiple instances to the database
    if db is None:
        #db = g._database = shelve.open("devices.db")
       db= shelve.open("devices.db")"""
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    """Present some documentation"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        # Read the content of the file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)





class VehicleList(Resource):
    def get(self):
        global Vehicles_in_server
		
        keys = list(Vehicles_in_server.keys())

        detected_vehicless = []

        for key in keys:
            detected_vehicless.append(Vehicles_in_server[key])

        return {'message': 'Success', 'data': detected_vehicless}, 200

    def post(self):
        global id_vehicle_db
        global Vehicles_in_server
        parser = reqparse.RequestParser()

        parser.add_argument('id', required=True)
        parser.add_argument('port', required=True)
        
		# Parse the arguments into an object
        args = parser.parse_args()
        Vehicle_ID=args.id 
        
		
		
		

        Vehicles_in_server[str(Vehicle_ID)] = args
        id_vehicle_db=id_vehicle_db+1
	
        return  {'message': 'OK'},201






class HazardList(Resource):
    def get(self):
        global shelf
		
        keys = list(shelf.keys())

        detected_hazards = []

        for key in keys:
            detected_hazards.append(shelf[key])

        return {'message': 'Success', 'data': detected_hazards}, 200

    def post(self):
        global id_hazard_db
        global shelf
        parser = reqparse.RequestParser()

        parser.add_argument('id', required=True)
        parser.add_argument('sn', required=True)
        parser.add_argument('ht', required=True)
        parser.add_argument('l', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        args["sn"]=App_ID

        self.validate_hazard(args)
        if self.validate_hazard(args):
            id_hazard_db= id_hazard_db+1
            shelf[str(id_hazard_db)] = args
        #print ("updating queue", args)
        q_hazard.put(args)
		#print(self.get())
		#TODO: change shelf[args['id']] for a local id given by the server
        #data=get_hazard(id)
        
		
        return  {'message': 'OK'},201
        #return {'message': 'hazard registered', 'data': args}, 201
    def validate_hazard(self, hazard):
        global shelf
        validation=True
		
        keys = list(shelf.keys())

        detected_hazards = []

        for key in keys:
            #detected_hazards.append(shelf[key])
            location_db=float(shelf[key]["l"])
            new_hazard_location=float(hazard["l"])
            loc_validation= abs(location_db-new_hazard_location)
            #print(location_db, new_hazard_location, shelf[key]["ht"], hazard["ht"])
            if shelf[key]["ht"]==hazard["ht"] and loc_validation<1:
                #print("hazard already detected")
                validation=False

        return validation		
		
        

		

class Hazard(Resource):
    def get(self, identifier):
        global shelf
		#shelf = get_db()
        #print (identifier)
        # If the key does not exist in the data store, return a 404 error.
        if not (identifier in shelf):
            return {'message': 'hazard not found', 'data': {}}, 404

        return {'message': 'hazard found', 'data': shelf[identifier]}, 200

    def delete(self, identifier):
        global shelf
		#shelf = get_db()

        # If the key does not exist in the data store, return a 404 error.
        if not (identifier in shelf):
            return {'message': 'hazard not found', 'data': {}}, 404

        del shelf[identifier]
        return '', 204



api.add_resource(HazardList, '/detected_hazard')
api.add_resource(Hazard, '/detected_hazard/<string:id>')
api.add_resource(VehicleList, '/vehiclelist')


"""
UDP_IP = '127.0.0.1' #
UDP_PORT = server_ports[App_ID]['port_udp'] #The port to be set in the ingress mapping in AdvantEDGE

BROADCAST='255.255.255.255'
BUFFER_SIZE = 1024

cs = socket(AF_INET, SOCK_DGRAM)
#cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

def thread_poster():
    global Vehicles_in_server
    while True:
	
        myhazard = q_hazard.get()
        output=str(myhazard)
        print(output)
        cs.sendto(output.encode('utf-8') , (UDP_IP,UDP_PORT )) #the same port we bind on the rx
        print("sent hazard")
        for vehicles in Vehicles_in_server:
            #print(Vehicles_in_server)
            myport=int(Vehicles_in_server[vehicles]["port"])
            #cs.sendto(output.encode('utf-8') , (BROADCAST, myport)) #the same port we bind on the rx
            
        time.sleep(0.01)








x0_poster = threading.Thread(target=thread_poster, args=())
x0_poster.daemon = True
x0_poster.start()
"""