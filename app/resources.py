import json
import requests
from typing import List, Dict, Tuple, AnyStr
import os


from flask_restful import Resource
from flask import request


class github(Resource):
    """
    Class for storing functions used by all routes

    Those include:
        downloading data from api,
        extracting data,
        handling exceptions
    """

    @staticmethod
    def getUrl(username: AnyStr) -> List[Dict]:
        """
        Downloads data from api

        Parameters:
            username - username (github handle) for which the data will be downloaded

        Returns:
            data - list of dictionaries downloaded from github api
        """
        if "" == username or " " in username or "/" in username:
            raise Exception("Bad username")
        try:
            auth = (os.environ.get("gh_user", ""),
                    os.environ.get("gh_token", ""))
            req = requests.get(
                f"https://api.github.com/users/{username}/repos", auth=auth)
            # print(req.status_code)
            if req.status_code == 200:
                data = json.loads(req.content)
                return data
            else:
                raise Exception(f"Error {req.status_code}")
                # 404 etc are passed here and cached below as user not found, that may require a change
        except Exception as e:
            print(e)
            raise Exception("User not found")

    @staticmethod
    def extractData(data: List[Dict]) -> List[Dict]:
        """
        Extracts downloaded data

        Extracts intresting info (name and number of stars)
        from list of repositories produced by getUrl method

        Parameters:
            data - data returned by getUrl (List of dictionaries)

        Returns:
            list of dictionaries, same format as input data
            but only with important information
        """
        ret = []

        for i in data:
            element = {}
            element["name"] = i["name"]
            element["stars"] = i["stargazers_count"]
            ret.append(element)
        return ret

    @staticmethod
    def handler(e: Exception) -> Tuple[None, int]:
        """
        Handles exceptions thrown by getUrl method

        Parameters:
            exception of class Exception with string describing the problem

        Returns:
            None value (as data) and http response code
        """
        print(e)
        code = 200
        if "Bad username" == str(e):
            code = 400
        elif "User not found" == str(e):
            code = 204
        return None, code


class ListRep(github):
    """
    Class for handling queries for list of repositories
    """

    def get(self):
        """
        Method to handle get requests

        Returns:
            Data (json list of repositories), on exception data provided
            from exception handler with proper response code
        """
        args = request.args
        user = args.get("user")
        try:
            data = self.getUrl(user)
            return self.extractData(data)
        except Exception as e:
            return self.handler(e)


class Stars(github):
    """
    Class for handling queries for total number of stars on repositories
    """

    @staticmethod
    def starSum(data: List[Dict]) -> int:
        """
        Counts sum of stars in data provided from extractData method

        Parameters:
            data - data returned by extractData (List of dictionaries)

        Returns:
            single int - sum of numbers of stars
        """
        x = 0
        for i in data:
            x += i["stars"]
        return x

    def get(self):
        """
        Method to handle get requests

        Returns:
            Data (single int), on exception data provided
            from exception handler with proper response code
        """
        args = request.args
        user = args.get("user")

        try:
            data = self.getUrl(user)
            ex = self.extractData(data)

            return self.starSum(ex)

        except Exception as e:
            return self.handler(e)
