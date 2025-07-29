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

"""Extractors for configuration and job-xml nodes"""
import os
from os import path
from typing import Dict, List
import xml.etree.ElementTree as ET
import logging

from o2a.converter.constants import HDFS_FOLDER
from o2a.converter.exceptions import ParseException
from o2a.o2a_libs.src.o2a_lib import el_parser

TAG_CONFIGURATION = "configuration"
TAG_PROPERTY = "property"
TAG_NAME = "name"
TAG_VALUE = "value"
TAG_JOB_XML = "job-xml"


def extract_properties_from_configuration_node(config_node: ET.Element) -> Dict[str, str]:
    """Extracts configuration properties from ``configuration`` node"""
    properties_dict: Dict[str, str] = dict()
    for property_node in config_node.findall(TAG_PROPERTY):
        name_node = property_node.find(TAG_NAME)
        value_node = property_node.find(TAG_VALUE)

        # Check if name_node and value_node exist
        if name_node is None or value_node is None:
            logging.warning('Element "property" should have direct children elements: name, value. One of them does not exist. Skipping this property.')
            continue  # Skip this property if either name or value is missing

        name = name_node.text
        value = value_node.text

        # Log debug information
        logging.debug(f"name_node: {name}, value_node: {value}")

        # Only add to properties_dict if name and value are not None or empty
        if name and value:
            properties_dict[name] = el_parser.translate(value)
        else:
            logging.warning(f"Skipping property with name: {name} and value: {value} because one of them is empty.")



    return properties_dict


def extract_properties_from_job_xml_nodes(job_xml_nodes: List[ET.Element], input_directory_path: str):
    """Extracts configuration properties from ``job_xml`` nodes"""
    properties_dict: Dict[str, str] = dict()

    for xml_file in job_xml_nodes:
        file_name = xml_file.text
        logging.info(f"file_name: {file_name}")
        if not file_name:
            raise ParseException(
                'Element "job-xml" should have content, however its value is empty. Make sure the element '
                "has the correct content."
            )
        file_path = path.join(file_name)
        if file_path.startswith("hdfs://"):
            # Use hdfs dfs -get to fetch the file locally
            local_tmp_file = "/tmp/job_xml_tmp.xml"
            os.system(f"rm -rf {local_tmp_file} && hdfs dfs -get {file_path} {local_tmp_file}")
            file_path = local_tmp_file
        
        config_tree = ET.parse(file_path)
        #print(f"file_path: {file_path}")
        #print(f"config_tree: {config_tree}")
        #print(f"config_tree XML content:\n{ET.tostring(config_tree.getroot(), encoding='unicode')}")

        config_node = config_tree.getroot()
        if not config_node:
            raise ParseException(
                "A job-xml configuration node is specified in the workflow XML, however its value is empty."
                "Make sure the path to a configuration file is valid."
            )
        new_properties = extract_properties_from_configuration_node(config_node)
        properties_dict.update(new_properties)

    return properties_dict
