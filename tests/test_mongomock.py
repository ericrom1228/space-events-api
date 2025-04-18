from mongomock_motor import AsyncMongoMockClient


async def test_mock_client():
    client = AsyncMongoMockClient()
    collection = client['test_db']['test_collection']
    # collection = AsyncMongoMockClient()['tests']['test-1']

    assert await collection.count_documents({}) == 0

    assert await collection.find({}).to_list(None) == []

    result = await collection.insert_one({'a': 1})
    assert result.inserted_id

    assert len(await collection.find({}).to_list(None)) == 1