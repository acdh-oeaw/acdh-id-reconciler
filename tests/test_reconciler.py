import unittest
from acdh_id_reconciler import gnd_to_geonames, gnd_to_wikidata, geonames_to_gnd, geonames_to_wikidata

DATA = [
    (
        "http://d-nb.info/gnd/4074255-6/",
        {
            'wikidata': 'http://www.wikidata.org/entity/Q41329',
            'gnd': '4074255-6',
            'geonames': '2772400'
        }
    ),
    (
        "https://d-nb.info/gnd/4010858-2",
        {
            'wikidata': 'http://www.wikidata.org/entity/Q261664',
            'gnd': '4010858-2',
            'geonames': '2781124'
        }
    )
]

DATA_GND_TO_WIKIDATA = [
    (
        "http://d-nb.info/gnd/4074255-6/",
        {
            'wikidata': 'http://www.wikidata.org/entity/Q41329',
            'gnd': '4074255-6',
        }
    ),
    (
        "https://d-nb.info/gnd/4010858-2",
        {
            'wikidata': 'http://www.wikidata.org/entity/Q261664',
            'gnd': '4010858-2',
        }
    )
]

DATA_GEONAMES_WIKI = [
    (
        "https://www.geonames.org/2761369",
        {
            'wikidata': 'http://www.wikidata.org/entity/Q1741',
            'geonames': '2761369',
        }
    ),
    (
        "https://www.geonames.org/2633352",
        {
            'wikidata': 'http://www.wikidata.org/entity/Q42462',
            'geonames': '2633352',
        }
    )
]

DATA_GEONAMES_GND = [
    (
        "https://www.geonames.org/2761369",
        {
            'wikidata': 'http://www.wikidata.org/entity/Q1741',
            'geonames': '2761369',
            'gnd': '4066009-6'
        }
    ),
    (
        "https://www.geonames.org/2633352",
        {
            'wikidata': 'http://www.wikidata.org/entity/Q42462',
            'geonames': '2633352',
            'gnd': '4067205-0'
        }
    )
]


class TestTestTest(unittest.TestCase):
    """Tests for `acdh_id_reconciler` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_gnd_to_geonames(self):
        for x in DATA:
            result = gnd_to_geonames(x[0])
            self.assertEqual(result, x[1])

    def test_002_gnd_to_wikidata(self):
        for x in DATA_GND_TO_WIKIDATA:
            result = gnd_to_wikidata(x[0])
            self.assertEqual(result, x[1])

    def test_003_geonames_to_wikidata(self):
        for x in DATA_GEONAMES_WIKI:
            result = geonames_to_wikidata(x[0])
            self.assertEqual(result, x[1])

    def test_004_geonames_to_gnd(self):
        for x in DATA_GEONAMES_GND:
            result = geonames_to_gnd(x[0])
            self.assertEqual(result, x[1])
