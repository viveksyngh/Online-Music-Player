import unittest
from app import app


class FlaskTestCase(unittest.TestCase):

    # Ensure that Flask was set up correctly
    def test_index(self):
    	tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that login page loads correctly   
    def test_login(self):
    	tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(b'Please login' in response.data)

    # Ensure that for correct login
    def test_correct_login(self):
    	tester = app.test_client(self)
        response = tester.post('/login', 
        	data=dict(username="admin", password="admin") ,
        	follow_redirects=True
        	)
        self.assertIn('You have just logged in', response.data)

    #Ensure that login page behaves correctly when given an incorrect credentials
    def test_incorrect_login(self):
    	tester = app.test_client(self)
        response = tester.post('/login', 
        	data=dict(username="wrong", password="wrong") ,
        	follow_redirects=True
        	)
        self.assertIn('Invalid Credentaials. Please try again.', response.data)

    #Ensure Logout Behaves Correctly
    def test_logout(self):
    	tester = app.test_client(self)
        tester.post('/login', 
        	data=dict(username="admin", password="admin") ,
        	follow_redirects=True
        	)
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn('You have logged out', response.data)


    #Ensure home pages requires login works correctly
    def test_main_require_login(self) :
    	tester = app.test_client(self)
        response = tester.get('/', follow_redirects=True)
        self.assertIn('You need to login first', response.data)

    def test_post_login(self):
    	tester = app.test_client(self)
        response = tester.post('/login', 
        	data=dict(username="admin", password="admin") ,
        	follow_redirects=True
        	)
        self.assertIn('Hello from the Shell', response.data)



if __name__ == '__main__' :
	unittest.main()