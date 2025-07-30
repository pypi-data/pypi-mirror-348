import unittest

from evdutyapi.api_response.station_response import StationResponse


class StationResponseTest(unittest.TestCase):
    def test_parses_json(self):
        json = StationResponse(id="1", name="A", terminals=[]).to_json()

        station = StationResponse.from_json(json)

        self.assertEqual(station.id, "1")
        self.assertEqual(station.name, "A")
        self.assertEqual(station.terminals, [])

    def test_set_empty_terminals_on_default(self):
        json = StationResponse(id="1", name="A").to_json()

        station = StationResponse.from_json(json)

        self.assertEqual(station.terminals, [])
