# See LICENSE file for reasons!

import json
import os

class Server:
    def __init__(self):
        self.config = {}
        if os.path.exists("server.json"):
            with open("server.json") as f:
                self.config = json.load(f)
        self.tokens = {}
        self.online = self.config["online"]
        self.name = self.config["name"]

    def check_token(self, token):
        for t in self.tokens:
            if token == t:
                return self.tokens[t]
        return None
    
    def delete_token(self, token):
        for t in self.tokens:
            if token == t:
                del self.tokens[t]

    def insert_token(self, token, username):
        self.tokens[token] = username

