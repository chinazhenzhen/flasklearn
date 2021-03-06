from flask import Flask,make_response,render_template,session,redirect,url_for,flash,app

from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..mymail import send_email

@main.route('/',method=['GET','POST'])
def index():
    form=NameForm()
    if form.validate_on_submit():#如果表单接收到数据则返回true
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            #db.session.commit()
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'],'New User','mail/new_user',user=user)
        else:
            session['known'] = True
        session['name']=form.name.data
        form.name.data=''
        return redirect(url_for('.index'))
            #flash('Look like you have changed your name!')

    return render_template("index.html",form=form,name=session.get('name'),known=session.get('known',False))
