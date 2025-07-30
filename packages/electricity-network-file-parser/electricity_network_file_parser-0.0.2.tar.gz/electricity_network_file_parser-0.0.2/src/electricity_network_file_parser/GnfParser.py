import pandas as pd
from electricity_network_file_parser.FileParser import FileParser

class GnfParser(FileParser):

    def __init__(self, file_path):
        super().__init__(file_path)
        self.parse_entities_dict = {
            "PROFILE" : ["General", "ProfileType"],
            "GM TYPE" : ["General"],
            "NODE" : ["General"],
            "LINK" : ["General"],
            "CABLE" : ["General", "CablePart", "CableType"],
            "TRANSFORMER" : ["General", "VoltageControl", "TransformerType"],
            "SOURCE" : ["General"],
            "LOAD" : ["General"],
            "HOME" : ["General", "ConnectionCableType", "FuseType"],
            "MEASURE FIELD" : ["General"],
            "FUSE": ["General"]
        }

    def parse_cable_types(self, cables_df : pd.DataFrame) -> pd.DataFrame:
        columns_to_group_by = ["Unom", "Price", "C", "C0", 
                               "Inom0", "G1", "Inom1", "G2", 
                               "Inom2", "G3", "Inom3", "Ik1s", 
                               "Tr", "TInom", "TIk1s", "Frequency", 
                               "R_c", "X_c", "R_cc_n", "X_cc_n", "R_cc_o", 
                               "X_cc_o", "R_e", "X_e", "R_ce", "X_ce", "Inom_e", "Ik1s_e", 
                               "R_h", "X_h", "R_ch_n", "X_ch_n", "R_ch_o", 
                               "X_ch_o", "R_hh_n", "X_hh_n", "R_hh_o", "X_hh_o", "R_he", "X_he", 
                               "Inom_h", "Ik1s_h"]

        unique_cable_types = self.group_data_frame_by_columns(cables_df, columns_to_group_by)
        dictionaries = unique_cable_types.to_dict('records')
        long_names = []
        short_names = []
        for dictionary in dictionaries:
            dictionary.pop("count")
            cables_with_cable_type_params = self.get_records_containing_field_values(cables_df, dictionary)
            cable_types = cables_with_cable_type_params["CableType"].unique()
            short_names_values = cables_with_cable_type_params["ShortName"].unique()
            long_names.append(",".join(cable_types))
            short_names.append(",".join(short_names_values))

        unique_cable_types["Longnames"] = long_names
        unique_cable_types["Shortnames"] = short_names
        return unique_cable_types