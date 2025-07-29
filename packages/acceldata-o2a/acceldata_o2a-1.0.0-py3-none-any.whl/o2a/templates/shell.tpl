{#
  Copyright 2019 Google LLC

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
#}
{% import "macros/props.tpl" as props_macro %}
{{ task_id | to_var }} = bash.BashOperator(
    task_id={{ task_id | to_python }},
    trigger_rule={{ trigger_rule | to_python }},
    bash_command="""
    {%- if hdfs_files %}
    # Copy files from HDFS to local working directory
    {% for file in hdfs_files %}
    hdfs dfs -get {{ file.source }} {{ file.target }} || exit 1
    chmod +x {{ file.target }} || echo "Warning: Could not make {{ file.target }} executable"
    {% endfor %}
    {% endif %}
    
    # Execute the shell command
    {{ pig_command }}
    """,
    {% if new_env_vars %}env={{ new_env_vars | to_python }},
    append_env=True,
    {% endif %}
    params={{ props_macro.props(action_node_properties=action_node_properties, action_node_path=action_node_path) }},
)
