from sqlalchemy import or_
from sqlalchemy.orm import Session
from make_database import Base, Page
from sqlalchemy import create_engine


def main():
    engine = create_engine("sqlite:///search-engine.db")
    Base.metadata.create_all(engine)
    session = Session(bind=engine)

    search_word = "spam"
    result = session.query(Page.url).filter(or_(Page.title.contains(search_word), Page.description.contains(search_word))).all()
    print(result)

if __name__ == '__main__':
    main()
