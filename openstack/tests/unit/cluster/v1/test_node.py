# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import mock
import testtools

from openstack.cluster.v1 import node


FAKE_ID = '123d0955-0099-aabb-b8fa-6a44655ceeff'
FAKE_NAME = 'test_node'

FAKE = {
    'id': FAKE_ID,
    'cluster_id': 'clusterA',
    'metadata': {},
    'name': FAKE_NAME,
    'profile_id': 'myserver',
    'index': 1,
    'role': 'master',
}

FAKE_CREATE_RESP = {
    'node': {
        'id': FAKE_ID,
        'name': FAKE_NAME,
        'cluster_id': '99001122-aabb-ccdd-ffff-efdcab124567',
        'action': '1122aabb-eeff-7755-2222-00991234dcba',
        'created_time': None,
        'deleted_time': None,
        'updated_time': None,
        'data': {},
        'role': 'master',
        'index': 1,
        'init_time': None,
        'metadata': {},
        'profile_id': '560a8f9d-7596-4a32-85e8-03645fa7be13',
        'profile_name': 'myserver',
        'project': '333acb15a43242f4a609a27cb097a8f2',
        'status': 'INIT',
        'status_reason': 'Initializing',
    }
}


class TestNode(testtools.TestCase):

    def setUp(self):
        super(TestNode, self).setUp()

    def test_basic(self):
        sot = node.Node()
        self.assertEqual('node', sot.resource_key)
        self.assertEqual('nodes', sot.resources_key)
        self.assertEqual('/nodes', sot.base_path)
        self.assertEqual('clustering', sot.service.service_type)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_retrieve)
        self.assertTrue(sot.allow_update)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_list)

    def test_instantiate(self):
        sot = node.Node(FAKE)
        self.assertEqual(FAKE['id'], sot.id)
        self.assertEqual(FAKE['name'], sot.name)

        self.assertEqual(FAKE['profile_id'], sot.profile_id)
        self.assertEqual(FAKE['cluster_id'], sot.cluster_id)
        self.assertEqual(FAKE['name'], sot.name)
        self.assertEqual(FAKE['index'], sot.index)
        self.assertEqual(FAKE['role'], sot.role)
        self.assertEqual(FAKE['metadata'], sot.metadata)

    def test_join(self):
        sot = node.Node(FAKE)
        sot['id'] = 'IDENTIFIER'

        resp = mock.Mock()
        resp.body = {'action': '1234-5678-abcd'}
        resp.json = mock.Mock(return_value=resp.body)
        sess = mock.Mock()
        sess.put = mock.Mock(return_value=resp)
        self.assertEqual(resp.body, sot.join(sess, 'cluster-b'))
        url = 'nodes/%s/action' % sot.id
        body = {'join': {'cluster_id': 'cluster-b'}}
        sess.put.assert_called_once_with(url, endpoint_filter=sot.service,
                                         json=body)

    def test_leave(self):
        sot = node.Node(FAKE)
        sot['id'] = 'IDENTIFIER'

        resp = mock.Mock()
        resp.body = {'action': '2345-6789-bbbb'}
        resp.json = mock.Mock(return_value=resp.body)
        sess = mock.Mock()
        sess.put = mock.Mock(return_value=resp)
        self.assertEqual(resp.body, sot.leave(sess))
        url = 'nodes/%s/action' % sot.id
        body = {'leave': {}}
        sess.put.assert_called_once_with(url, endpoint_filter=sot.service,
                                         json=body)
