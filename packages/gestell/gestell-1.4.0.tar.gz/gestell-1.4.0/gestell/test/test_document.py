import os
import pytest
from gestell import Gestell
from pathlib import Path
from aiofile import AIOFile
import aiohttp


gestell = Gestell()
organization_id = os.getenv('ORGANIZATION_ID')
if not organization_id:
    raise ValueError('ORGANIZATION_ID environment variable is not set')
collection_id = ''
document_id = ''


@pytest.mark.asyncio
async def test_create_collection():
    global collection_id
    response = await gestell.collection.create(
        organization_id=organization_id,
        name='Automated Test Collection',
        description='An automated test collection',
        type='frame',
    )
    assert response.status == 'OK'
    assert len(response.id) > 1
    collection_id = response.id


@pytest.mark.asyncio
async def test_presign_upload_and_create_document():
    global document_id
    test_file_path = Path(__file__).parent / 'sample.jpg'

    presign_response = await gestell.document.presign(
        collection_id=collection_id, filename='sample.jpg', type='image/jpeg'
    )
    assert presign_response.status == 'OK'

    async with AIOFile(str(test_file_path), 'rb') as f:
        file_content = await f.read()

    async with aiohttp.ClientSession() as session:
        await session.put(
            presign_response.url,
            headers={'ContentType': 'image/jpeg'},
            data=file_content,
        )

    create_response = await gestell.document.create(
        collection_id=collection_id,
        name='sample.jpg',
        path=presign_response.path,
        type='image/jpeg',
        job=False,
    )
    assert create_response.status == 'OK'
    document_id = create_response.id


@pytest.mark.asyncio
async def test_upload_document_as_buffer_and_string():
    test_file_path = Path(__file__).parent / 'sample.jpg'
    response = await gestell.document.upload(
        collection_id=collection_id,
        name='sample-2.jpg',
        file=str(test_file_path),
        job=False,
    )

    assert response.status == 'OK'

    await gestell.document.delete(collection_id=collection_id, document_id=response.id)

    async with AIOFile(str(test_file_path), 'rb') as f:
        file_content = await f.read()
    response2 = await gestell.document.upload(
        collection_id=collection_id,
        name='sample-2.jpg',
        type='image/jpeg',
        file=file_content,
        job=False,
    )

    assert response2.status == 'OK'

    await gestell.document.delete(collection_id=collection_id, document_id=response2.id)


@pytest.mark.asyncio
async def test_update_document():
    response = await gestell.document.update(
        collection_id=collection_id, document_id=document_id, name='sample-updated.jpg'
    )
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_get_document():
    response = await gestell.document.get(
        collection_id=collection_id, document_id=document_id
    )
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_get_document_job():
    response = await gestell.job.get(
        collection_id=collection_id, document_id=document_id
    )
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_reprocess_document_job():
    response = await gestell.job.reprocess(
        collection_id=collection_id, type='status', ids=[document_id]
    )
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_cancel_document_job():
    response = await gestell.job.cancel(collection_id=collection_id, ids=[document_id])
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_delete_document():
    response = await gestell.document.delete(
        collection_id=collection_id, document_id=document_id
    )
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_delete_collection():
    response = await gestell.collection.delete(collection_id=collection_id)
    assert response.status == 'OK'
