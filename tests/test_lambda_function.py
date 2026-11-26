import json
import unittest
from lambda_function import lambda_handler


def make_event(method, path, body=None):
    event = {
        "version": "2.0",
        "rawPath": path,
        "requestContext": {"http": {"method": method}},
    }
    if body is not None:
        event["body"] = json.dumps(body) if not isinstance(body, str) else body
    return event


class CloudAPITests(unittest.TestCase):
    def call(self, method, path, body=None):
        result = lambda_handler(make_event(method, path, body), None)
        return result["statusCode"], json.loads(result["body"])

    def test_root(self):
        code, body = self.call("GET", "/")
        self.assertEqual(code, 200)
        self.assertEqual(body["service"], "CloudAPI")

    def test_hello(self):
        code, body = self.call("GET", "/hello")
        self.assertEqual(code, 200)
        self.assertIn("Hello", body["message"])

    def test_status(self):
        code, body = self.call("GET", "/status")
        self.assertEqual(code, 200)
        self.assertEqual(body["health"], "healthy")

    def test_greet(self):
        code, body = self.call("POST", "/greet", {"name": "Debmalya"})
        self.assertEqual(code, 200)
        self.assertEqual(body["message"], "Hello, Debmalya!")

    def test_greet_missing_name(self):
        code, body = self.call("POST", "/greet", {})
        self.assertEqual(code, 400)
        self.assertEqual(body["status"], "error")

    def test_invalid_json(self):
        code, body = self.call("POST", "/greet", "{not-json")
        self.assertEqual(code, 400)

    def test_unknown_route(self):
        code, body = self.call("GET", "/missing")
        self.assertEqual(code, 404)


if __name__ == "__main__":
    unittest.main(verbosity=2)
