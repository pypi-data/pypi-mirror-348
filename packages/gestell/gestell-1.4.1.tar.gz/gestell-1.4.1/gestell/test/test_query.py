import os
import pytest
from gestell import Gestell

gestell = Gestell()
organization_id = os.getenv('ORGANIZATION_ID')
if not organization_id:
    raise ValueError('ORGANIZATION_ID environment variable is not set')
collection_id = ''
feature_id = ''
table_id = ''


@pytest.mark.asyncio
async def test_create_collection():
    global collection_id
    response = await gestell.collection.create(
        organization_id=organization_id,
        name='Automated Test Collection',
        description='An automated test collection',
        type='canon',
        categories=[
            {
                'name': 'Unga Bunga Features',
                'type': 'features',
                'instructions': 'Unga Bunga, Features, Unga Bunga',
            },
            {
                'name': 'Unga Bunga Tables',
                'type': 'table',
                'instructions': 'Unga Bunga, Tables, Unga Bunga',
            },
        ],
    )
    assert response.status == 'OK'
    assert len(response.id) > 1
    collection_id = response.id


@pytest.mark.asyncio
async def test_retrieve_category_ids():
    global feature_id, table_id

    collections = await gestell.collection.list()
    assert collections.status == 'OK'
    assert len(collections.result) > 0, 'No collections found'

    collection_id = collections.result[0].id

    response = await gestell.collection.get(collection_id=collection_id)
    assert response.status == 'OK'
    assert response.result is not None, 'No collection data returned'
    assert response.result.categories is not None, 'No categories found in collection'

    for category in response.result.categories:
        if category.type == 'features':
            feature_id = category.id
        if category.type == 'table':
            table_id = category.id


@pytest.mark.asyncio
async def test_query_search():
    response = await gestell.query.search(
        collection_id=collection_id,
        prompt='Unga Bunga, do not return anything, Unga Bunga',
        method='fast',
    )
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_query_prompt():
    response = gestell.query.prompt(
        collection_id=collection_id,
        prompt='Unga Bunga, do not return anything, Unga Bunga',
    )
    full_response = b''
    async for chunk in response:
        full_response += chunk

    result = full_response.decode('utf-8')
    assert len(result) > 1


@pytest.mark.asyncio
async def test_query_features():
    response = await gestell.query.features(
        collection_id=collection_id, category_id=feature_id
    )
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_query_table():
    response = await gestell.query.table(
        collection_id=collection_id, category_id=table_id
    )
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_delete_collection():
    response = await gestell.collection.delete(collection_id)
    assert response.status == 'OK'
