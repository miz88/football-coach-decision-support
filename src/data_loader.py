"""StatsBomb Data Loading Module

Handles loading and basic processing of StatsBomb open data.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd
import requests


class StatsBombLoader:
    """Load and process StatsBomb open data."""
    
    BASE_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
    
    def __init__(self, data_dir: Optional[str] = None):
        """Initialize StatsBomb loader.
        
        Args:
            data_dir: Directory to cache downloaded data. Defaults to 'data/raw'
        """
        self.data_dir = Path(data_dir or "data/raw")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.competitions = None
        self.matches_cache = {}
        self.events_cache = {}
    
    def load_competitions(self) -> pd.DataFrame:
        """Load all available competitions.
        
        Returns:
            DataFrame with competition information
        """
        if self.competitions is not None:
            return self.competitions
        
        url = f"{self.BASE_URL}/competitions.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            self.competitions = pd.DataFrame(data)
            return self.competitions
        except Exception as e:
            raise RuntimeError(f"Failed to load competitions: {e}")
    
    def load_matches(self, competition_id: int, season_id: Optional[int] = None) -> List[Dict]:
        """Load matches for a specific competition.
        
        Args:
            competition_id: StatsBomb competition ID
            season_id: Optional season ID filter
            
        Returns:
            List of match dictionaries
        """
        cache_key = f"{competition_id}_{season_id}"
        if cache_key in self.matches_cache:
            return self.matches_cache[cache_key]
        
        url = f"{self.BASE_URL}/matches/{competition_id}.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if season_id is not None:
                data = [m for m in data if m.get('season', {}).get('season_id') == season_id]
            
            self.matches_cache[cache_key] = data
            return data
        except Exception as e:
            raise RuntimeError(f"Failed to load matches: {e}")
    
    def load_events(self, match_id: int) -> pd.DataFrame:
        """Load events for a specific match.
        
        Args:
            match_id: StatsBomb match ID
            
        Returns:
            DataFrame with event information
        """
        if match_id in self.events_cache:
            return self.events_cache[match_id]
        
        url = f"{self.BASE_URL}/events/{match_id}.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            df = pd.json_normalize(data)
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            self.events_cache[match_id] = df
            return df
        except Exception as e:
            raise RuntimeError(f"Failed to load events for match {match_id}: {e}")
    
    def get_match_info(self, match_id: int) -> Dict:
        """Get detailed information about a match."""
        competitions = self.load_competitions()
        
        for comp_id in competitions['competition_id'].unique():
            matches = self.load_matches(comp_id)
            for match in matches:
                if match['match_id'] == match_id:
                    return match
        
        raise ValueError(f"Match {match_id} not found")
