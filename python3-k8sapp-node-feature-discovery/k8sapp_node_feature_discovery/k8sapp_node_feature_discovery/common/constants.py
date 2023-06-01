#
# Copyright (c) 2023 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

# Helm: Supported charts:
# These values match the names in the chart package's Chart.yaml
HELM_CHART_NFD = 'node-feature-discovery'

# Namespace to deploy the application
HELM_NS_NFD = 'node-feature-discovery'

# Application Name
HELM_APP_NFD = 'node-feature-discovery'

# Custom Resources and Custom Resource Definitions
HELM_CRD_GROUP_NFD = 'nfd.k8s-sigs.io'

HELM_CRD_NAME_NF_NFD = 'nodefeatures.nfd.k8s-sigs.io'
HELM_CRD_VERSION_NF_NFD = 'v1alpha1'
HELM_CRD_PLURAL_NF_NFD = 'nodefeatures'
HELM_CRD_SHORT_NF_NFD = 'nf'

HELM_CRD_NAME_NFR_NFD = 'nodefeaturerules.nfd.k8s-sigs.io'
HELM_CRD_VERSION_NFR_NFD = 'v1alpha1'
HELM_CRD_PLURAL_NFR_NFD = 'nodefeaturerules'
HELM_CRD_SHORT_NFR_NFD = 'nfr'
