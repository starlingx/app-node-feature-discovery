#
# Copyright (c) 2023 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

from sysinv.common import exception
from sysinv.helm import base

from k8sapp_node_feature_discovery.common import constants as app_constants


class NodeFeatureDiscoveryHelm(base.BaseHelm):
    """Class to encapsulate helm operations for the node feature discovery chart"""

    SUPPORTED_NAMESPACES = base.BaseHelm.SUPPORTED_NAMESPACES + \
        [app_constants.HELM_NS_NFD]
    SUPPORTED_APP_NAMESPACES = {
        app_constants.HELM_APP_NFD:
            base.BaseHelm.SUPPORTED_NAMESPACES + [app_constants.HELM_NS_NFD],
    }

    CHART = app_constants.HELM_CHART_NFD

    SERVICE_NAME = app_constants.HELM_APP_NFD

    def get_namespaces(self):
        return self.SUPPORTED_NAMESPACES

    def get_overrides(self, namespace=None):

        overrides = {
            app_constants.HELM_NS_NFD: {}
        }

        if namespace in self.SUPPORTED_NAMESPACES:
            return overrides[namespace]

        if namespace:
            raise exception.InvalidHelmNamespace(chart=self.CHART,
                                                 namespace=namespace)

        return overrides
