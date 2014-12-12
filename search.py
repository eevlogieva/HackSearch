from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

from sqlalchemy import or_
from sqlalchemy.orm import Session
from make_database import Base, Page
from sqlalchemy import create_engine


@app.route("/")
def load_page():
    return render_template("index.html")


@app.route("/search/")
def search():
    engine = create_engine("sqlite:///search-engine.db")
    Base.metadata.create_all(engine)
    session = Session(bind=engine)
    search_word = request.args.get('search_phrase', '')
    result = session.query(Page).filter(or_(Page.title.contains(search_word), Page.description.contains(search_word))).all()
    return render_template('template.html', result=result)


if __name__ == "__main__":
    app.run()
