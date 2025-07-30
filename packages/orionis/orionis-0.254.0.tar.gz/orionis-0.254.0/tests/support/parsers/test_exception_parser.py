from orionis.luminate.support.parsers.exception_parser import ExceptionParser
from orionis.luminate.test import TestCase
from tests.support.parsers.fakes.fake_custom_error import CustomError

class TestsExceptionParser(TestCase):

    async def testBasicExceptionStructure(self):
        """
        Ensure that the ExceptionParser correctly structures a basic exception.
        """
        try:
            raise ValueError("Something went wrong")
        except Exception as e:
            result = ExceptionParser(e).toDict()

            self.assertIsInstance(result, dict)
            self.assertIn("error_type", result)
            self.assertIn("error_message", result)
            self.assertIn("stack_trace", result)
            self.assertIn("error_code", result)
            self.assertIn("cause", result)

            self.assertEqual(result["error_type"], "ValueError")
            self.assertTrue("Something went wrong" in result["error_message"])
            self.assertIsNone(result["error_code"])
            self.assertIsNone(result["cause"])
            self.assertIsInstance(result["stack_trace"], list)
            self.assertGreater(len(result["stack_trace"]), 0)

    async def testRawExceptionProperty(self):
        """
        Ensure that the raw_exception property returns the original exception.
        """
        try:
            raise RuntimeError("Test exception")
        except Exception as e:
            parser = ExceptionParser(e)
            self.assertIs(parser.raw_exception, e)

    async def testExceptionWithCode(self):
        try:
            raise CustomError("Custom message", code=404)
        except Exception as e:
            result = ExceptionParser(e).toDict()
            self.assertEqual(result["error_code"], 404)
            self.assertEqual(result["error_type"], "CustomError")

    async def testNestedExceptionCause(self):
        """
        Ensure that the ExceptionParser correctly handles nested exceptions.
        """
        try:
            try:
                raise ValueError("Original cause")
            except ValueError as exc:
                raise TypeError("Outer error")
        except Exception as e:
            result = ExceptionParser(e).toDict()
            self.assertEqual(result["error_type"], "TypeError")