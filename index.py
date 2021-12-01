# -*- coding: utf-8 -*-
from flask_api import FlaskAPI
from settings import *
from lib.mysql import MysqlPython

#
app = FlaskAPI(__name__)
app.debug = DEBUG

# Kết nối DB MySQL 
DB = MysqlPython(host=DB_HOST, port=DB_PORT,user=DB_USERNAME,
                 password=DB_PASSWORD, database=DB_DATABASE)

@app.route("/", methods=['GET'])
def home():
    return "OK"

#api
@app.route("/api/list-comment", methods=['GET']) 
def api_list_comment():
    comment_list = []
    rs = DB.query("SELECT * FROM `comments` ORDER BY `id` DESC LIMIT 8")
    if rs:
        for item in rs:
            comment = {
                "user_name"     :   item.get('user_name'),
                "comment"       :   item.get('comment'),
                "comment_at"    :   item.get('created_at').strftime("%H:%M")
            }
            comment_list.append(comment)
        comment_list.reverse()        
    return comment_list        

# Not found
@app.errorhandler(404)
def not_found(error=None):
    return "Not found"    

if __name__ == "__main__":
    #logging
    import logging
    import os 
    log_file = os.path.join(LOG_FOLDER, "error.log")
    logging.basicConfig(filename=log_file,level=logging.DEBUG)
    
    if DEBUG:        
        app.run('0.0.0.0', port=APP_PORT)
    else:
        from waitress import serve
        serve(app, host="0.0.0.0", port=APP_PORT) 
