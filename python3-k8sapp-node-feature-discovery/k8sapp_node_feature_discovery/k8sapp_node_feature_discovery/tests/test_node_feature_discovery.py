# Copyright (c) 2023 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

from k8sapp_node_feature_discovery.tests import test_plugins

from sysinv.db import api as dbapi
from sysinv.tests.db import base as dbbase
from sysinv.tests.db import utils as dbutils
from sysinv.tests.helm import base


class NodeFeatureDiscoveryTestCase(test_plugins.K8SAppNodeFeatureDiscoveryAppMixin,
                                   base.HelmTestCaseMixin):

    def setUp(self):
        super(NodeFeatureDiscoveryTestCase, self).setUp()
        self.app = dbutils.create_test_app(name='node-feature-discovery')
        self.dbapi = dbapi.get_instance()


class NodeFeatureDiscoveryTestCaseDummy(NodeFeatureDiscoveryTestCase, dbbase.ProvisionedControllerHostTestCase):
    # without a test zuul will fail
    def test_dummy(self):
        pass
