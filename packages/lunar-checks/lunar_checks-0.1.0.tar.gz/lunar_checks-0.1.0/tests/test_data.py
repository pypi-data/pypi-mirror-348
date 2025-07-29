import pytest
import json
from src.lunar_snippets.data import SnippetData, JsonPathExpression


class TestGetMerged():
    @pytest.fixture
    def snippet_data(self):
        test_data = {
            'metadata_instances': [],
            'merged_blob': {
                'string': 'hello world',
                'array': ['hello', 'world'],
                'object1': {'hello': 'world'},
                'object2': {'hello': 'moon'}
            }
        }
        return SnippetData.from_json(json.dumps(test_data))

    def assert_result(self, result, expected_value, expected_paths):
        assert result is not None
        assert result.value == expected_value
        assert result.paths == expected_paths

    def test_get_single_value(self, snippet_data):
        result = snippet_data.get_merged(JsonPathExpression('.string'))
        self.assert_result(result, 'hello world', ['string'])

    def test_get_missing(self, snippet_data):
        result = snippet_data.get_merged(JsonPathExpression('.missing'))
        assert result is None

    def test_get_array(self, snippet_data):
        result = snippet_data.get_merged(JsonPathExpression('.array'))
        self.assert_result(result, ['hello', 'world'], ['array'])

    def test_get_array_index(self, snippet_data):
        result = snippet_data.get_merged(JsonPathExpression('.array[0]'))
        self.assert_result(result, 'hello', ['array.[0]'])

    def test_get_nested_object(self, snippet_data):
        result = snippet_data.get_merged(JsonPathExpression('.object1.hello'))
        self.assert_result(result, 'world', ['object1.hello'])

    def test_get_nested_object_missing(self, snippet_data):
        result = snippet_data.get_merged(
            JsonPathExpression('.object1.missing')
        )
        assert result is None

    def test_multi_match_array_index(self, snippet_data):
        result = snippet_data.get_merged(JsonPathExpression('.array[*]'))
        self.assert_result(
            result,
            ['hello', 'world'],
            ['array.[0]', 'array.[1]']
        )

    def test_multi_match_object_key(self, snippet_data):
        result = snippet_data.get_merged(JsonPathExpression('..hello'))
        self.assert_result(
            result,
            ['world', 'moon'],
            ['object1.hello', 'object2.hello']
        )


class TestGetAll():
    @pytest.fixture
    def snippet_data(self):
        test_data = {
            'merged_blob': {},
            'metadata_instances': [
                {
                    'payload': {
                        'single': 'hello world',
                        'double': 'hello1',
                        'single_array': ['hello', 'world'],
                        'double_array': ['goodbye', 'moon'],
                        'single_object': {'hello': 'world'},
                        'double_object': {'hello': 'moon'}
                    }
                },
                {
                    'payload': {
                        'double': 'hello2',
                        'double_array': ['mars', 'i', 'guess'],
                        'double_object': {'hello': 'venus'}
                    }
                }
            ]
        }
        return SnippetData.from_json(json.dumps(test_data))

    def assert_all_results(self, result, expected):
        assert result is not None
        assert len(result) == len(expected)
        for idx, (expected_value, expected_paths) in enumerate(expected):
            assert result[idx].value == expected_value
            assert result[idx].paths == expected_paths

    def test_get_single_key_in_one_delta(self, snippet_data):
        result = snippet_data.get_all(JsonPathExpression('.single'))
        self.assert_all_results(result, [
            ('hello world', ['single'])
        ])

    def test_get_single_key_in_two_deltas(self, snippet_data):
        result = snippet_data.get_all(JsonPathExpression('.double'))
        self.assert_all_results(result, [
            ('hello2', ['double']),
            ('hello1', ['double'])
        ])

    def test_get_missing(self, snippet_data):
        result = snippet_data.get_all(JsonPathExpression('.missing'))
        self.assert_all_results(result, [])

    def test_get_single_array(self, snippet_data):
        result = snippet_data.get_all(JsonPathExpression('.single_array'))
        self.assert_all_results(result, [
            (['hello', 'world'], ['single_array'])
        ])

    def test_get_single_array_index(self, snippet_data):
        result = snippet_data.get_all(JsonPathExpression('.single_array[0]'))
        self.assert_all_results(result, [
            ('hello', ['single_array.[0]'])
        ])

    def test_get_double_array(self, snippet_data):
        result = snippet_data.get_all(JsonPathExpression('.double_array'))
        self.assert_all_results(result, [
            (['mars', 'i', 'guess'], ['double_array']),
            (['goodbye', 'moon'], ['double_array'])
        ])

    def test_get_double_array_index(self, snippet_data):
        result = snippet_data.get_all(JsonPathExpression('.double_array[0]'))
        self.assert_all_results(result, [
            ('mars', ['double_array.[0]']),
            ('goodbye', ['double_array.[0]'])
        ])

    def test_get_double_array_index_some_out_of_bounds(self, snippet_data):
        result = snippet_data.get_all(JsonPathExpression('.double_array[2]'))
        self.assert_all_results(result, [
            ('guess', ['double_array.[2]'])
        ])

    def test_get_single_object(self, snippet_data):
        result = snippet_data.get_all(JsonPathExpression('.single_object'))
        self.assert_all_results(result, [
            ({'hello': 'world'}, ['single_object'])
        ])

    def test_get_double_object(self, snippet_data):
        result = snippet_data.get_all(JsonPathExpression('.double_object'))
        self.assert_all_results(result, [
            ({'hello': 'venus'}, ['double_object']),
            ({'hello': 'moon'}, ['double_object'])
        ])

    def test_get_single_object_key(self, snippet_data):
        result = snippet_data.get_all(
            JsonPathExpression('.single_object.hello')
        )
        self.assert_all_results(result, [
            ('world', ['single_object.hello'])
        ])

    def test_get_double_object_key(self, snippet_data):
        result = snippet_data.get_all(
            JsonPathExpression('.double_object.hello')
        )
        self.assert_all_results(result, [
            ('venus', ['double_object.hello']),
            ('moon', ['double_object.hello'])
        ])

    def test_get_single_object_key_missing(self, snippet_data):
        result = snippet_data.get_all(
            JsonPathExpression('.single_object.missing')
        )
        self.assert_all_results(result, [])

    def test_get_double_object_key_missing(self, snippet_data):
        result = snippet_data.get_all(
            JsonPathExpression('.double_object.missing')
        )
        self.assert_all_results(result, [])

    def test_multi_match_single_array_index(self, snippet_data):
        result = snippet_data.get_all(JsonPathExpression('.single_array[*]'))
        self.assert_all_results(result, [
            (['hello', 'world'], ['single_array.[0]', 'single_array.[1]'])
        ])

    def test_multi_match_double_array_index(self, snippet_data):
        result = snippet_data.get_all(JsonPathExpression('.double_array[*]'))
        self.assert_all_results(result, [
            (
                ['mars', 'i', 'guess'],
                ['double_array.[0]', 'double_array.[1]', 'double_array.[2]']
            ),
            (
                ['goodbye', 'moon'],
                ['double_array.[0]', 'double_array.[1]']
            )
        ])

    def test_multi_match_object_key(self, snippet_data):
        result = snippet_data.get_all(JsonPathExpression('..hello'))
        self.assert_all_results(result, [
            ('venus', ['double_object.hello']),
            (['world', 'moon'], ['single_object.hello', 'double_object.hello'])
        ])


class TestJsonPathExpression():
    def test_invalid_json_path(self):
        with pytest.raises(ValueError):
            JsonPathExpression('.[invalid')

    def test_invalid_snippet_data(self):
        with pytest.raises(ValueError):
            SnippetData({})

    def test_invalid_snippet_data_missing_merged_blob(self):
        with pytest.raises(ValueError):
            SnippetData({
                'metadata_instances': []
            })

    def test_invalid_snippet_data_missing_metadata_instances(self):
        with pytest.raises(ValueError):
            SnippetData({
                'merged_blob': {}
            })
