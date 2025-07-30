import unittest

import pandas as pd
from electricity_network_file_parser.GnfParser import GnfParser

class Test(unittest.TestCase):

    def setUp(self):
        self.gnf_parser = GnfParser("test.gnf")

    def test_gnf_parser(self):
        self.gnf_parser.parse_file()

    def test_parse_property_line_function(self):
        property_line = "#General StringValue:'Test string 1' NumberValue:1 BooleanValue:True FloatValue:2,53"
        expected_output = {
            "StringValue": "Test string 1",
            "NumberValue": 1,
            "BooleanValue": True,
            "FloatValue": 2.53
        }
        result = self.gnf_parser.parse_property_line(property_line)
        self.assertEqual(result.property_attributes, expected_output)
        self.assertEqual(result.property_type, "General")

    def test_parse_entities_function(self):
        # Arrange
        lines = [
            "#General StringValue:'Test string 1' NumberValue:1 BooleanValue:True FloatValue:2,53",
            "#Attributes StringValue2:'Test string 2' NumberValue2:2 BooleanValue2:False FloatValue2:3,53",
            "#General StringValue:'Test string 3' NumberValue:3 BooleanValue:False FloatValue:3,14",
            "#Attributes StringValue2:'Test string 4' NumberValue2:4 BooleanValue2:False FloatValue2:4,53"
        ]

        # Execute
        result_df = self.gnf_parser.parse_entities(lines, ["General", "Attributes"])

        # Assert
        expected_output_dict = {
            "StringValue": ["Test string 1", "Test string 3"],
            "NumberValue": [1, 3],
            "BooleanValue": [True, False],
            "FloatValue": [2.53, 3.14],
            "StringValue2": ["Test string 2", "Test string 4"],	
            "NumberValue2": [2, 4],
            "BooleanValue2": [False, False],
            "FloatValue2": [3.53, 4.53]
        }
        expected_output_df = pd.DataFrame(expected_output_dict)
        self.assertTrue(expected_output_df.equals(result_df))

    def test_parse_cable_types(self):
        # Arrange
        cables_df = self.gnf_parser.parse_entities(self.gnf_parser.entity_dict["CABLE"], ["General", "CablePart", "CableType"])

        # Execute
        cabletype_df = self.gnf_parser.parse_cable_types(cables_df)

        # Assert
        expected_number_of_rows = 1
        expected_long_names = "4x95Al+4x6Cu+35CuAs(V-VMvKhsas),4x95Al+4x6Cu+35CuAs(V-VMvKhsas)-test"
        self.assertEqual(cabletype_df.shape[0], expected_number_of_rows)
        self.assertEqual(cabletype_df["Longnames"].iloc[0], expected_long_names)

if __name__ == '__main__':
    unittest.main()