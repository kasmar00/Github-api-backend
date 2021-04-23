import json
import urllib.request
import re


from flask_restful import Resource
from flask import request


class github(Resource):
    @staticmethod
    def getUrl(username):
        # if not re.match("^([a-z\d]+-)*[a-z\d]+$", username):
        if "" == username or " " in username or "/" in username:
            raise Exception("Bad username")
        try:
            with urllib.request.urlopen(f"https://api.github.com/users/{username}/repos") as response:
                data = json.loads(response.read())
            return data
        except:
            raise Exception("User not found")

    @staticmethod
    def extractData(data):
        ret = []

        for i in data:
            element = {}
            element["name"] = i["name"]
            element["stars"] = i["stargazers_count"]
            ret.append(element)
        return ret

    @staticmethod
    def handler(e):
        print(e)
        code = 200
        if "Bad username" == str(e):
            code = 400
        elif "User not found" == str(e):
            code = 204
        return [], code


class List(github):
    def get(self):
        args = request.args
        user = args.get("user")
        try:
            data = self.getUrl(user)
            return self.extractData(data)
        except Exception as e:
            return self.handler(e)


class Stars(github):
    @staticmethod
    def starSum(data):
        x = 0
        for i in data:
            x += i["stars"]
        return x

    def get(self):
        args = request.args
        user = args.get("user")

        try:
            data = self.getUrl(user)
            ex = self.extractData(data)

            return self.starSum(ex)

        except Exception as e:
            return self.handler(e)
