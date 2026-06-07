# Football Coach Decision Support System

## Project Overview

A **prescriptive decision support system** that provides real-time tactical recommendations to football coaches during matches. This proof-of-concept uses open StatsBomb data to analyze game situations and recommend:

- **Substitutions** - Optimal player changes based on performance and game state
- **Formation Changes** - Tactical adjustments based on match dynamics
- **Pressing Tactics** - Intensity and positioning recommendations based on possession loss patterns

## Academic Context

- **Framework**: CRISP-DM (Cross-Industry Standard Process for Data Mining)
- **Data Source**: StatsBomb Open Data
- **Type**: Proof of Concept for academic research
- **Language**: Python

## Project Structure

```
football-coach-decision-support/
├── README.md                          # This file
├── METHODOLOGY.md                     # Detailed CRISP-DM methodology
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore patterns
│
├── data/
│   ├── raw/                          # Raw StatsBomb data
│   ├── processed/                    # Cleaned and engineered features
│   └── rules/                        # Prescription rules (JSON/YAML)
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py               # StatsBomb data loading utilities
│   ├── game_state.py                # Game state representation
│   ├── feature_engineering.py       # Feature extraction and engineering
│   ├── prescription_engine.py       # Core decision recommendation engine
│   ├── rules_manager.py             # Rule loading and management
│   └── utils.py                     # Helper functions
│
├── notebooks/
│   ├── 01_data_exploration.ipynb    # Exploratory data analysis
│   ├── 02_feature_engineering.ipynb # Feature development
│   ├── 03_rule_development.ipynb    # Prescription rule development
│   └── 04_proof_of_concept.ipynb    # PoC demonstration
│
└── tests/
    ├── __init__.py
    ├── test_data_loader.py
    ├── test_game_state.py
    └── test_prescription_engine.py
```

## CRISP-DM Phases

### 1. Business Understanding
Define the coach's decision-making needs during matches and identify high-impact tactical decisions.

### 2. Data Understanding
Analyze StatsBomb open data structure, event types, and available information for decision-making.

### 3. Data Preparation
Clean, normalize, and engineer features to represent game situations for prescriptive analysis.

### 4. Modeling
Develop prescription rules based on domain expertise and data patterns to recommend actions.

### 5. Evaluation
Validate recommendations against expert judgment and historical outcomes.

### 6. Deployment
Create interface for real-time game situation analysis and recommendation delivery.

## Installation

```bash
# Clone the repository
git clone https://github.com/miz88/football-coach-decision-support.git
cd football-coach-decision-support

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```python
from src.data_loader import StatsBombLoader
from src.game_state import GameState
from src.prescription_engine import PrescriptionEngine

# Load StatsBomb data
loader = StatsBombLoader()
matches = loader.load_matches(competition_id=11)  # Euro 2020

# Analyze a specific match
match_id = matches[0]['match_id']
events = loader.load_events(match_id)

# Create game state at specific moment
game_state = GameState(match_id, events, timestamp=45*60)

# Get recommendations
engine = PrescriptionEngine()
recommendations = engine.get_recommendations(game_state)

print(recommendations)
```

## Key Features

### Game State Representation
- Current score and time
- Possession patterns
- Player positions and fatigue
- Recent possession loss locations
- Formation detection
- Pressure events

### Prescription Engine
- Rule-based recommendations
- Case-based reasoning (similar historical situations)
- Multi-criteria decision analysis
- Confidence scoring

### Recommendation Types
1. **Substitutions**: Based on player performance, fatigue, and game needs
2. **Formation Changes**: Tactical adjustments for offensive/defensive balance
3. **Pressing Tactics**: Intensity recommendations based on loss patterns

## Dependencies

- `statsbomb` - StatsBomb API client
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `matplotlib`, `seaborn` - Visualization
- `json` - Configuration management
- `pytest` - Testing

See `requirements.txt` for full list.

## Usage

See individual module documentation and notebooks for detailed usage examples.

## Contributing

This is an academic proof-of-concept project. Contributions and improvements welcome!

## License

MIT License - See LICENSE file for details

## Authors

- miz88

## References

- StatsBomb Open Data: https://github.com/statsbomb/open-data
- CRISP-DM Framework: https://www.ibm.com/cloud/learn/crisp-dm
- Football Analytics Resources: https://www.americanfootballanalysis.com/
