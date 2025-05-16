import yaml
import os

def load_rules(rule_dir="sast_engine/rules"):
    rules = []
    for file in os.listdir(rule_dir):
        if file.endswith(".yaml"):
            with open(os.path.join(rule_dir, file), 'r') as f:
                rule = yaml.safe_load(f)
                rules.append(rule)
    return rules
