import aiohttp


def with_session(async_function):
    async def _inner(*args, session=None, **kwargs):
        if session:
            return await async_function(*args, **kwargs, session=session)

        async with aiohttp.ClientSession() as session:
            return await async_function(*args, **kwargs, session=session)
    return _inner
