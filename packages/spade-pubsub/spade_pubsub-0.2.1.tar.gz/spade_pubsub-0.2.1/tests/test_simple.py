import pytest
import asyncio
from pyjabber.server import Server
import slixmpp

async def wait_for_server(server, timeout=5.0):
    """Wait until the server is ready (has a _client_listener)."""
    t0 = asyncio.get_event_loop().time()
    while not (hasattr(server, '_client_listener') and server._client_listener):
        if asyncio.get_event_loop().time() - t0 > timeout:
            raise TimeoutError("Server did not start within timeout")
        await asyncio.sleep(0.1)

@pytest.fixture
async def server_fixture():
    srv = Server(host="localhost", database_in_memory=True)
    # Launch server.start() in background so it does not block
    server_task = asyncio.create_task(srv.start())
    await wait_for_server(srv)
    yield srv
    await srv.stop()
    server_task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await server_task

@pytest.mark.asyncio
async def test_client_connect_disconnect(server_fixture):
    class TestClient(slixmpp.ClientXMPP):
        def __init__(self, jid, password):
            super().__init__(jid, password)
            self.add_event_handler("session_start", self.start)
            self.add_event_handler("disconnected", self.disconnected)
            self.connected = False
            self.disconnected_event = False

        def start(self, event):
            self.connected = True
            self.disconnect()

        def disconnected(self, event):
            self.disconnected_event = True

    jid = "test@localhost"
    password = "password"
    client = TestClient(jid, password)
    client.connect()
    await client.process(forever=False)

    assert client.connected
    assert client.disconnected_event
