# prompts/prompt_manager.py
import yaml
from typing import Dict, Any

class PromptTemplate:
    def __init__(self, template: str):
        self.template = template

    def format(self, **kwargs: Any) -> str:
        return self.template.format(**kwargs)

class PromptCategory:
    def __init__(self, system: str, user: str):
        self.system = PromptTemplate(system)
        self.user = PromptTemplate(user)

class Prompts:
    retrieval: PromptCategory
    generation: PromptCategory
    meta_data_enhancement: PromptCategory

    def __init__(self, yaml_file: str):
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)
        
        for category, prompts in data.items():
            if 'system' not in prompts or 'user' not in prompts:
                raise ValueError(f"Invalid format for category {category}")
            setattr(self, category, PromptCategory(
                system=prompts['system'],
                user=prompts['user']
            ))

    def __getattr__(self, name: str) -> PromptCategory:
        raise AttributeError(f"Prompt category '{name}' not found")