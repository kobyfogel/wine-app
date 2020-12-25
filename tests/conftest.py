import os
import tempfile

import pytest

from wine import db, routes
from wine import app


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        # with app.app_context():
        #     app.init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


@pytest.fixture
def user():
    admin = routes.register('admin', 'admin', 'admin')
    db.session.add(admin)
    db.session.commit()
    yield admin
    db.session.delete(admin)
    db.session.commit()
