import unittest

import me


class MifiExporterTests(unittest.TestCase):
    def setUp(self) -> None:
        assert me.IPAddress  # COOPER
        return super().setUp()

    def test_temp(self) -> None:
        pass


if __name__ == "__main__":
    unittest.main()
