import unittest
from translit_me.lang_tables import table_lookup
from translit_me.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


class TestMainInterface(unittest.TestCase):
    def test_main_interface(self):
        for source, target in table_lookup.keys():
            if isinstance(source, str) and isinstance(target, str):
                with self.subTest(source_lang=source, target_lang=target):
                    response = client.post("/", json={"source_lang": source, "target_lang": target, "word": "test"})
                    self.assertEqual(response.status_code, 200, f"Failed for {source} -> {target}")
                    result = response.json()
                    self.assertIn("transliterated_word", result,
                                  f"No transliterated word returned for {source} -> {target}")
                    self.assertTrue(result["transliterated_word"],
                                    f"Empty transliterated word for {source} -> {target}")


if __name__ == "__main__":
    unittest.main()
