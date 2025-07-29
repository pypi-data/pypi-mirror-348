from context import netaio
from enum import IntEnum
import unittest


class TestMisc(unittest.TestCase):
    def setUp(self):
        self.original_message_type_class = netaio.Header.message_type_class

    def tearDown(self):
        netaio.Header.message_type_class = self.original_message_type_class

    def test_message_type_class_monkey_patch(self):
        class TestMessageType(IntEnum):
            TEST = 100

        netaio.Header.message_type_class = TestMessageType
        header = netaio.Header(
            message_type=TestMessageType.TEST,
            auth_length=0,
            body_length=0,
            checksum=0
        )
        data = header.encode()
        decoded = netaio.Header.decode(data)
        assert decoded.message_type is TestMessageType.TEST

    def test_message_type_class_injection(self):
        class TestMessageType(IntEnum):
            TEST = 100

        netaio.Header.message_type_class = TestMessageType
        header = netaio.Header(
            message_type=TestMessageType.TEST,
            auth_length=0,
            body_length=0,
            checksum=0
        )
        data = header.encode()
        decoded = netaio.Header.decode(data, message_type_factory=TestMessageType)
        assert decoded.message_type is TestMessageType.TEST

    def test_Message_encoding_decoding_and_copying(self):
        message = netaio.Message.prepare(
            body=netaio.Body.prepare(b'content', b'uri'),
            message_type=netaio.MessageType.OK,
            auth_data=netaio.AuthFields({'test': b'test'})
        )
        data = message.encode()
        decoded = netaio.Message.decode(data)
        assert decoded.body.content == b'content'
        assert decoded.body.uri == b'uri'
        assert decoded.header.message_type == netaio.MessageType.OK
        assert decoded.auth_data.fields == {'test': b'test'}

        msg = message.copy()
        assert msg.body.content == message.body.content
        assert msg.body.uri == message.body.uri
        assert msg.header.message_type == message.header.message_type
        assert msg.auth_data.fields == message.auth_data.fields

        msg.body.content = b'new content'
        assert msg.body.content != message.body.content

        # now test with missing auth_data and empty body
        message = netaio.Message.prepare(
            body=netaio.Body.prepare(b'', b''),
            message_type=netaio.MessageType.OK
        )
        data = message.encode()
        decoded = netaio.Message.decode(data)
        assert decoded.body.content == b''
        assert decoded.body.uri == b''
        assert decoded.header.message_type == netaio.MessageType.OK
        assert decoded.auth_data.fields == {}

        msg = message.copy()
        assert msg.body.content == message.body.content
        assert msg.body.uri == message.body.uri
        assert msg.header.message_type == message.header.message_type
        assert msg.auth_data.fields == message.auth_data.fields

        msg.body.content = b'new content'
        assert msg.body.content != message.body.content

    def test_UDPNode_peer_helper_methods(self):
        node = netaio.UDPNode(local_peer=netaio.Peer(set(), b'local id', b'local data'))
        # first add a peer
        assert len(node.peers) == 0
        result = node.add_or_update_peer(b'test id', b'test data', ('0.0.0.0', 8888))
        assert type(result) is bool, type(result)
        assert result is True
        assert len(node.peers) == 1
        assert b'test id' in node.peers
        result = node.add_or_update_peer(b'local id', b'anything', ('0.0.0.0', 9999))
        assert type(result) is bool, type(result)
        assert result is False

        # get the peer by id
        peer = node.get_peer(peer_id=b'test id')
        assert peer is not None
        assert peer.id == b'test id'

        # get the peer by addr
        peer = node.get_peer(addr=('0.0.0.0', 8888))
        assert peer is not None
        assert peer.id == b'test id'

        # now remove the peer
        node.remove_peer(('0.0.0.0', 8888), b'test id')
        assert len(node.peers) == 0


if __name__ == "__main__":
    unittest.main()
