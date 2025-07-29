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
"""Maps Shell action into Airflow's DAG"""
from typing import List, Set, Dict
from xml.etree.ElementTree import Element


from o2a.converter.task import Task
from o2a.converter.relation import Relation
from o2a.mappers.action_mapper import ActionMapper
from o2a.mappers.extensions.prepare_mapper_extension import PrepareMapperExtension
from o2a.o2a_libs.src.o2a_lib.property_utils import PropertySet
from o2a.utils.xml_utils import get_tag_el_text, get_tags_el_array_from_text, find_nodes_by_tag
from o2a.o2a_libs.src.o2a_lib import el_parser
from o2a.utils.el_utils import normalize_path
from o2a.utils.env_var_extractor import extract_env_var_values_from_action_node

TAG_RESOURCE = "resource-manager"
TAG_NAME = "name-node"
TAG_CMD = "exec"
TAG_ARG = "argument"
TAG_FILE = "file"


class ShellMapper(ActionMapper):
    """
    Converts a Shell Oozie action to an Airflow task.
    """

    def __init__(self, oozie_node: Element, name: str, props: PropertySet, **kwargs):
        ActionMapper.__init__(self, oozie_node=oozie_node, name=name, props=props, **kwargs)
        self._parse_oozie_node()
        self.prepare_extension: PrepareMapperExtension = PrepareMapperExtension(self)

    def _parse_oozie_node(self):
        self.resource_manager = get_tag_el_text(self.oozie_node, TAG_RESOURCE)
        self.name_node = get_tag_el_text(self.oozie_node, TAG_NAME)

        cmd_txt = get_tag_el_text(self.oozie_node, TAG_CMD)
        args = get_tags_el_array_from_text(self.oozie_node, TAG_ARG)
        
        # Format each argument with proper spacing
        formatted_args = []
        for arg in args:
            formatted_args.append(f" {arg} ")
        
        # Join the command with the formatted arguments
        cmd = cmd_txt + "".join(formatted_args)

        self.bash_command = el_parser.translate(cmd, quote=False)
        self.pig_command = f"sh {self.bash_command}"
        
        # Parse file nodes
        self.hdfs_files = self._parse_file_nodes()
        self.new_env_vars = extract_env_var_values_from_action_node(self.oozie_node)

    def _parse_file_nodes(self) -> List[Dict[str, str]]:
        """
        Parse the <file> nodes which specify HDFS files to be copied to the local working directory.
        
        In Oozie, the file elements can include an optional local name fragment after the # character.
        For example:
            <file>hdfs://path/to/file.sh</file> - copies the file with original name
            <file>hdfs://path/to/file.sh#renamed.sh</file> - copies and renames to renamed.sh
        
        Returns:
            List of dictionaries with 'source' and 'target' keys
        """
        files = []
        file_nodes = find_nodes_by_tag(self.oozie_node, TAG_FILE)
        
        for file_node in file_nodes:
            file_path = file_node.text
            if not file_path:
                continue
                
            # Normalize the path to handle variable substitution
            file_path = normalize_path(file_path, props=self.props, allow_no_schema=True)
            
            # Check if there's a target filename specified with #
            if '#' in file_path:
                source_path, target_name = file_path.split('#', 1)
            else:
                source_path = file_path
                # Extract just the filename from the path
                target_name = source_path.split('/')[-1]
                
            files.append({
                'source': source_path,
                'target': target_name
            })
            
        return files

    def to_tasks_and_relations(self):
        action_task = Task(
            task_id=self.name,
            template_name="shell.tpl",
            template_params=dict(
                pig_command=self.pig_command,
                action_node_properties=self.props.action_node_properties,
                action_node_path=self.props.action_node_path,
                hdfs_files=self.hdfs_files,
                new_env_vars=self.new_env_vars,
            ),
        )
        tasks = [action_task]
        relations: List[Relation] = []
        prepare_task = self.prepare_extension.get_prepare_task()
        if prepare_task:
            tasks, relations = self.prepend_task(prepare_task, tasks, relations)
        return tasks, relations

    def required_imports(self) -> Set[str]:
        return {
            "from airflow.utils import dates",
            "from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator",
            "import os",  # Added for file path handling
            "from airflow.operators.bash import BashOperator"  # Ensures BashOperator is available
        }
