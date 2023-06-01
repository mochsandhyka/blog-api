from flask import request
from json_checker import Checker
from app import db, request_mapping, request_struct, prefix_middleware, response_handler
from app.hash import hash_password
from uuid import uuid4
from datetime import datetime
from app.models.user import User
from app.models.address import Address
from app.validator import validator_user, validator_response

def create_user():
    try:
        id_address = uuid4()
        json_body = request.json
        data = request_mapping.create_user(json_body)
        result = Checker(request_struct.User(), soft=True).validate(data)
        
        # validate field
        validator = validator_user(request)   
        if not validator.validate():
            errors = validator.errors
            for field in result:
                if field in errors:
                    return response_handler.bad_request(validator_response(errors['{field}'][0]))
            return response_handler.bad_request(validator_response(errors))

        # tbl_address
        address = Address(id_address = id_address)

        # tbl_user
        user = User(id_user = uuid4(), 
                    name = result['name'],
                    username = result['username'],
                    email = result['email'],
                    password = hash_password(result['password']),
                    created_at = datetime.now(),
                    address = address
                    )
        
        db.session.add(address,user)
        db.session.commit()

        response = {
            "code": "201",
            "status": "CREATED",
            "data": {
                "id_user": user.id_user,
                "name": user.name,
                "email": user.email,
                "password": user.password,
                "created_at": user.created_at,
                "id_address": user.id_address
            },
            "message": "Successfull Create User"
        }
        return response_handler.created(response)
  
    except Exception as err:
        response = {
            "code": "500",
            "status": "BAD_GATEWAY",
            "error": str(err)
        }
        return response_handler.bad_gateway(response)