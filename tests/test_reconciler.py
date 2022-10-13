import unittest
from acdh_id_reconciler import gnd_to_geonames

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
