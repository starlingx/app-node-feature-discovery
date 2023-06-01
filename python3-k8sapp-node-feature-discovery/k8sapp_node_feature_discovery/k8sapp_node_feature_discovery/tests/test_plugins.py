#
# Copyright (c) 2023 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

from k8sapp_node_feature_discovery.common import constants as app_constants

from sysinv.tests.db import base as dbbase


class K8SAppNodeFeatureDiscoveryAppMixin(object):
    app_name = app_constants.HELM_APP_NFD
    path_name = app_name + '.tgz'

    def setUp(self):
        super(K8SAppNodeFeatureDiscoveryAppMixin, self).setUp()


# Test Configuration:
# - Controller
# - IPv6
# - Ceph Storage
# - node-feature-discovery app
class K8sAppNodeFeatureDiscoveryControllerTestCase(K8SAppNodeFeatureDiscoveryAppMixin,
                                                   dbbase.BaseIPv6Mixin,
                                                   dbbase.BaseCephStorageBackendMixin,
                                                   dbbase.ControllerHostTestCase):
    pass


# Test Configuration:
# - AIO
# - IPv4
# - Ceph Storage
# - node-feature-discovery app
class K8SAppNodeFeatureDiscoveryAIOTestCase(K8SAppNodeFeatureDiscoveryAppMixin,
                                            dbbase.BaseCephStorageBackendMixin,
                                            dbbase.AIOSimplexHostTestCase):
    pass
