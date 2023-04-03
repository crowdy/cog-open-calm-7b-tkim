from argparse import ArgumentParser
import os
import stat
from jinja2 import Template

# Flan configs, can modify as 
CONFIGS = {
    "flan-t5-small": {
        "cog_yaml_parameters": {"predictor":"predict.py:Predictor"},
        "config_py_parameters": {"model_name": "google/flan-t5-small"}
    },
    "flan-t5-base": {
        "cog_yaml_parameters": {"predictor":"predict.py:Predictor"},
        "config_py_parameters": {"model_name": "google/flan-t5-base"}
    },
    "flan-t5-large": {
        "cog_yaml_parameters": {"predictor":"predict.py:Predictor"},
        "config_py_parameters": {"model_name": "google/flan-t5-large"}
    },
    "flan-t5-xl": {
        "cog_yaml_parameters": {"predictor":"predict.py:Predictor"},
        "config_py_parameters": {"model_name": "google/flan-t5-xl"}
    },
    "flan-t5-xxl": {
        "cog_yaml_parameters": {"predictor":"predict.py:Predictor"},
        "config_py_parameters": {"model_name": "google/flan-t5-xxl"}
    },
    "flan-ul2": {
        "cog_yaml_parameters": {"predictor":"predict.py:EightBitPredictor", "extra_deps":'''- "bitsandbytes==0.37.2"'''},
        "config_py_parameters": {"model_name": "google/flan-ul2"}
    }
}

def _reset_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def write_one_config(template_fpath: str, fname_out: str, config: dict):
    with open(template_fpath, "r") as f:
        template_content = f.read()
        base_template = Template(template_content)

    _reset_file(fname_out)

    with open(fname_out, "w") as f:
        f.write(base_template.render(config))

    # Give all users write access to resulting generated file. 
    current_permissions = os.stat(fname_out).st_mode
    new_permissions = current_permissions | stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH
    os.chmod(fname_out, new_permissions)


def write_configs(model_name):
    master_config = CONFIGS[model_name]
    write_one_config("templates/cog_template.yaml", "cog.yaml", master_config['cog_yaml_parameters'])
    write_one_config("templates/config_template.py", "config.py", master_config['config_py_parameters'])

    
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--model_name", default="base", help="name of the flan-t5 model you want to configure cog for")
    args = parser.parse_args()

    write_configs(args.model_name)