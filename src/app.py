"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure, Member
from werkzeug.exceptions import BadRequest, InternalServerError
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    try:
        members = jackson_family.get_all_members()
        response_body = {
            "family members": members,
            "total members": len(members)
        }
        return jsonify(response_body), 200
    except BadRequest as e:
        return jsonify({'message': 'Bad request'}), e.code
    except InternalServerError as e:
        return jsonify({'message': 'Internal server error'}), e.code
    except:
        return jsonify({'message': 'Unexpected error'})

@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        return jsonify(member), 200
    except BadRequest as e:
        return jsonify({'message': 'Bad request'}), e.code
    except InternalServerError as e:
        return jsonify({'message': 'Internal server error'}), e.code
    except:
        return jsonify({'message': 'Unexpected error'})

@app.route('/members/create', methods=['POST'])
def create_member():
    try:
        member = request.get_json()
        member = jackson_family.add_member(member)
        return jsonify({'message': member['first_name'] + ' created successfully'}), 200
    except BadRequest as e:
        return jsonify({'message': 'Bad request'}), e.code
    except InternalServerError as e:
        return jsonify({'message': 'Internal server error'}), e.code
    except:
        return jsonify({'message': 'Unexpected error'})

@app.route('/members/<int:member_id>/delete', methods=['DELETE'])
def delete_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        jackson_family.delete_member(member_id)
        return jsonify({'message': member['first_name'] + ' deleted successfully'}), 200
    except BadRequest as e:
        return jsonify({'message': 'Bad request'}), e.code
    except InternalServerError as e:
        return jsonify({'message': 'Internal server error'}), e.code
    except:
        return jsonify({'message': 'Unexpected error'})

@app.route('/members/<int:member_id>/update', methods=['PUT'])
def update_member(member_id):
    try:
        new_member = request.get_json()
        jackson_family.update_member(member_id, new_member)
        return jsonify({'message': new_member['first_name'] + ' updated successfully'}), 200
    except BadRequest as e:
        return jsonify({'message': 'Bad request'}), e.code
    except InternalServerError as e:
        return jsonify({'message': 'Internal server error'}), e.code
    except:
        return jsonify({'message': 'Unexpected error'})  
        
#* Note on PUT/POST/PATCH
# It is also important to keep in mind that when using PUT method all the information is mandatory, the whole resource, in contrast to PATCH method that can update only a subset of a resource.
# However, in practice, many APIs use POST for updating resources as well, because it is more flexible and allows for partial updates.
# It's important to keep in mind that while POST method allows more flexibility, it also requires additional handling and validation on the server side to ensure that the correct fields are being updated, whereas PUT method can rely on the client to send the entire resource and replace it.  

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
