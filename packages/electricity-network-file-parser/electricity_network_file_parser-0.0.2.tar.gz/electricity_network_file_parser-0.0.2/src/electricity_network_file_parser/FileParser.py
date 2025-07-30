from typing import List
import pandas as pd

from pathlib import Path

from electricity_network_file_parser.dataclasses import PropertyDescription

class FileParser:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.data_frames :dict[str, pd.DataFrame] = {} 

        with open(self.file_path, mode='r') as file:
            lines = file.readlines()

        self.entity_dict = self.create_entity_dict(lines)
        self.parse_entities_dict = { }

    def is_integer(self, s : str):
        to_check = s

        if to_check.startswith('-') or to_check.startswith('+'):
            to_check = to_check[1:]

        return to_check.isdigit()

    def parse_value(self, value):
        if value == 'True':
            return True
        elif value == 'False':
            return False
        elif self.is_integer(value):
            return int(value)
        elif value.startswith("'") and value.endswith("'"):
            return value[1:-1]
        else:
            return float(value.replace(",", "."))
        
    def extend_dictionary(self, dict_to_extend : dict, dict_extension : dict):
        for key, value in dict_extension.items():
            dict_to_extend[key] = value

    def parse_property_line(self, property_line : str):
        property_name = property_line[1: property_line.index(" ")]
        property_attributes = property_line[property_line.index(" "):]
        col_name = ''
        value = ''
        reading_value = False
        reading_string = False
        property_dict = {}
        for char in property_attributes:
            if char == ':' and not reading_value:
                reading_value = True
            elif not reading_value:
                col_name += char
            elif char == ' ' and not reading_string and value != '':
                property_dict[col_name.strip()] = self.parse_value(value)
                reading_value = False
                value = ''
                col_name = ''
            elif reading_value:
                if char == "'" and not reading_string:
                    reading_string = True
                elif char == "'" and reading_string:
                    reading_string = False
                value += char

        property_dict[col_name.strip()] = self.parse_value(value)
        return PropertyDescription(property_name, property_dict)

    def parse_entities(self, lines : List[str], property_attributes_to_parse : List[str]):
        parsed_property_types = []
        data_instance = {}
        data_instances = []
        for line in lines:
            line_stripped = line.strip()
            property_name = ""
            if " " in line_stripped:
                property_name = line_stripped[1: line_stripped.index(" ")]
            started_new_entity = property_name in parsed_property_types and property_name == "General"
            all_property_types_parsed = len(parsed_property_types) == len(property_attributes_to_parse)
            if started_new_entity or all_property_types_parsed:
                if not all_property_types_parsed:
                    print(f"Not all property types are present for entity {line_stripped}")
                data_instances.append(data_instance)
                data_instance = {}
                parsed_property_types = []
            if property_name in property_attributes_to_parse:
                general_properties = self.parse_property_line(line_stripped)
                self.extend_dictionary(data_instance, general_properties.property_attributes)
                parsed_property_types.append(general_properties.property_type)

        if len(data_instance.items()) > 0:
            data_instances.append(data_instance)

        return pd.DataFrame(data_instances)

    def create_entity_dict(self, lines):
        entity_indices = [i for i, line in enumerate(lines) if line.strip().startswith("[") and line.strip().endswith("]")]
        entity_start_indices = [val for i, val in enumerate(entity_indices) if i % 2 == 0]
        entity_end_indices = [val for i,val in enumerate(entity_indices) if i % 2 != 0]

        entity_dict = {}

        for i in range(0, len(entity_start_indices)):
            entity_name = lines[entity_start_indices[i]].strip()[1:-1]
            entity_dict[entity_name] = lines[entity_start_indices[i] + 1:entity_end_indices[i]]
        return entity_dict
    
    def group_data_frame_by_columns(self, df : pd.DataFrame, columns_to_group_by : List[str]) -> pd.DataFrame:
        for col in columns_to_group_by:
            df[col] = df.apply(lambda x, col=col: -1 if pd.isnull(x[col]) or pd.isna(x[col]) else x[col], axis=1)
        result = df.groupby(columns_to_group_by).size().reset_index().rename(columns={0:'count'})
        return result
    
    def get_records_containing_field_values(self, df : pd.DataFrame, fields : dict) -> pd.DataFrame:
        query = " and ".join([f"{key} == {value}" for key, value in fields.items()])
        return df.query(query)

    def parse_cable_types(self, cables_df : pd.DataFrame) -> pd.DataFrame:
        pass

    def write_all_data_frames(self, file_name : str = "data.xlsx"):
        self.data_frames["CABLETYPE"] = self.get_cable_type_data_as_dataframe()
        with pd.ExcelWriter(file_name) as writer:
            for name, dataframe in self.data_frames.items():
                dataframe.to_excel(writer, sheet_name=name, index=False)

    def parse_file(self):
        for key, value in self.parse_entities_dict.items():
            if key in self.parse_entities_dict.keys() and key in self.entity_dict.keys():
                if key not in self.data_frames.keys():
                    self.data_frames[key] = pd.DataFrame()
                self.data_frames[key] = pd.concat([self.data_frames[key], self.parse_entities(self.entity_dict[key], value)])
        if "CABLE" in self.data_frames.keys():
            self.data_frames["CABLETYPE"] = self.parse_cable_types(self.data_frames["CABLE"])

    def write_all_data_frames(self, file_name : str = "data.xlsx"):
        with pd.ExcelWriter(file_name) as writer:
            for name, dataframe in self.data_frames.items():
                dataframe.to_excel(writer, sheet_name=name, index=False)