import pytest
from unittest.mock import Mock, patch

from .main import app, on_event, src_data_topic
import asyncio


@pytest.fixture()
def test_app(event_loop):
    """passing in event_loop helps avoid 'attached to a different loop' error"""
    app.finalize()
    app.conf.store = 'memory://'
    app.flow_control.resume()
    return app


@pytest.mark.asyncio()
async def test_on_event(test_app):
    pass
    with patch(__name__ + '.src_data_topic') as mocked_src_data_topic:
        mocked_src_data_topic.send()
        print("==========")
        print(type(mocked_src_data_topic))
    #     mocked_src_data_topic.send = mock_coro()
        async with on_event.test_context() as agent:
            print(type(agent))
            agent.put('{"foo": 1}')
    #         mocked_src_data_topic.send.assert_called_with({'foo': 1})


# def mock_coro(return_value=None, **kwargs):
#     """Create mock coroutine function."""
#
#     async def wrapped(*args, **kwargs):
#         return return_value
#
#     return Mock(wraps=wrapped, **kwargs)
