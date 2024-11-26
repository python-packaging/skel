import unittest

import regen


class RegenTest(unittest.TestCase):
    def test_variable_format(self) -> None:
        self.assertEqual("1", regen.variable_format("{foo}", foo="1"))
        self.assertEqual("{foo}", regen.variable_format("{foo}"))
        self.assertEqual("{ foo }", regen.variable_format("{ foo }", foo="1"))
        self.assertEqual("{{foo}}", regen.variable_format("{{foo}}", foo="1"))
        with self.assertRaises(TypeError):
            self.assertEqual("1", regen.variable_format("{foo}", foo=1, bar=2))  # type: ignore [arg-type]


if __name__ == "__main__":
    unittest.main()
