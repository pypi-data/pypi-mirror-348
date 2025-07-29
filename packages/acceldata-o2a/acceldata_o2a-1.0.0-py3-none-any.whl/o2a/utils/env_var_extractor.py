# -*- coding: utf-8 -*-
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Extract params from oozie's action node"""
from _elementtree import Element

from o2a.o2a_libs.src.o2a_lib import el_parser
from o2a.utils import xml_utils

TAG_ENV_VAR = "env-var"


def extract_env_var_values_from_action_node(oozie_node: Element):
    env_var_nodes = xml_utils.find_nodes_by_tag(oozie_node, TAG_ENV_VAR)

    new_env_vars = {}
    for node in env_var_nodes:
        if not node.text:
            continue
        env_var = el_parser.translate(node.text)
        key, _, value = env_var.partition("=")
        new_env_vars[key] = value
    return new_env_vars
