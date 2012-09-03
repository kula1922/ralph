#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.conf import settings

from ralph.util import plugin
from ralph .discovery.plugins.ssh_ibm_bladecenter import ssh_ibm_reboot
from ralph.discovery.plugins.ipmi import ipmi_reboot
from ralp.discovery.hp_ilo import IloHost


@plugin.register(chain='deployment', requires=['ticket', 'dns', 'dhcp'],
                 priority=0)
def reboot(deployment):
    management = deployment.device.find_management()

    user, password = settings.ILO_USER, settings.ILO_PASSWORD
    if user:
        if IloHost(management, user, password).reboot(True):
            return True

    user, password = settings.IPMI_USER, settings.IPMI_PASSWORD
    if user:
        if ipmi_reboot(management, user, password, True):
            return
    user = settings.SSH_IBM_USER
    bay = deployment.device.chassis_position
    if user and bay:
        if ssh_ibm_reboot(management, bay):
            return True
    return False