import os
import pytest
from gestell import Gestell

gestell = Gestell()
organization_id = os.getenv('ORGANIZATION_ID')
if not organization_id:
    raise ValueError('ORGANIZATION_ID environment variable is not set')


@pytest.mark.asyncio
async def test_get_organization():
    response = await gestell.organization.get(id=organization_id)
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_list_organizations():
    response = await gestell.organization.list()
    assert response.status == 'OK'
    assert len(response.result) > 0


@pytest.mark.asyncio
async def test_list_organizations_with_skip():
    response = await gestell.organization.list(skip=100, take=0)
    assert response.status == 'OK'
    assert len(response.result) == 0


@pytest.mark.asyncio
async def test_list_organizations_with_search():
    response = await gestell.organization.list(search='Unga Bunga 42 42')
    assert response.status == 'OK'
    assert len(response.result) == 0


@pytest.mark.asyncio
async def test_update_organization():
    response = await gestell.organization.update(
        id=organization_id,
        name='Automated Test Organization Updated',
        description='This is an automated test organization updated',
    )
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_add_member_to_organization():
    response = await gestell.organization.add_members(
        id=organization_id,
        members=[{'id': 'test@chriscates.ca', 'role': 'member'}],
    )
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_remove_member_from_organization():
    response = await gestell.organization.remove_members(
        id=organization_id,
        members=['test@chriscates.ca'],
    )
    assert response.status == 'OK'
