"""Feature Engineering Module

Extracts and engineers features from raw events for prescriptive analysis.
"""

from typing import Dict, List
import pandas as pd
from src.game_state import GameState


class FeatureExtractor:
    """Extract features from game events and state."""
    
    @staticmethod
    def extract_player_stats(events_df: pd.DataFrame, player_id: int, team_id: int) -> Dict:
        """Extract player statistics from events.
        
        Args:
            events_df: DataFrame with event data
            player_id: Player ID to extract stats for
            team_id: Team ID
            
        Returns:
            Dictionary with player statistics
        """
        player_events = events_df[
            (events_df['player'].apply(lambda x: x.get('id') if isinstance(x, dict) else None) == player_id) &
            (events_df['team'].apply(lambda x: x.get('id') if isinstance(x, dict) else None) == team_id)
        ]
        
        stats = {
            'player_id': player_id,
            'team_id': team_id,
            'total_events': len(player_events),
            'passes': 0,
            'pass_completion': 0.0,
            'errors': 0,
            'dispossessed': 0
        }
        
        for _, event in player_events.iterrows():
            event_type = event['type'].get('name') if isinstance(event['type'], dict) else event['type']
            
            if event_type == 'Pass':
                stats['passes'] += 1
                if event.get('pass', {}).get('outcome') is None:
                    stats['pass_completion'] += 1
            elif event_type == 'Error':
                stats['errors'] += 1
            elif event_type == 'Dispossessed':
                stats['dispossessed'] += 1
        
        if stats['passes'] > 0:
            stats['pass_completion'] = stats['pass_completion'] / stats['passes']
        
        return stats
    
    @staticmethod
    def extract_team_stats(events_df: pd.DataFrame, team_id: int) -> Dict:
        """Extract team statistics.
        
        Args:
            events_df: DataFrame with event data
            team_id: Team ID
            
        Returns:
            Dictionary with team statistics
        """
        team_events = events_df[
            events_df['team'].apply(lambda x: x.get('id') if isinstance(x, dict) else None) == team_id
        ]
        
        stats = {
            'team_id': team_id,
            'total_events': len(team_events),
            'passes': 0,
            'shot_attempts': 0,
            'possession_losses': 0
        }
        
        for _, event in team_events.iterrows():
            event_type = event['type'].get('name') if isinstance(event['type'], dict) else event['type']
            
            if event_type == 'Pass':
                stats['passes'] += 1
            elif event_type == 'Shot':
                stats['shot_attempts'] += 1
            elif event_type == 'Dispossessed':
                stats['possession_losses'] += 1
        
        return stats


class GameStateFeatures:
    """Extract features from a GameState object for prescriptive rules."""
    
    @staticmethod
    def get_substitution_features(game_state: GameState) -> Dict:
        """Extract features relevant to substitution decisions.
        
        Args:
            game_state: Current game state
            
        Returns:
            Dictionary with substitution-relevant features
        """
        return {
            'match_time': game_state.match_time,
            'match_minute': game_state.match_minute,
            'score_differential': game_state.score_differential,
            'pressing_intensity': game_state.pressing_intensity,
            'possession_team': game_state.possession_team.name
        }
    
    @staticmethod
    def get_formation_change_features(game_state: GameState) -> Dict:
        """Extract features relevant to formation change decisions.
        
        Args:
            game_state: Current game state
            
        Returns:
            Dictionary with formation-relevant features
        """
        return {
            'match_time': game_state.match_time,
            'match_minute': game_state.match_minute,
            'score_differential': game_state.score_differential,
            'possession_loss_zone': game_state.get_possession_loss_zone(),
            'pressing_intensity': game_state.pressing_intensity,
            'home_formation': game_state.home_team.formation,
            'away_formation': game_state.away_team.formation
        }
    
    @staticmethod
    def get_pressing_features(game_state: GameState) -> Dict:
        """Extract features relevant to pressing intensity decisions.
        
        Args:
            game_state: Current game state
            
        Returns:
            Dictionary with pressing-relevant features
        """
        return {
            'match_time': game_state.match_time,
            'match_minute': game_state.match_minute,
            'score_differential': game_state.score_differential,
            'possession_loss_zone': game_state.get_possession_loss_zone(),
            'current_pressing_intensity': game_state.pressing_intensity,
            'defending_team': game_state.defending_team.name,
            'recent_possession_losses': len(game_state.recent_possession_losses)
        }
