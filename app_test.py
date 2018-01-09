import os
import app
import unittest
import tempfile
import StringIO
from PIL import Image
from werkzeug.utils import secure_filename

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.testing = True
        self.app = app.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def test_photo_response(self):
        response = self.app.post('/',
            data=dict(
                {'file': (open('test.jpg'), 'test.jpg')}
            ), content_type='multipart/form-data', follow_redirects=True
        )
        test_image = Image.open('test.jpg')
        imgString = StringIO.StringIO()
        test_image.save(imgString, format='jpeg')
        assert imgString.getvalue() in response.data

if __name__ == '__main__':
    unittest.main()































