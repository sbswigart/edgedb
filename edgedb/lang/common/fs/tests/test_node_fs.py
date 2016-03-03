##
# Copyright (c) 2013 MagicStack Inc.
# All rights reserved.
#
# See LICENSE for details.
##


import os
import uuid

from metamagic.utils.fs.nodesystem import FSSystem


class TestNodeFSSystem:
    def test_utils_fs_node_1(self):
        from . import node
        from .bucket import TestBucket
        from metamagic.utils.fs import Bucket, backends

        assert issubclass(node.FS, FSSystem)
        assert node.FS.class_buckets[TestBucket][0].cls is backends.FSBackend

        c = node.FS()
        c.configure()
        assert not Bucket.get_backends()
        assert len(TestBucket.get_backends()) == 1

        dirname = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
        b = TestBucket.get_backends()[0]
        assert b.path == os.path.join(dirname, 'foo')
        assert b.pub_path == '/a'


        test_id = uuid.UUID('7f7d4de4-bf14-11e2-ad89-50b7c37a37b2')

        name = b._get_base_name(TestBucket, test_id, 'z' * 50 + 'o' * 100 + '.jpg')
        assert name[-b._FN_LEN_LIMIT-1:] == '/7f7d4de4bf1411e2ad8950b7c37a37b2_zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz.jpg'
        assert name == 'c6ed112e-bf13-11e2-9cfc-3b4fcbee9e31/4G/R4/7f7d4de4bf1411e2ad8950b7c37a37b2_zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz.jpg'

        name = b._get_base_name(TestBucket, test_id, '.' + 'z' * 50 + 'o' * 100)
        assert name[-b._FN_LEN_LIMIT-1:] == '/7f7d4de4bf1411e2ad8950b7c37a37b2_.zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'
        assert name == 'c6ed112e-bf13-11e2-9cfc-3b4fcbee9e31/4G/R4/7f7d4de4bf1411e2ad8950b7c37a37b2_.zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'

        name = b._get_base_name(TestBucket, test_id, 'z' * 20 + 'o' * 100)
        assert name[-b._FN_LEN_LIMIT-1:] == '/7f7d4de4bf1411e2ad8950b7c37a37b2_zzzzzzzzzzzzzzzzzzzzoooooooooooooooooooooo'
        assert name == 'c6ed112e-bf13-11e2-9cfc-3b4fcbee9e31/4G/R4/7f7d4de4bf1411e2ad8950b7c37a37b2_zzzzzzzzzzzzzzzzzzzzoooooooooooooooooooooo'

        name = b._get_base_name(TestBucket, test_id, 'spam.png')
        assert name == 'c6ed112e-bf13-11e2-9cfc-3b4fcbee9e31/4G/R4/7f7d4de4bf1411e2ad8950b7c37a37b2_spam.png'
