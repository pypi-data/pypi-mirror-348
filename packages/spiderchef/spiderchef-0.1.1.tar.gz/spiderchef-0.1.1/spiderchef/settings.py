import re

from environs import Env

HELP = """SpiderChef is a powerful, recipe-based web scraping tool that makes data extraction systematic and reproducible."""

env = Env()

BASE_RECIPE = {
    "base_url": "https://example.com",
    "name": "Example",
    "steps": [{"type": "fetch", "path": "/hello"}],
}


RE_WHITESPACE_CHARS = re.compile(r"\s\s+")
RE_HTML_TAGS = re.compile(r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
RE_CURRENCY_CHARS = re.compile(r"[$€£¥₹¢¤]|\b(?:USD|EUR|GBP|JPY|INR)\b")
RE_VAR = re.compile(r"\${([^}]*?)}")
RE_ENV_VAR = re.compile(r"\${env\.([A-Za-z_][A-Za-z0-9_]*)}")
