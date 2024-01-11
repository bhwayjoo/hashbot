from flask import Flask, request, redirect , render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask("__name__")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hsschs.db"
db = SQLAlchemy(app)
vide='6852521025:AAGy-21aK_AQfF2zOcmuXNsqB71X4VdPbQg'
message="hi"

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(250), nullable=False)
    username=db.Column(db.String(250), nullable=False)
    chat_id=db.Column(db.String(500), nullable=False ,unique=True)

    Number=db.Column(db.String(200), nullable=False, default='0')
    sub_statues=db.Column(db.String(250), nullable=False, default='trial')


    hassh = db.Column(db.String(250), nullable=False, default=vide)
    targetHash = db.Column(db.String(250), nullable=False, default=vide)
    brutetype= db.Column(db.String(250), nullable=False, default=vide)
    characters= db.Column(db.String(250), nullable=False, default=vide)
    min_num= db.Column(db.String(250), nullable=False, default=vide)
    max_num= db.Column(db.String(250), nullable=False, default=vide)
    filedir= db.Column(db.String(250), nullable=False, default=vide)
    complete= db.Column(db.String(250), nullable=False, default='no')


    def __repr__(self):
        return(f"User('{self.fname}', '{self.username}', '{self.chat_id}', '{self.sub_statues} ,'{self.Number}', '{self.sub_statues}', '{self.hassh}', '{self.targetHash}' , '{self.brutetype}' , '{self.characters}' , '{self.min_num}', '{self.max_num}', '{self.min_num}', '{self.complete}', '{self.filedir}'  )")
@app.route("/")
def home():
    text = request.args.get("text")
    return f"Flask received the following text:{text}"


@app.route("/sum")
def sum():
    message = ""  # Initialize the message variable

    output = request.args.get("output")
    username = request.args.get("username")
    first_name = request.args.get("first_name")
    chat_id = request.args.get("chat_id")

    user = User.query.filter_by(chat_id=chat_id).first()

    def finish():
        user.hassh = vide
        user.complete = vide
        user.targetHash = vide
        user.brutetype = vide
        user.characters = vide
        user.min_num = vide
        user.max_num = vide
        user.filedir=vide
        user.status = "no"

        db.session.commit()

    if user:
        if user.sub_statues == "trial" and int(user.Number) >= 3:
            status = "failed"
            # No need to redeclare message here
            result = {
                "chat_id": chat_id,
                "original_link": output,
                "message": message,
                "status": status,
            }
            return result
        else:
            status = "success"
            # Rest of your code

            if user.hassh == vide and user.targetHash==vide and user.brutetype==vide and user.characters==vide and user.min_num==vide and user.max_num==vide and user.complete=='no':
                if int(output)==1 or int(output)==2 or int(output)==3:
                    user = User.query.filter_by(chat_id=chat_id).first_or_404()
                    user.hassh = int(output)
                    db.session.commit()
                    message = 'type Your target hash'
                else :
                    message= 'Type your hash type\n1: md5\n2: sha256\n3: wpa\n'

            elif user.targetHash==vide and user.brutetype==vide and user.characters==vide and user.min_num==vide and user.max_num==vide and user.complete=='no':

                def send():
                    user = User.query.filter_by(chat_id=chat_id).first_or_404()
                    user.targetHash = output
                    db.session.commit()
                    return 'Type your brute force type\n1: create a word list\n2: update a word list\n3: use default wordlist (rockyou)'

                if int(user.hassh)==1 and len(output)==32:
                    message=send()
                elif int(user.hassh)==2 and len(output)==64:
                    message=send()
                elif int(user.hassh)==3 and output.split('*')[0]=="WPA":
                    message=send()
                else:
                    if int(user.hassh)==1:
                        message = 'your hash is not md5 hash please enter a md5 hash'
                    elif int(user.hassh)==2:
                        message = 'your hash is not sha256 hash please enter a sha256 hash'
                    elif int(user.hassh)==3:
                        message = 'your hash is not hc22000 hash please enter a hc22000 hash'

            elif user.brutetype==vide and user.characters==vide and user.min_num==vide and user.max_num==vide and user.complete=='no' :


                user = User.query.filter_by(chat_id=chat_id).first_or_404()
                user.brutetype = output
                db.session.commit()
                if user.brutetype=='1':
                    message = 'Type your characters:'
                elif user.brutetype=='2' and user.filedir == vide:
                    message=('accee1')
                    user.filedir='hi'
                    db.session.commit()
                    print('accescddd')
                    db.session.commit()
                    targetHash = user.targetHash
                    brutetype = user.brutetype
                    characters = user.characters
                    min_num = user.min_num
                    max_num = user.max_num
                    message = 'send your file '
                    result = {
                        "chat_id": chat_id,
                        "original_link": output,
                        "message": message,
                        "status": status,
                        "brutetype": brutetype,

                    }
                    return result
                elif user.brutetype=='2':
                    message=('accee2')
                    user.complete = 'file'
                    print('accescddd')
                    hassh = user.hassh
                    user.filedir = output
                    db.session.commit()
                    filedir = user.filedir
                    user.complete = 'file'
                    complete = user.complete
                    hassh = user.hassh
                    targetHash = user.targetHash
                    brutetype = user.brutetype
                    characters = user.characters
                    min_num = user.min_num
                    max_num = user.max_num
                    message = 'password is '
                    result = {
                        "chat_id": chat_id,
                        "original_link": output,
                        "message": message,
                        "hassh": hassh,
                        "complete": 'file',
                        "targetHash": targetHash,
                        "brutetype": '2',
                        "characters": characters,
                        "min_num": min_num,
                        "max_num": max_num,
                        "filedir": filedir,
                        "status": status,
                    }
                    finish()
                    return result







                elif user.brutetype=='3':
                    user.complete='rok'
                    complete = user.complete
                    hassh = user.hassh
                    targetHash = user.targetHash
                    brutetype = user.brutetype
                    characters = user.characters
                    min_num = user.min_num
                    max_num = user.max_num
                    message = 'your passwowrd is '


                    result = {

                        "chat_id": chat_id,
                        "original_link": output,
                        "message": message,
                        "hassh": hassh,
                        "complete": complete,
                        "targetHash": targetHash,
                        "brutetype": brutetype,
                        "characters": characters,
                        "min_num": min_num,
                        "max_num": max_num,
                        "status": status,
                    }
                    finish()

                    return result



            elif user.characters==vide and user.min_num==vide and user.max_num==vide and user.complete=='no':

                user = User.query.filter_by(chat_id=chat_id).first_or_404()
                user.characters = output
                db.session.commit()
                message = 'Type your min numbers:'

            elif user.min_num == vide and user.max_num == vide and user.complete == 'no':
                try :
                    if (type(int(output)) == int):
                        user = User.query.filter_by(chat_id=chat_id).first_or_404()
                        user.min_num = output
                        db.session.commit()
                        message = 'Type your max numbers:'
                except:
                    message = 'Type your min numbers:'



            elif user.max_num == vide and user.complete == 'no':
                try :
                    if (type(int(output)) == int):
                        user = User.query.filter_by(chat_id=chat_id).first_or_404()
                        user.max_num = output
                        user.complete = 'yes'
                        db.session.commit()

                except:
                    message = 'Type your max numbers:'


            

                user = User.query.filter_by(chat_id=chat_id).first_or_404()
                user.max_num = output
                user.complete='yes'
                db.session.commit()

                complete =user.complete
                hassh=user.hassh
                targetHash = user.targetHash
                brutetype = user.brutetype
                characters = user.characters
                min_num = user.min_num
                max_num = user.max_num
                message ='your passwowrd is '

                result = {

                    "chat_id": chat_id,
                    "original_link": output,
                    "message": message,
                    "hassh":hassh,
                    "complete" :complete,
                    "targetHash":targetHash,
                    "brutetype":brutetype,
                    "characters":characters,
                    "min_num":min_num,
                    "max_num":max_num,
                    "status": status,
                }
                finish()

                return result


            else:
                user.hassh = vide
                user.complete = "no"
                user.targetHash = vide
                user.brutetype = vide
                user.characters = vide
                user.min_num = vide
                user.max_num = vide
                user.status = "no"
                db.session.commit()
                message = 'Type your hash type\n1: md5\n2: sha256\n3: wpa'
                result = {

                    "chat_id": chat_id,
                    "original_link": output,
                    "message": message,
                    "status": status,

                }

                return result

            result = {
                "chat_id": chat_id,
                "original_link": output,
                "message": message,
                "status": status,
            }
            return result

    else:

        user = User(fname=first_name, username=username, chat_id=chat_id)
        db.session.add(user)
        db.session.commit()
        status = "success"

        result = {
            "chat_id": chat_id,
            "original_link": output,
            "message": 'type /start for start your crack',
            "status": status,
        }
        return result
@app.route("/start")
def start():
    message = 'Type your hash type\n1: md5\n2: sha256\n3: wpa'


    output = request.args.get("output")
    username = request.args.get("username")
    first_name = request.args.get("first_name")
    chat_id = request.args.get("chat_id")

    user = User.query.filter_by(chat_id=chat_id).first()

    if user:
        user.hassh = vide
        user.complete = "no"
        user.targetHash = vide
        user.brutetype = vide
        user.characters = vide
        user.min_num = vide
        user.max_num = vide
        user.status = "no"
        db.session.commit()

        status=""
        result = {

            "chat_id": chat_id,
            "original_link": output,
            "message": message,
            "status": status,

        }

        return result

    else :
        user = User(fname=first_name, username=username, chat_id=chat_id)
        db.session.add(user)
        db.session.commit()
        status = "success"

        result = {
            "chat_id": chat_id,
            "original_link": output,
            "message": 'message',
            "status": status,
        }
        return result
@app.route("/display_users")
def display_users():
    users = User.query.all()
    return render_template("display_users.html", users=users)


@app.route("/file")
def file():
    message = ""
    output = request.args.get("output")
    username = request.args.get("username")
    first_name = request.args.get("first_name")
    chat_id = request.args.get("chat_id")

    user = User.query.filter_by(chat_id=chat_id).first()
    if user:
        if user.brutetype == '2':
            user.filedir = output
            db.session.commit()

            user.complete = 'file'
            db.session.commit()

            status = 'acces'
            hassh = user.hassh
            filedir = user.filedir
            user.complete = 'file'
            complete = user.complete
            hassh = user.hassh
            targetHash = user.targetHash
            brutetype = user.brutetype
            message = 'password is '
            result = {
                "chat_id": chat_id,
                "message": message,
                "hassh": hassh,
                "complete": complete,
                "targetHash": targetHash,
                "brutetype": brutetype,
                "filedir": filedir,
                "status": status,
            }
            user.hassh = vide
            user.complete = vide
            user.targetHash = vide
            user.brutetype = vide
            user.characters = vide
            user.min_num = vide
            user.max_num = vide
            user.filedir = vide
            user.status = "no"

            db.session.commit()
            return result

    # If user is not found or brutetype is not '2'
    return {"error": "User not found or invalid brutetype"}
        
   

if __name__ == "__main__":

    app.run(debug=True)