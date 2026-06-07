"""Rules Manager Module

Loads and manages prescription rules from configuration files.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional


class RulesManager:
    """Manages prescription rules from configuration."""
    
    def __init__(self, rules_dir: str = "data/rules"):
        """Initialize rules manager.
        
        Args:
            rules_dir: Directory containing rule files
        """
        self.rules_dir = Path(rules_dir)
        self.rules_dir.mkdir(parents=True, exist_ok=True)
        self.rules = {}
    
    def load_rules(self, rule_type: str) -> Dict:
        """Load rules for a specific type.
        
        Args:
            rule_type: Type of rules ('substitution', 'formation', 'pressing')
            
        Returns:
            Dictionary of rules
        """
        json_path = self.rules_dir / f"{rule_type}_rules.json"
        yaml_path = self.rules_dir / f"{rule_type}_rules.yaml"
        
        if json_path.exists():
            with open(json_path, 'r') as f:
                self.rules[rule_type] = json.load(f)
        elif yaml_path.exists():
            with open(yaml_path, 'r') as f:
                self.rules[rule_type] = yaml.safe_load(f)
        else:
            self.rules[rule_type] = {}
        
        return self.rules.get(rule_type, {})
    
    def get_rule(self, rule_type: str, rule_id: str) -> Optional[Dict]:
        """Get a specific rule.
        
        Args:
            rule_type: Type of rule
            rule_id: Rule identifier
            
        Returns:
            Rule dictionary or None
        """
        if rule_type not in self.rules:
            self.load_rules(rule_type)
        
        return self.rules.get(rule_type, {}).get(rule_id)
    
    def save_rules(self, rule_type: str, rules: Dict, format: str = 'json'):
        """Save rules to file.
        
        Args:
            rule_type: Type of rules
            rules: Dictionary of rules
            format: File format ('json' or 'yaml')
        """
        if format == 'json':
            path = self.rules_dir / f"{rule_type}_rules.json"
            with open(path, 'w') as f:
                json.dump(rules, f, indent=2)
        elif format == 'yaml':
            path = self.rules_dir / f"{rule_type}_rules.yaml"
            with open(path, 'w') as f:
                yaml.dump(rules, f, default_flow_style=False)
        
        self.rules[rule_type] = rules
