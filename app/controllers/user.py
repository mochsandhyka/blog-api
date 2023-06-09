from flask import request
from json_checker import Checker
from app import db, request_mapping, request_struct, response_handler
from app.hash import hash_password
from uuid import uuid4
from datetime import datetime
from app.models.user import User
from app.models.address import Address
from app.response_validator import *
from sqlalchemy import update

def create_user():
    try:
        json_body = request.json
        data = request_mapping.create_user(json_body)
        result = Checker(request_struct.User(), soft=True).validate(data)
        
        select_user = User.query.all()

        # iterasi tbl_user
        list = []
        for i in select_user:
            list.append({
                "username": i.username,
                "email": i.email
            })
        
        # validate if username and email is exist
        for i in list:
            if result['username'] == i['username']:
                return response_handler.bad_request('Username is Exist')
            elif result['email'] == i['email']:
                return response_handler.bad_request('Email is Exist')
                
        # validate field
        validator = validator_user(request)   
        if not validator.validate():
            errors = validator.errors
            for field in result:
                if field in errors:
                    return response_handler.bad_request(errors['{field}'][0])
            return response_handler.bad_request(errors)

        # tbl_address
        id_address = uuid4()
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

        data = {
            "id_user": user.id_user,
            "name": user.name,
            "email": user.email,
            "password": user.password,
            "created_at": user.created_at,
            "id_address": user.id_address
        }
        return response_handler.created(data, 'User Successfull Created')
    
    except KeyError as err:
        return response_handler.bad_request(f'{err.args[0]} field must be filled')
    
    except Exception as err:
        return response_handler.bad_gateway(str(err))
    
def read_user(id):
    try:
        
        id_user = User.query.values(User.id_user)
        exist = False
        for i in id_user:
            if(str(i.id_user) == id):
                exist = True
                break
        
        if not exist:
            return response_handler.not_found('User Not Found')
        
        user = User.query.get(id)
        address = user.address
        
        data = {
            "id_user": user.id_user,
            "name": user.name,
            "email": user.email,
            "password": user.password,
            "created_at": user.created_at,
            "address": {
                "id_address": address.id_address,
                "address": address.address,
                "rt": address.rt,
                "rw": address.rw,
                "kelurahan_desa": address.kelurahan_desa,
                "kecamatan": address.kecamatan
            }
        }
        return response_handler.ok(data,"")

    except Exception as err:
        return response_handler.bad_gateway(str(err))
    
def update_user(id):
    try:
        id_user = User.query.all()
        exist = False
        for i in id_user:
            if(str(i.id_user) == id):
                exist = True
                break
            
        if not exist:
            return response_handler.not_found('User Not Found')
        
        json_body = request.json
        data = request_mapping.update_user(json_body)
        result = Checker(request_struct.update_user(), soft=True).validate(data)

        validator = validator_update_user(request)
        if not validator.validate():
            errors = validator.errors
            for field in result:
                if field in errors:
                    return response_handler.bad_request(errors['{field}'][0])
            return response_handler.bad_request(errors)
        
        
        user = User.query.filter_by(id_user = id).first()
        address = user.address

        if result['username'] == user.username:
            user.username = result['username']
        else:
            existing_user = User.query.filter_by(username=result['username']).first()
            if existing_user:
                return response_handler.bad_request('Username already exists')

        user.name = result['name']
        user.username = result['username']
        user.email = result['email']
        user.password = hash_password(result['password'])
        address.address = result['address']
        address.rt = result['rt']
        address.rw = result['rw']
        address.kelurahan_desa = result['kelurahan_desa']
        address.kecamatan = result['kecamatan']

        db.session.commit()

        data = {
            "id_user": user.id_user,
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "password": user.password,
            "address": address.address,
            "rt": address.rt,
            "rw": address.rw,
            "kelurahan_desa": address.kelurahan_desa,
            "kecamatan": address.kecamatan
        }
        return response_handler.ok(data, "Your data is updated")

    except KeyError as err:
        return response_handler.bad_request(f'{err.args[0]} field must be filled')
    
    except Exception as err:
        return response_handler.bad_gateway(str(err))
    
def delete_user(id):
    try:
        id_user = User.query.all()
        exists = False
        for i in id_user:
            if (str(i.id_user) == id):
                exists = True
                break

        if not exists:
            return response_handler.not_found('User Not Found')
        
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return response_handler.ok("","User Successfull Deleted")
    
    except Exception as err:
        return response_handler.bad_gateway(err)

def list_user():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int )
        total_user = User.query.count()
        if not per_page:
            per_page = total_user

        user = User.query.order_by(User.created_at.desc()).paginate(page = page, per_page = per_page)
        data = []
        for i in user.items:
            data.append({
                "id_user": i.id_user,
                "name": i.name,
                "username": i.username,
                "email": i.email,
                "password": i.password,
                "address.address": i.address.address,
                "address.rt": i.address.rt,
                "address.rw": i.address.rw,
                "address.kelurahan_desa": i.address.kelurahan_desa,
                "address.kecamatan": i.address.kecamatan
            })
        meta = {
            "page": user.page,
            "pages": user.pages,
            "total_count": user.total,
            "prev_page": user.prev_num,
            "next_page": user.next_num,
            "has_prev": user.has_prev,
            "has_next": user.has_next
        }
        return response_handler.ok_with_meta(data,meta)
    except Exception as err:
        return response_handler.bad_gateway(err)
        
