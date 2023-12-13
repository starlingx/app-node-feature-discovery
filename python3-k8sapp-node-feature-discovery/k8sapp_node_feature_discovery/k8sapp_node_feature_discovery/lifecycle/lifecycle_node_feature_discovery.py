#
# Copyright (c) 2023 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
# All Rights Reserved.
#

""" System inventory App lifecycle operator."""

from oslo_log import log as logging
from sysinv.common import constants
from sysinv.common import kubernetes
from sysinv.common import utils as cutils
from sysinv.helm import lifecycle_base as base

from k8sapp_node_feature_discovery.common import constants as app_constants

LOG = logging.getLogger(__name__)


class NodeFeatureDiscoveryAppLifecycleOperator(base.AppLifecycleOperator):

    def app_lifecycle_actions(self, context, conductor_obj, app_op, app, hook_info):
        """Perform lifecycle actions for an operation

        :param context: request context, can be None
        :param conductor_obj: conductor object, can be None
        :param app_op: AppOperator object
        :param app: AppOperator.Application object
        :param hook_info: LifecycleHookInfo object

        """
        if hook_info.lifecycle_type == constants.APP_LIFECYCLE_TYPE_OPERATION:
            if hook_info.operation == constants.APP_REMOVE_OP:
                if hook_info.relative_timing == constants.APP_LIFECYCLE_TIMING_PRE:
                    return self.pre_remove(app, app_op)
                if hook_info.relative_timing == constants.APP_LIFECYCLE_TIMING_POST:
                    return self.post_remove(app, app_op)

        super(NodeFeatureDiscoveryAppLifecycleOperator, self).app_lifecycle_actions(
            context, conductor_obj, app_op, app, hook_info
        )

    def pre_remove(self, app, app_op):
        # Due to ordering of deletes, to prevent the namespace finalizer from waiting
        # indefinitely, we need to ensure that the custom resources, if they exist,
        # are deleted.

        LOG.debug(
            "Executing pre_remove for {} app".format(app_constants.HELM_APP_NFD))

        custom_resources_list = []

        custom_resources_list = app_op._kube.list_namespaced_custom_resources(
                                                app_constants.HELM_CRD_GROUP_NFD,
                                                app_constants.HELM_CRD_VERSION_NF_NFD,
                                                app_constants.HELM_NS_NFD,
                                                app_constants.HELM_CRD_PLURAL_NF_NFD)

        if custom_resources_list:
            for custom_resource in custom_resources_list:

                app_op._kube.delete_custom_resource(
                                            app_constants.HELM_CRD_GROUP_NFD,
                                            app_constants.HELM_CRD_VERSION_NF_NFD,
                                            app_constants.HELM_NS_NFD,
                                            app_constants.HELM_CRD_PLURAL_NF_NFD,
                                            custom_resource["metadata"]["name"])

        custom_resources_list = app_op._kube.list_custom_resources(
                                               app_constants.HELM_CRD_GROUP_NFD,
                                               app_constants.HELM_CRD_VERSION_NFR_NFD,
                                               app_constants.HELM_CRD_PLURAL_NFR_NFD)

        if custom_resources_list:
            for custom_resource in custom_resources_list:

                cmd = [
                    'kubectl',
                    '--kubeconfig',
                    kubernetes.KUBERNETES_ADMIN_CONF,
                    'delete',
                    "{}/{}".format(
                        app_constants.HELM_CRD_SHORT_NFR_NFD,
                        custom_resource["metadata"]["name"]
                    )
                ]

                stdout, stderr = cutils.trycmd(*cmd)

                if stderr:
                    LOG.warn("{} app: cmd={} stdout={} stderr={}".format(app.name,
                                                                         cmd,
                                                                         stdout,
                                                                         stderr))
                else:
                    LOG.debug("{} app: cmd={} stdout={}".format(app.name,
                                                                cmd,
                                                                stdout))

    def post_remove(self, app, app_op):

        LOG.debug(
            "Executing post_remove for {} app".format(app_constants.HELM_APP_NFD))

        # Helm doesn't delete CRDs and the namespace. To clean up after
        # application-remove, we need to explicitly delete them.
        cmd = ['kubectl', '--kubeconfig', kubernetes.KUBERNETES_ADMIN_CONF,
               'delete', 'crd', app_constants.HELM_CRD_NAME_NF_NFD]
        stdout, stderr = cutils.trycmd(*cmd)

        if stderr:
            LOG.warn("{} app: cmd={} stdout={} stderr={}".format(app.name,
                                                                 cmd,
                                                                 stdout,
                                                                 stderr))
        else:
            LOG.debug("{} app: cmd={} stdout={}".format(app.name, cmd, stdout))

        cmd = ['kubectl', '--kubeconfig', kubernetes.KUBERNETES_ADMIN_CONF,
               'delete', 'crd', app_constants.HELM_CRD_NAME_NFR_NFD]
        stdout, stderr = cutils.trycmd(*cmd)

        if stderr:
            LOG.warn("{} app: cmd={} stdout={} stderr={}".format(app.name,
                                                                 cmd,
                                                                 stdout,
                                                                 stderr))
        else:
            LOG.debug("{} app: cmd={} stdout={}".format(app.name, cmd, stdout))

        app_op._kube.kube_delete_namespace(app_constants.HELM_NS_NFD)
