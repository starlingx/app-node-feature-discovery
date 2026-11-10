# Copyright (c) 2023,2026 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

import glob
import os

import yaml

from k8sapp_node_feature_discovery.tests import test_plugins

from sysinv.db import api as dbapi
from sysinv.tests.db import base as dbbase
from sysinv.tests.db import utils as dbutils
from sysinv.tests.helm import base

# Pod Security Admission label the node-feature-discovery namespace must
# carry so the framework PSA helper treats it as a privileged (managed)
# namespace instead of skipping it (STX.APP.19 / CGTS-110133).
PSA_ENFORCE_LABEL = 'pod-security.kubernetes.io/enforce'
PSA_ENFORCE_LEVEL = 'privileged'
NFD_NAMESPACE = 'node-feature-discovery'


def _find_namespace_manifest():
    """Locate the fluxcd base/namespace.yaml shipped by the app.

    The manifest lives in the sibling stx-node-feature-discovery package.
    Walk up from this test file looking for it so the test does not depend
    on a fixed relative depth, and returns None when the manifest is not
    present (e.g. an isolated build sandbox) so the test can be skipped.
    """
    search_root = os.path.abspath(os.path.dirname(__file__))
    for _ in range(8):
        matches = glob.glob(os.path.join(
            search_root, '**', 'fluxcd-manifests', 'base', 'namespace.yaml'),
            recursive=True)
        if matches:
            return matches[0]
        parent = os.path.dirname(search_root)
        if parent == search_root:
            break
        search_root = parent
    return None


class NodeFeatureDiscoveryTestCase(test_plugins.K8SAppNodeFeatureDiscoveryAppMixin,
                                   base.HelmTestCaseMixin):

    def setUp(self):
        super(NodeFeatureDiscoveryTestCase, self).setUp()
        self.app = dbutils.create_test_app(name='node-feature-discovery')
        self.dbapi = dbapi.get_instance()


class NodeFeatureDiscoveryNamespacePSATestCase(
        test_plugins.K8SAppNodeFeatureDiscoveryAppMixin,
        base.HelmTestCaseMixin):

    def test_namespace_has_privileged_psa_label(self):
        """The NFD namespace must be labeled privileged for PSA.

        Closes the STX.APP.19 gap (CGTS-110133): without this label the
        framework PSA helper skips the namespace and NFD pods would be
        rejected under strict Pod Security Admission enforcement.
        """
        manifest = _find_namespace_manifest()
        if manifest is None:
            self.skipTest('base/namespace.yaml not available in this '
                          'test environment')

        with open(manifest) as f:
            docs = list(yaml.safe_load_all(f))

        nfd_ns = None
        for doc in docs:
            if not doc:
                continue
            if (doc.get('kind') == 'Namespace' and
                    doc.get('metadata', {}).get('name') == NFD_NAMESPACE):
                nfd_ns = doc
                break

        self.assertIsNotNone(
            nfd_ns,
            'node-feature-discovery Namespace not found in %s' % manifest)

        labels = nfd_ns.get('metadata', {}).get('labels', {})
        self.assertEqual(
            labels.get(PSA_ENFORCE_LABEL), PSA_ENFORCE_LEVEL,
            '%s namespace must carry %s=%s for Pod Security Admission' % (
                NFD_NAMESPACE, PSA_ENFORCE_LABEL, PSA_ENFORCE_LEVEL))


class NodeFeatureDiscoveryTestCaseDummy(NodeFeatureDiscoveryTestCase, dbbase.ProvisionedControllerHostTestCase):
    # without a test zuul will fail
    def test_dummy(self):
        pass
