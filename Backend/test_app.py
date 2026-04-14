import unittest

# Example: agar tumhara database connection file ka naam database.py hai
# toh yaha import karo (adjust according to your project)
# from database import connect_db

class TestApp(unittest.TestCase):

    def test_sample(self):
        """Simple test to check working"""
        self.assertEqual(1, 1)

    def test_database_connection(self):
        """Test database connection (dummy example)"""
        try:
            # yaha actual DB function call kar sakte ho
            # db = connect_db()
            # self.assertIsNotNone(db)

            # filhaal dummy check
            connected = True
            self.assertTrue(connected)

        except Exception as e:
            self.fail(f"Database connection failed: {e}")

    def test_validation(self):
        """Test simple validation logic"""
        data = "Adarsh"
        self.assertTrue(len(data) > 0)


if __name__ == "__main__":
    unittest.main()
