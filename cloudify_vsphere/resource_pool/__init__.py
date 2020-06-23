# Copyright (c) 2019-2020 Cloudify Platform Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Stdlib imports

# Third party imports
from pyVmomi import vim

# Cloudify imports
from cloudify.exceptions import NonRecoverableError

# This package imports
from ..utils import op
from vsphere_plugin_common import (
    with_server_client,
)
from vsphere_plugin_common.constants import (
    RESOURCE_POOL_ID,
)


@op
@with_server_client
def create(ctx, server_client, name, use_external_resource):
    vmware_resource = server_client._get_obj_by_name(
        vim.ResourcePool,
        name,
    )

    if use_external_resource:
        if not vmware_resource:
            raise NonRecoverableError(
                'Could not use existing resource_pool "{name}" as no '
                'resource_pool by that name exists!'.format(
                    name=name,
                )
            )
    else:
        raise NonRecoverableError(
            'Datastores cannot currently be created by this plugin.'
        )

    ctx.instance.runtime_properties[RESOURCE_POOL_ID] = vmware_resource.id


@op
@with_server_client
def delete(ctx, name, use_external_resource, **_):
    if use_external_resource:
        ctx.logger.info(
            'Not deleting existing resource_pool: {name}'.format(
                name=name,
            )
        )
    else:
        ctx.logger.info(
            'Not deleting resource_pool {name} as creation and deletion of '
            'resource_pools is not currently supported by this plugin.'.format(
                name=name,
            )
        )
