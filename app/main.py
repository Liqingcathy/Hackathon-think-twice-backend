import json
from flask import Flask, jsonify, request
from app import create_app
import requests
import os
from bson import json_util
from pymongo import MongoClient

# from model.users import User
# from model.account import Account

app, pymongo = create_app()
# client = MongoClient("mongodb://localhost:27017/")

replace_db_accounts = []

@app.route('/user_balance', methods=['POST'])
def create_users():
    #create user collections
    users: Collection = pymongo.db.finance
    users = pymongo.db.users
    response_body = request.get_json()
    if response_body:
        customer_id = response_body['customer_id']
        # if users.find_one({'customer_id' : customer_id}):
        #     return jsonify({'msg' : 'User with the give customer id already exists'}), 400
        
        user = {
            'name': response_body['name'],
            'email': response_body['email'],
            'customer_id': response_body['customer_id']
        }

        users.insert_one(user)        
        response = requests.get(
            f'http://api.nessieisreal.com/customers/{customer_id}/accounts?key={os.environ.get("CAPITAL_ONE_API")}'
        ).json()
        print(response)

        #save accounts collection to mongodb
        store_user_by_accounts(response)
        #sent data to client
        balance_by_act_type = json.dumps(get_all_balance(response))

    else:
        return {"msg" : "Invalid data response"}, 400
    return balance_by_act_type

@app.route('/user_accounts', methods=['POST'])
def store_user_by_accounts(accounts_list_response):
    accounts: Collection = pymongo.db.finance
    accounts = pymongo.db.accounts
    for account in accounts_list_response:
        by_account = {
                'nickname': account['nickname'],
                'type': account['type'],
                'balance' : account['balance'],
                'customer_id': account['customer_id']
        }

        accounts.insert_one(by_account) 
    return {'msg' : 'accounts are saved'}, 201

def get_all_balance(acct_list):
    account_res = []
    for account in acct_list:
        balance_dict = {}
        balance_dict['type'] = account['type']
        balance_dict['balance'] = account['balance']
        account_res.append(balance_dict)
    return account_res

@app.route('/users', methods=['GET'])
def get_users():
    users = pymongo.db.users.find()
    return json_util.dumps(users)

@app.route('/users_accounts', methods=['GET'])
def get_users_accounts():
    accounts = pymongo.db.accounts.find()
    return json_util.dumps(accounts)


@app.route('/user/<email>', methods=['GET'])
def get_one_user(email):
    user = pymongo.db.users.find_one({'email': email})
    print('match email user', user)
    return {'msg' : 'Found match'}, 200

