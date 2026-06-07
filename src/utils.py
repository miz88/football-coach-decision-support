"""Utility Functions

Helper functions for the prescription system.
"""

from typing import Dict, List
import math


def calculate_pitch_zone(x: float, y: float) -> str:
    """Calculate which zone of pitch a coordinate is in.
    
    Pitch dimensions: 0-120 (x), 0-80 (y)
    Zones: defensive, midfield, attacking (by x)
           left, center, right (by y)
    
    Args:
        x: X coordinate (0-120)
        y: Y coordinate (0-80)
        
    Returns:
        Zone name
    """
    x_zone = "defensive" if x < 40 else "midfield" if x < 80 else "attacking"
    y_zone = "left" if y < 26.67 else "center" if y < 53.33 else "right"
    
    return f"{x_zone}_{y_zone}"


def distance_to_goal(x: float, y: float, team: str = "home") -> float:
    """Calculate distance from coordinate to goal.
    
    Args:
        x: X coordinate
        y: Y coordinate
        team: "home" or "away"
        
    Returns:
        Distance in pitch units
    """
    goal_x = 120 if team == "away" else 0
    goal_y = 40
    
    dx = x - goal_x
    dy = y - goal_y
    
    return math.sqrt(dx**2 + dy**2)


def calculate_match_phase(match_minute: float) -> str:
    """Determine match phase.
    
    Args:
        match_minute: Current match minute
        
    Returns:
        Phase name
    """
    if match_minute < 15:
        return "early_game"
    elif match_minute < 30:
        return "opening_phase"
    elif match_minute < 45:
        return "first_half_closing"
    elif match_minute < 60:
        return "second_half_opening"
    elif match_minute < 75:
        return "midgame_phase"
    elif match_minute < 85:
        return "final_push"
    else:
        return "injury_time"


def format_recommendation(recommendation) -> str:
    """Format recommendation for display.
    
    Args:
        recommendation: Recommendation object
        
    Returns:
        Formatted string
    """
    return f"""
=== TACTICAL RECOMMENDATION ===
Type: {recommendation.recommendation_type.upper()}
Action: {recommendation.action}
Confidence: {recommendation.confidence:.0%}
Rationale: {recommendation.rationale}
"""
