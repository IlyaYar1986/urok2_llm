import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "web" / "personalizaciya_tyutorstvo.html"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.id_counts = {}
        self.details = 0

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            value = values["id"]
            self.ids.add(value)
            self.id_counts[value] = self.id_counts.get(value, 0) + 1
        if tag == "details":
            self.details += 1


class PersonalizaciyaTyutorstvoPageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8") if PAGE.exists() else ""
        cls.parser = PageParser()
        cls.parser.feed(cls.html)

    def test_page_exists_with_required_sections(self):
        self.assertTrue(PAGE.is_file())
        required = {"hero", "problema", "personalizaciya", "pochemu-seychas"}
        self.assertTrue(required.issubset(self.parser.ids))
        duplicates = [
            element_id
            for element_id, count in self.parser.id_counts.items()
            if count > 1
        ]
        self.assertEqual(duplicates, [], f"Duplicate ids: {duplicates}")

    def test_no_link_to_index(self):
        self.assertNotIn('href="../index.html"', self.html)
        self.assertNotIn("href=\"index.html\"", self.html)

    def test_problema_section_has_distribution_stats(self):
        for marker in ("30%", "40%", "слишком просто", "слишком сложно", "оптимальная"):
            self.assertIn(marker, self.html)

    def test_personalizaciya_section_has_five_principles(self):
        for marker in (
            "Содержание под его уровень",
            "Удобный темп",
            "Подходящий формат подачи",
            "Обратную связь в нужный момент",
            "Поддержку именно там",
        ):
            self.assertIn(marker, self.html)
        self.assertGreaterEqual(self.parser.details, 5)

    def test_bloom_section_has_corrected_effect_sizes(self):
        for marker in ("Bloom", "1984", "98%", "VanLehn", "Nickow", "Kraft"):
            self.assertIn(marker, self.html)
        self.assertNotIn("0,3–0,8 стандартных отклонений", self.html)


if __name__ == "__main__":
    unittest.main()
