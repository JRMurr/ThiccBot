import pytest
from src import create_app, db as _db
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from src.config import TestConfig


# DB modifed taken from
# https://github.com/pytest-dev/pytest-flask/issues/70#issuecomment-361005780
@pytest.fixture(scope="session")
def app():
    """
    Returns session-wide application.
    """
    app = create_app(TestConfig)
    return app


@pytest.fixture(scope="function")
def db(app, request):
    """
    Returns function initialized database so db is cleared after each test.
    """
    with app.app_context():
        _db.drop_all()
        _db.create_all()


@pytest.fixture(scope="function", autouse=True)
def session(app, db, request):
    """
    Returns function-scoped session.
    """
    with app.app_context():
        conn = _db.engine.connect()
        txn = conn.begin()

        options = dict(bind=conn, binds={})
        sess = _db.create_scoped_session(options=options)

        # establish  a SAVEPOINT just before beginning the test
        # (http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#using-savepoint)
        sess.begin_nested()

        @event.listens_for(sess(), "after_transaction_end")
        def restart_savepoint(sess2, trans):
            # Detecting whether this is the nested transaction of the test
            if trans.nested and not trans._parent.nested:
                # The test should have normally called session.commit(),
                # but to be safe we explicitly expire the session
                sess2.expire_all()
                sess.begin_nested()

        _db.session = sess
        yield sess
        # Cleanup
        sess.remove()
        # This instruction rollsback any commit that were executed in the tests.
        txn.rollback()
        conn.close()
