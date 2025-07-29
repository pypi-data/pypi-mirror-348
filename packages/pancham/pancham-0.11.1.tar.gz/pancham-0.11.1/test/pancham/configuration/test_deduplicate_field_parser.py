import pandas as pd

from configuration.deduplicate_field_parser import DeduplicateFieldParser


class TestExplodeFieldParser:


    def test_parse_field(self):
        parser = DeduplicateFieldParser()
        field = {
            'name': 'a',
            'func': {
                'deduplicate': {}
            }
        }

        assert parser.can_parse_field(field)

    def test_deduplicate_field(self):
        parser = DeduplicateFieldParser()
        field = {
            'name': 'a',
            'field_type': 'str',
            'func': {
                'deduplicate': {
                    'source_name': 'b',
                }
            }
        }

        dfield = parser.parse_field(field)

        data= pd.DataFrame({
            'b': ['a', 'c', 'd', 'd'],
            'c': [1, 2, 3, 4]
        })

        out = dfield.df_func(data)

        assert len(out) == 3
