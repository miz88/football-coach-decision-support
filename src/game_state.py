"""Game State Representation Module

Represents the current state of a football match for decision-making.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import pandas as pd
import numpy as np


@dataclass
class Team:
    """Represents a team in the game."""
    team_id: int
    name: str
    formation: Optional[str] = None
    score: int = 0
    possession: float = 0.0


@dataclass
class Player:
    """Represents a player in the game."""
    player_id: int
    name: str
    team_id: int
    position: Optional[str] = None
    minutes_played: int = 0
    pass_completion: float = 0.0
    pass_count: int = 0
    errors: int = 0
    is_on_field: bool = True


@dataclass
class GameState:
    """Represents the complete state of a football match."""
    
    match_id: int
    match_time: int
    home_team: Team
    away_team: Team
    possession_team_id: int
    pressing_intensity: str = "medium"
    recent_possession_losses: List[tuple] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate game state after initialization."""
        if self.match_time < 0:
            raise ValueError("Match time cannot be negative")
    
    @property
    def match_minute(self) -> float:
        """Get match time in minutes."""
        return self.match_time / 60.0
    
    @property
    def score_differential(self) -> int:
        """Get score differential (home - away)."""
        return self.home_team.score - self.away_team.score
    
    @property
    def possession_team(self) -> Team:
        """Get the team currently in possession."""
        if self.possession_team_id == self.home_team.team_id:
            return self.home_team
        return self.away_team
    
    @property
    def defending_team(self) -> Team:
        """Get the team currently defending."""
        if self.possession_team_id == self.home_team.team_id:
            return self.away_team
        return self.home_team
    
    def get_possession_loss_zone(self) -> Optional[str]:
        """Determine the primary zone where possession is being lost.
        
        Returns:
            Zone name: 'defensive', 'midfield', 'attacking', or None
        """
        if not self.recent_possession_losses:
            return None
        
        avg_x = np.mean([loss[0] for loss in self.recent_possession_losses])
        
        if avg_x < 40:
            return "defensive"
        elif avg_x < 80:
            return "midfield"
        else:
            return "attacking"
    
    def to_dict(self) -> Dict:
        """Convert game state to dictionary."""
        return {
            'match_id': self.match_id,
            'match_time': self.match_time,
            'match_minute': self.match_minute,
            'home_team_score': self.home_team.score,
            'away_team_score': self.away_team.score,
            'score_differential': self.score_differential,
            'possession_team': self.possession_team.name,
            'possession_loss_zone': self.get_possession_loss_zone()
        }
