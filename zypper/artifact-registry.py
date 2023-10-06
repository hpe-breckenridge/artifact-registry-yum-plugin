#!/usr/bin/env python3
#
#  Copyright 2023 Hewlett Packard Enterprise Development LP
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from functools import cache
from subprocess import PIPE, run
import traceback

# See https://github.com/openSUSE/zypp-plugin
# Provided by python3(9|10|11)-zypp-plugin package
from zypp_plugin import Plugin


token_cmd = '/usr/libexec/ar-token'


class ArtifactRegistryPlugin(Plugin):

    URL = 'https://{location}-yum.pkg.dev/projects/{project}/{repository}'

    def RESOLVEURL(self, headers, data):
        try:
            url = self.URL.format(**headers)
            token = _get_token(**headers)
            self.answer('RESOLVEDURL', {'Authorization': f'Bearer {token}'}, url)
        except:
            self.error(body=traceback.format_exc())

@cache
def _get_token(service_account_json=None, service_account_email=None, **kwds):
    args = [token_cmd]
    # JSON has priority over email.
    if service_account_json:
        args.append('--service_account_json=' + service_account_json)
    elif service_account_email:
        args.append('--service_account_email=' + service_account_email)
    proc = run(args, stdout=PIPE, check=True, text=True)
    return proc.stdout


plugin = ArtifactRegistryPlugin()
plugin.main()
