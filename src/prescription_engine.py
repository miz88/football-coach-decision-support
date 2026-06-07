"""Prescription Engine Module

Core decision-making engine for generating tactical recommendations.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from src.game_state import GameState
from src.feature_engineering import GameStateFeatures


@dataclass
class Recommendation:
    """Represents a single recommendation."""
    recommendation_type: str  # 'substitution', 'formation_change', 'pressing'
    action: str  # Specific action to take
    confidence: float  # Confidence score 0-1
    rationale: str  # Why this recommendation
    supporting_data: Dict  # Data supporting the recommendation


class PrescriptionEngine:
    """Generate prescriptive recommendations based on game state."""
    
    def __init__(self):
        """Initialize the prescription engine."""
        self.recommendations_history = []
    
    def get_recommendations(self, game_state: GameState) -> List[Recommendation]:
        """Generate all applicable recommendations for current game state.
        
        Args:
            game_state: Current game state
            
        Returns:
            List of recommendations sorted by confidence
        """
        recommendations = []
        
        # Generate each type of recommendation
        substitution_recs = self._generate_substitution_recommendations(game_state)
        recommendations.extend(substitution_recs)
        
        formation_recs = self._generate_formation_recommendations(game_state)
        recommendations.extend(formation_recs)
        
        pressing_recs = self._generate_pressing_recommendations(game_state)
        recommendations.extend(pressing_recs)
        
        # Sort by confidence descending
        recommendations.sort(key=lambda x: x.confidence, reverse=True)
        
        return recommendations
    
    def _generate_substitution_recommendations(self, game_state: GameState) -> List[Recommendation]:
        """Generate substitution recommendations.
        
        Args:
            game_state: Current game state
            
        Returns:
            List of substitution recommendations
        """
        recommendations = []
        features = GameStateFeatures.get_substitution_features(game_state)
        
        # Rule 1: Fresh legs when trailing late
        if (features['score_differential'] < 0 and 
            features['match_minute'] > 70 and 
            features['match_minute'] < 85):
            
            rec = Recommendation(
                recommendation_type='substitution',
                action='Introduce offensive substitutes to push for equalizer',
                confidence=0.85,
                rationale='Trailing late in match - fresh attacking players needed',
                supporting_data={
                    'score_differential': features['score_differential'],
                    'match_minute': features['match_minute']
                }
            )
            recommendations.append(rec)
        
        # Rule 2: Defensive reinforcement when leading
        if (features['score_differential'] > 0 and 
            features['match_minute'] > 75):
            
            rec = Recommendation(
                recommendation_type='substitution',
                action='Consider defensive substitution to protect lead',
                confidence=0.70,
                rationale='Leading late - defensive stability is priority',
                supporting_data={
                    'score_differential': features['score_differential'],
                    'match_minute': features['match_minute']
                }
            )
            recommendations.append(rec)
        
        # Rule 3: Early substitution for tired players
        if features['match_minute'] > 60 and features['match_minute'] < 65:
            rec = Recommendation(
                recommendation_type='substitution',
                action='Refresh key players before fatigue affects performance',
                confidence=0.65,
                rationale='Optimal time for tactical substitutions (~65 mins)',
                supporting_data={
                    'match_minute': features['match_minute']
                }
            )
            recommendations.append(rec)
        
        return recommendations
    
    def _generate_formation_recommendations(self, game_state: GameState) -> List[Recommendation]:
        """Generate formation change recommendations.
        
        Args:
            game_state: Current game state
            
        Returns:
            List of formation recommendations
        """
        recommendations = []
        features = GameStateFeatures.get_formation_change_features(game_state)
        
        # Rule 1: Attacking formation when trailing
        if (features['score_differential'] < 0 and 
            features['match_minute'] > 60 and 
            features['match_minute'] < 80):
            
            rec = Recommendation(
                recommendation_type='formation_change',
                action='Shift to more attacking formation (add extra attacker)',
                confidence=0.80,
                rationale='Trailing by goal - need to increase attacking threat',
                supporting_data={
                    'score_differential': features['score_differential'],
                    'match_minute': features['match_minute'],
                    'possession_loss_zone': features['possession_loss_zone']
                }
            )
            recommendations.append(rec)
        
        # Rule 2: Defensive formation in early lead
        if (features['score_differential'] > 0 and 
            features['match_minute'] > 45 and 
            features['match_minute'] < 60):
            
            rec = Recommendation(
                recommendation_type='formation_change',
                action='Consolidate with defensive formation if opponent pressing',
                confidence=0.60,
                rationale='Protecting early lead - defensive stability preferred',
                supporting_data={
                    'score_differential': features['score_differential'],
                    'match_minute': features['match_minute']
                }
            )
            recommendations.append(rec)
        
        # Rule 3: Midfield control if losing possession in middle third
        if features['possession_loss_zone'] == 'midfield':
            rec = Recommendation(
                recommendation_type='formation_change',
                action='Add midfielder to control possession in midfield',
                confidence=0.75,
                rationale='Losing possession battles in midfield',
                supporting_data={
                    'possession_loss_zone': features['possession_loss_zone']
                }
            )
            recommendations.append(rec)
        
        return recommendations
    
    def _generate_pressing_recommendations(self, game_state: GameState) -> List[Recommendation]:
        """Generate pressing intensity recommendations.
        
        Args:
            game_state: Current game state
            
        Returns:
            List of pressing recommendations
        """
        recommendations = []
        features = GameStateFeatures.get_pressing_features(game_state)
        
        # Rule 1: High press when winning
        if (features['score_differential'] > 0 and 
            features['match_minute'] < 60):
            
            rec = Recommendation(
                recommendation_type='pressing',
                action='Maintain high pressing intensity - control the game',
                confidence=0.70,
                rationale='Winning position - press to prevent comeback',
                supporting_data={
                    'score_differential': features['score_differential'],
                    'match_minute': features['match_minute']
                }
            )
            recommendations.append(rec)
        
        # Rule 2: Increase pressing in midfield if losing there
        if (features['possession_loss_zone'] == 'midfield' and 
            features['recent_possession_losses'] > 3):
            
            rec = Recommendation(
                recommendation_type='pressing',
                action='Increase pressing intensity in midfield',
                confidence=0.75,
                rationale='Multiple possession losses in midfield - press higher',
                supporting_data={
                    'possession_loss_zone': features['possession_loss_zone'],
                    'recent_possession_losses': features['recent_possession_losses']
                }
            )
            recommendations.append(rec)
        
        # Rule 3: Drop defensive line when trailing
        if (features['score_differential'] < 0 and 
            features['match_minute'] > 70):
            
            rec = Recommendation(
                recommendation_type='pressing',
                action='Lower pressing intensity - defend deep and counter',
                confidence=0.65,
                rationale='Trailing late - counter-attacking approach',
                supporting_data={
                    'score_differential': features['score_differential'],
                    'match_minute': features['match_minute']
                }
            )
            recommendations.append(rec)
        
        return recommendations
    
    def find_similar_historical_situations(self, game_state: GameState, 
                                           historical_games: List[Dict]) -> List[Dict]:
        """Find similar historical game situations for case-based reasoning.
        
        Args:
            game_state: Current game state
            historical_games: List of historical game data
            
        Returns:
            List of similar situations with recommendations made then
        """
        similar_situations = []
        
        for game in historical_games:
            # Simple similarity based on score differential and match time
            score_diff = abs(game.get('score_differential', 0) - game_state.score_differential)
            time_diff = abs(game.get('match_minute', 0) - game_state.match_minute)
            
            # Similar if within 1 goal and 5 minutes
            if score_diff <= 1 and time_diff <= 5:
                similar_situations.append(game)
        
        return similar_situations
