"""
Transcript Tagger module.
Handles the tagging of transcript content using OpenAI API.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple, Any

from tenacity import retry, stop_after_attempt, wait_exponential

from .config import Config
from .difficulty_analyzer import DifficultyAnalyzer

logger = logging.getLogger(__name__)

class TranscriptTagger:
    """
    Tags transcript content using AI and analyzes difficulty.
    
    This class provides methods to:
    - Process transcript files and generate content tags
    - Analyze difficulty level of transcript content
    - Store and retrieve tagging results
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the transcript tagger.
        
        Args:
            config (Config, optional): Custom configuration. If None, default config is used.
        """
        self.config = config or Config()
        self.difficulty_analyzer = DifficultyAnalyzer(self.config)
        
        # Validate API key
        if not self.config.api_key:
            logger.warning("No OpenAI API key provided. Tagging functionality will be limited.")
        
        # Initialize storage directory
        self.storage_path = Path(self.config.storage_path)
        self._initialize_storage()
    
    def _initialize_storage(self):
        """Initialize the storage directory for saving tags."""
        try:
            self.storage_path.mkdir(parents=True, exist_ok=True)
            
            # Initialize tags file if it doesn't exist
            tags_file = self.storage_path / "transcript_tags.json"
            if not tags_file.exists():
                with open(tags_file, 'w', encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False, indent=2)
            
            logger.debug(f"Storage initialized at {self.storage_path}")
        except Exception as e:
            logger.error(f"Failed to initialize storage: {str(e)}")
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _call_openai_api(self, prompt: str) -> str:
        """
        Call OpenAI API with retry logic.
        
        Args:
            prompt (str): The prompt to send to OpenAI API
            
        Returns:
            str: The API response
        """
        try:
            import openai
            
            client = openai.OpenAI(api_key=self.config.api_key)
            response = client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that analyzes transcript content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        except ImportError:
            logger.error("OpenAI package not installed. Please install it with 'pip install openai'.")
            raise
        except Exception as e:
            logger.error(f"API call failed: {str(e)}")
            raise
    
    def extract_video_id(self, file_path: Union[str, Path]) -> str:
        """
        Extract video ID from file name.
        
        Args:
            file_path (str or Path): Path to the transcript file
            
        Returns:
            str: The extracted video ID
        """
        file_path = Path(file_path) if isinstance(file_path, str) else file_path
        file_name = file_path.stem
        
        # Assuming filename format is videoId_transcript.txt
        if '_transcript' in file_name:
            return file_name.split('_transcript')[0]
        
        # Fallback to using the whole filename as ID
        return file_name
    
    def analyze_tags(self, transcript_text: str) -> Dict[str, List[str]]:
        """
        Analyze transcript content and generate tags using OpenAI API.
        
        Args:
            transcript_text (str): The transcript content
            
        Returns:
            dict: Dictionary of tags by category
        """
        if not self.config.api_key:
            logger.warning("No API key provided. Cannot analyze tags.")
            return {}
        
        # Generate prompt for tag analysis
        prompt = self.config.generate_tag_prompt(transcript_text)
        
        # Call OpenAI API
        logger.info("Calling OpenAI API to analyze transcript tags...")
        response = self._call_openai_api(prompt)
        
        # Parse response to extract tags
        tags = self._parse_tag_response(response)
        
        return tags
    
    def _parse_tag_response(self, response: str) -> Dict[str, List[str]]:
        """
        Parse the API response to extract tags.
        
        Args:
            response (str): The API response
            
        Returns:
            dict: Dictionary of tags by category
        """
        tags = {}
        current_category = None
        
        # Process each line in the response
        for line in response.strip().split('\n'):
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Check if this line is a category header
            if line.endswith(':') or line.endswith('：'):
                category = line.rstrip(':：').strip()
                current_category = category
                tags[category] = []
            elif current_category is not None:
                # Handle comma-separated tags or single tag
                if ',' in line:
                    for tag in line.split(','):
                        clean_tag = tag.strip()
                        if clean_tag:
                            tags[current_category].append(clean_tag)
                else:
                    tags[current_category].append(line)
        
        return tags
    
    def analyze_difficulty(self, transcript_text: str) -> Dict[str, Any]:
        """
        Analyze the difficulty level of transcript content.
        
        Args:
            transcript_text (str): The transcript content
            
        Returns:
            dict: Difficulty analysis results
        """
        return self.difficulty_analyzer.analyze_text(transcript_text)
    
    def process_transcript(self, file_path: Union[str, Path], analyze_tags: bool = True, 
                           analyze_difficulty: bool = True) -> Dict[str, Any]:
        """
        Process a transcript file to generate tags and analyze difficulty.
        
        Args:
            file_path (str or Path): Path to the transcript file
            analyze_tags (bool): Whether to analyze tags using OpenAI API
            analyze_difficulty (bool): Whether to analyze difficulty
            
        Returns:
            dict: Dictionary containing tags and difficulty analysis
        """
        file_path = Path(file_path) if isinstance(file_path, str) else file_path
        
        if not file_path.exists():
            raise FileNotFoundError(f"Transcript file not found: {file_path}")
        
        # Read transcript
        with open(file_path, 'r', encoding='utf-8') as f:
            transcript_text = f.read()
        
        video_id = self.extract_video_id(file_path)
        logger.info(f"Processing transcript for video ID: {video_id}")
        
        result = {
            'video_id': video_id,
            'file_name': file_path.name,
            'tags': {},
            'difficulty': {}
        }
        
        # Analyze tags if requested
        if analyze_tags and self.config.api_key:
            try:
                result['tags'] = self.analyze_tags(transcript_text)
                logger.info(f"Generated tags for video ID: {video_id}")
            except Exception as e:
                logger.error(f"Failed to analyze tags: {str(e)}")
        
        # Analyze difficulty if requested
        if analyze_difficulty:
            try:
                result['difficulty'] = self.analyze_difficulty(transcript_text)
                logger.info(f"Analyzed difficulty for video ID: {video_id}")
            except Exception as e:
                logger.error(f"Failed to analyze difficulty: {str(e)}")
        
        # Save results
        self.save_results(result)
        
        return result
    
    def save_results(self, result: Dict[str, Any]) -> None:
        """
        Save tagging and difficulty analysis results to storage.
        
        Args:
            result (dict): The result dictionary
        """
        tags_file = self.storage_path / "transcript_tags.json"
        
        try:
            # Load existing data
            with open(tags_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Update with new data
            video_id = result['video_id']
            data[video_id] = result
            
            # Save back to file
            with open(tags_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Results saved for video ID: {video_id}")
        except Exception as e:
            logger.error(f"Failed to save results: {str(e)}")
            raise
    
    def get_results(self, video_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve tagging and difficulty analysis results from storage.
        
        Args:
            video_id (str, optional): If provided, get results for this video ID.
                                      If None, get all results.
            
        Returns:
            dict: Dictionary of results
        """
        tags_file = self.storage_path / "transcript_tags.json"
        
        try:
            with open(tags_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if video_id:
                return data.get(video_id, {})
            return data
        except Exception as e:
            logger.error(f"Failed to retrieve results: {str(e)}")
            return {} if video_id else {} 