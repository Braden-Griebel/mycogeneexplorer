import unittest
import os
import mycogeneexplorer.read_gene_list


class TestReadGeneList(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dict_base_path = os.path.join("..", "data", "name_dicts")
        cls.locus_list_path = os.path.join(dict_base_path, "locus_list.json")
        cls.names_to_locus_path = os.path.join(dict_base_path, "names_to_locus.json")
        cls.uniprot_to_locus_path = os.path.join(dict_base_path, "uniprot_to_locus.json")

    def test_parse_list(self):
        """
        test the parse_list function from read_gene_list module
        :return: None
        """
        input_string = "Rv1746-Rv5467, Rv2346,Rv5600 Rv5123\nRv0987"
        check_list = ["Rv1746", "Rv5467", "Rv2346", "Rv5600", "Rv5123", "Rv0987"]
        self.assertListEqual(
            mycogeneexplorer.read_gene_list.parse_list(input_string),
            check_list)

    def test_translate_list(self):
        """
        test the translate_list function from read_gene_list module
        :return: None
        """
        input_string = "P71925, P71926, gyrB"
        check_list = ["Rv2423", "Rv2422", "Rv0005"]
        self.assertListEqual(
            mycogeneexplorer.read_gene_list.translate_list(input_string),
            check_list
        )


if __name__ == '__main__':
    unittest.main()
