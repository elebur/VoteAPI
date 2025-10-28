# https://www.vintasoftware.com/blog/how-i-test-my-drf-serializers#mastering-drf-serializer-testing-a-comprehensive-example
class TestMenuSerializerWithDuplicatedItems:
    def test_no_duplicates_in_db(self):
        assert 1 == 2

    def test_same_item_name_with_different_description(self):
        assert 1 == 2
