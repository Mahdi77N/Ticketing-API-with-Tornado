import os.path
import torndb
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os
import datetime
from binascii import hexlify
import tornado.web
from tornado.options import define, options


define("port", default=1104, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="database host")
define("mysql_database", default="tickets", help="database name")
define("mysql_user", default="system", help="database user")
define("mysql_password", default="1*001/", help="database password")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # Get Method
            (r"/signup/([^/]+)/([^/]+)", signup),                                            # username & password
            (r"/login/([^/]+)/([^/]+)", login),                                              # username & password
            (r"/logout/([^/]+)/([^/]+)", logout),                                            # username & password
            (r"/sendticket/([^/]+)/([^/]+)/([^/]+)", sendticket),                            # token & subject & body
            (r"/getticketcli/([^/]+)", getticketcli),                                        # token
            (r"/closeticket/([^/]+)/([^/]+)", closeticket),                                  # token & id
            (r"/getticketmod/([^/]+)", getticketmod),                                        # token
            (r"/restoticketmod/([^/]+)/([^/]+)", restoticketmod),                            # token & id
            (r"/changestatus/([^/]+)/([^/]+)/([^/]+)", changestatus),            # token & id & status
            (r"/apicheck/([^/]+)", apicheck),
            
            # Post Method
            (r"/signup", signup),                                     # username & password
            (r"/login", login),                                       # username & password
            (r"/logout", logout),                                     # username & password
            (r"/sendticket", sendticket),                             # token & subject & body
            (r"/getticketcli", getticketcli),                         # token
            (r"/closeticket", closeticket),                           # token & id
            (r"/getticketmod", getticketmod),                         # token
            (r"/restoticketmod", restoticketmod),                     # token & id
            (r"/changestatus", changestatus),             # token & id & status
            (r".*", defaulthandler),                                  # defaultHandler
        ]
        settings = dict()
        super(Application, self).__init__(handlers, **settings)
        self.db = torndb.Connection(
            host=options.mysql_host,
            database=options.mysql_database,
            user=options.mysql_user,
            password=options.mysql_password
        )


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def check_user(self, username):
        resuser = self.db.get("SELECT * from users where username = %s", username)
        if resuser:
            return True
        else:
            return False


class defaulthandler(BaseHandler):
    def get(self):
        output = dict(message="Wrong Command!")
        self.write(output)
        
    def post(self, *args, **kwargs):
        output = dict(message="Wrong Command!")
        self.write(output)


class signup(BaseHandler):
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        firstname = self.get_argument('firstname')
        lastname = self.get_argument('lastname')
        #rule_db = self.db.get("SELECT rule from users where username = %s", username)
        #rule = rule_db['rule']
        if not self.check_user(username):
            api_token = str(hexlify(os.urandom(16)))
            self.db.execute("INSERT INTO users (username, password, token, rule, firstname, lastname) "
                            "values (%s, %s, %s ,%s, %s, %s) "
                            , username, password, api_token, "user", firstname, lastname)
            output = {'message': "Signed Up Successfully",
                      'token': api_token,
                      'rule': "user",
                      'code': "200"}
            self.write(output)
        else:
            output = {'message': "User Exists!"}
            self.write(output)

    def get(self, *args):
        if not self.check_user(args[0]):
            api_token = str(hexlify(os.urandom(16)))
            self.db.execute("INSERT INTO users (username, password, token, rule) "
                                      "values (%s, %s, %s, %s) "
                                      , args[0], args[1], api_token, "user")
            output = {'message': "Signed Up Successfully",
                      'token': api_token,
                      'code': "200"}
            self.write(output)
        else:
            output = {'status': 'User Exist'}
            self.write(output)


class login(BaseHandler):
    def get(self, *args):
        resuser = self.db.get("SELECT * from users where username = %s and password = %s", args[0], args[1])
        if resuser:
            api_token = self.db.get("SELECT token from users where username = %s", args[0])
            rule_db = self.db.get("SELECT rule from users where username = %s", args[0])
            rule = rule_db['rule']
            output = {'message': "Logged in Successfully",
                      'code': "200",
                      'token': api_token,
                      'rule': rule}
            self.write(output)
        else:
            output = {'message': "User doesn't exist!"}
            self.write(output)


class logout(BaseHandler):
    def get(self, *args, **kwargs):
        password_db = self.db.get("SELECT password FROM users WHERE username = %s", args[0])
        password = password_db['password']
        if args[1] == password:
            output = {'message': "Logged out Successfully",
                      'code': "200"}
            self.write(output)
        else:
            output = {'message': "Error!"}
        self.write(output)


class sendticket(BaseHandler):
    def post(self, *args, **kwargs):
        api_token = self.get_argument('token')
        subject = self.get_argument('subject')
        body = self.get_argument('body')
        status = 'in progress'
        username_db = self.db.get("SELECT username from users where token = %s", api_token)
        username = username_db['username']
        self.db.execute("INSERT INTO ticket (username, subject, body, status) "
                                  "values (%s, %s, %s, %s) ",
                                  username, subject, body, status)
        #message_id = self.db.get("SELECT id from ticket where username = %s", username)
        output = {'message': "Ticket Sent Successfully",
                  #'id': message_id,
                  'code': "200"}
        self.write(output)
        
    def get(self, *args, **kwargs):
        api_token = str(args[0])
        subject = args[1]
        body = args[2]
        status = 'in progress'
        username_db = self.db.get("SELECT username FROM users WHERE token = %s", api_token)
        username = username_db['username']
        print(username)
        self.db.execute("INSERT INTO ticket (username, subject, body, status) "
                        "values (%s, %s, %s, %s) ",
                        username, subject, body, status)
        message_id_db = self.db.get("SELECT id from ticket where username = %s", username)
        message_id = message_id_db['id']
        output = {'message': "Ticket Sent Successfully",
                  'id': message_id,
                  'code': "200"}
        self.write(output)
        
        
class getticketcli(BaseHandler):
    def get(self, *args, **kwargs):
        token = args[0]
        username_db = self.db.get("SELECT username from users where token = %s", token)
        username = username_db['username']
        rule_db = self.db.get("SELECT rule from users where username = %s", username)
        rule = rule_db['rule']
        subject_db = self.db.get("SELECT subject from ticket where username = %s", username)
        subject = subject_db['subject']
        body_db = self.db.get("SELECT body from ticket where username = %s", username)
        body = body_db['body']
        status_db = self.db.get("SELECT status from ticket where username = %s", username)
        status = status_db['status']
        output = {'tickets': "There Are -1- Ticket",
                  'code': "200",
                  'block 0': {
                      'subject': subject,
                      'body': body,
                      'status': status,
                      'id': "1",
                      'date': str(datetime.datetime.now())
                  }}
        if rule == "user":
            self.write(output)
        else:
            self.write("Warning!")


class closeticket(BaseHandler):
    def post(self, *args, **kwargs):
        api_token = self.get_argument('token')
        message_id = int(self.get_argument('id'))
        username_db = self.db.get("SELECT username from users where token = %s", api_token)
        username = username_db['username']
        rule_db = self.db.get("SELECT rule from users where username = %s", username)
        rule = rule_db['rule']
        msg = "Ticket with id -" + str(message_id) + "- Closed Successfully"
        output = {'message': msg,
                  'code': "200"}
        if rule == "user":
            self.db.execute("UPDATE ticket SET status = 'close' where username = %s and id = %s", username, message_id)
            self.write(output)
        else:
            output = {'message': "Access Denied"}
            self.write(output)
            
    def get(self, *args, **kwargs):
        api_token = args[0]
        message_id = args[1]
        username_db = self.db.get("SELECT username from users where token = %s", api_token)
        username = username_db['username']
        rule_db = self.db.get("SELECT rule from users where username = %s", username)
        rule = rule_db['rule']
        msg = "Ticket with id -" + str(message_id) + "- Closed Successfully"
        output = {'message': msg,
                  'code': "200"}
        if rule == "user":
            self.db.execute("UPDATE ticket SET status = 'close' where username = %s and id = %s", username, message_id)
            self.write(output)
        else:
            output = {'message': "Access Denied"}
            self.write(output)
            
class getticketmod(BaseHandler):
    def get(self, *args, **kwargs):
        token = args[0]
        username_db = self.db.get("SELECT username from users where token = %s", token)
        username = username_db['username']
        rule_db = self.db.get("SELECT rule from users where username = %s", username)
        rule = rule_db['rule']
        subject_db = self.db.get("SELECT subject from ticket where username = %s", username)
        subject = subject_db['subject']
        body_db = self.db.get("SELECT body from ticket where username = %s", username)
        body = body_db['body']
        status_db = self.db.get("SELECT status from ticket where username = %s", username)
        status = status_db['status']
        output = {'tickets': "There Are -1- Ticket",
                  'code': "200",
                  'block 0': {
                      'subject': subject,
                      'body': body,
                      'status': status,
                      'id': "1",
                      'date': str(datetime.datetime.now())
                  }}
        if rule == "manager":
            self.write(output)
        else:
            self.write("Warning!")


class restoticketmod(BaseHandler):
    def post(self, *args, **kwargs):
        api_token = self.get_argument('token')
        ticket_id = self.get_argument('id')
        message_body = self.get_argument('body')
        rule = self.db.get("SELECT rule from users where token = %s", api_token)
        #rule = rule_db['rule']
        username = self.db.get("SELECT username from ticket where id = %s", ticket_id)
        #username = username_db['username']
        if rule == "manager":
            self.db.execute("INSERT INTO chats (username, body) values (%s %s) ", username, message_body)
            output = {'message': "Response to Ticket With id -1- Sent Successfully",
                      'code': "200"}
            self.write(output)
        else:
            output = {'message': "Access Denied!"}
            self.write(output)


class changestatus(BaseHandler):
    def post(self, *args, **kwargs):
        api_token = self.get_argument('token')
        ticket_id = self.get_argument('id')
        ticket_status = self.get_argument('status')
        rule_db = self.db.get("SELECT rule from users where token = %s", api_token)
        rule = rule_db['rule']
        output = {'message': "Status Ticket With id -1- Changed Successfully",
                  'code': "200"}
        if rule == "manager":
            self.db.execute("UPDATE ticket SET status = %s where id = %s", ticket_status, ticket_id)
            self.write(output)
        else:
            output = {'message': "Access Denied!"}
            self.write(output)

class apicheck(BaseHandler):
    def get(self, *args, **kwargs):
        exists = self.db.get("SELECT * from users where token = %s", args[0])
        if exists:
            username = self.db.get("SELECT username from users where token = %s", args[0])
            password = self.db.get("SELECT password from users where token = %s", args[0])
            rule_db = self.db.get("SELECT rule from users where token = %s", args[0])
            rule = rule_db['rule']
            token = args[0]
            output = {'message': 'Signed Up Successfully',
                      'token': token,
                      'rule': rule,
                      'username': username,
                      'password': password,
                      'code': "200"}
            self.write(output)
        else:
            output = {'message': 'Unsuccessful'}
            self.write(output)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
