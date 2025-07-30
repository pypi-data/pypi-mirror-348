"""
Difficulty Analyzer module.
Analyzes the difficulty level of transcript content based on various metrics.
"""

import re
import logging
import statistics
from pathlib import Path
from typing import Dict, Any, List, Union, Optional, Tuple

import textstat
from wordfreq import word_frequency

from .config import Config

logger = logging.getLogger(__name__)

class DifficultyAnalyzer:
    """
    Analyzes and rates the difficulty level of transcript content.
    
    This class provides methods to analyze various aspects of text difficulty:
    - Word frequency analysis
    - Sentence complexity
    - Readability metrics
    - Overall difficulty rating
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the difficulty analyzer.
        
        Args:
            config (Config, optional): Custom configuration. If None, default config is used.
        """
        self.config = config or Config()
    
    def count_words(self, text: str) -> int:
        """
        Count the number of words in a text.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            int: The word count
        """
        # Split by whitespace and filter out empty strings
        words = [word for word in re.split(r'\s+', text) if word]
        return len(words)
    
    def count_sentences(self, text: str) -> int:
        """
        Count the number of sentences in a text.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            int: The sentence count
        """
        # Basic sentence splitting based on period, question mark, and exclamation mark
        # This is a simplified approach; more sophisticated NLP might be needed for complex texts
        sentences = re.split(r'[.!?]+', text)
        # Filter out empty strings
        sentences = [s.strip() for s in sentences if s.strip()]
        return len(sentences)
    
    def average_word_length(self, text: str) -> float:
        """
        Calculate the average word length in a text.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            float: The average word length
        """
        # Clean text and split into words
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        if not words:
            return 0
        
        total_length = sum(len(word) for word in words)
        return total_length / len(words)
    
    def average_sentence_length(self, text: str) -> float:
        """
        Calculate the average sentence length (in words) in a text.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            float: The average sentence length in words
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0
        
        words_per_sentence = [self.count_words(sentence) for sentence in sentences]
        return sum(words_per_sentence) / len(sentences)
    
    def calculate_word_frequency_score(self, text: str) -> float:
        """
        Calculate the proportion of infrequent words in the text.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            float: The proportion of infrequent words (0-1)
        """
        # Clean text and get unique words
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        if not words:
            return 0
        
        # Consider a word "infrequent" if its frequency is below a threshold
        # Lower frequencies indicate harder words
        infrequent_threshold = 1e-5  # Adjust this threshold as needed
        infrequent_words = [word for word in words if word_frequency(word, 'en') < infrequent_threshold]
        
        return len(infrequent_words) / len(words)
    
    def calculate_readability_metrics(self, text: str) -> Dict[str, float]:
        """
        Calculate various readability metrics for the text.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            dict: Dictionary of readability metrics
        """
        metrics = {
            'flesch_reading_ease': textstat.flesch_reading_ease(text),
            'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text),
            'gunning_fog': textstat.gunning_fog(text),
            'smog_index': textstat.smog_index(text),
            'coleman_liau_index': textstat.coleman_liau_index(text),
            'automated_readability_index': textstat.automated_readability_index(text),
            'dale_chall_readability_score': textstat.dale_chall_readability_score(text),
        }
        
        return metrics
    
    def determine_difficulty_level(self, metrics: Dict[str, Any]) -> Tuple[int, str, Dict[str, Any]]:
        """
        Determine the content difficulty level based on the calculated metrics.
        
        Args:
            metrics (dict): Dictionary of text metrics
            
        Returns:
            tuple: (difficulty_level_number, difficulty_level_name, detailed_metrics)
        """
        # Extract key metrics
        fk_grade = metrics['readability']['flesch_kincaid_grade']
        infrequent_words_ratio = metrics['word_frequency_score']
        avg_sentence_length = metrics['avg_sentence_length']
        
        # Calculate individual scores based on thresholds
        readability_score = 0
        for level_name, threshold in self.config.readability_thresholds.items():
            if fk_grade <= threshold:
                readability_score = list(self.config.readability_thresholds.keys()).index(level_name) + 1
                break
        else:
            # If above all thresholds, assign the highest level
            readability_score = 5
        
        word_freq_score = 0
        for level_name, threshold in self.config.word_frequency_thresholds.items():
            if infrequent_words_ratio <= threshold:
                word_freq_score = list(self.config.word_frequency_thresholds.keys()).index(level_name) + 1
                break
        else:
            # If above all thresholds, assign the highest level
            word_freq_score = 5
        
        sentence_complexity_score = 0
        for level_name, threshold in self.config.sentence_complexity_thresholds.items():
            if avg_sentence_length <= threshold:
                sentence_complexity_score = list(self.config.sentence_complexity_thresholds.keys()).index(level_name) + 1
                break
        else:
            # If above all thresholds, assign the highest level
            sentence_complexity_score = 5
        
        # Calculate the final score as a weighted average
        # Weight the components according to their importance in determining difficulty
        weights = {
            'readability': 0.5,        # Readability metrics are most important
            'word_freq': 0.3,          # Word frequency is next most important
            'sentence_complexity': 0.2  # Sentence complexity is least important
        }
        
        weighted_score = (
            readability_score * weights['readability'] +
            word_freq_score * weights['word_freq'] +
            sentence_complexity_score * weights['sentence_complexity']
        )
        
        # Round to nearest integer and ensure it's within the valid range
        final_score = min(max(round(weighted_score), 1), 5)
        
        # Create a detailed breakdown of the metrics for reference
        difficulty_breakdown = {
            'readability_level': readability_score,
            'word_frequency_level': word_freq_score, 
            'sentence_complexity_level': sentence_complexity_score,
            'weighted_score': weighted_score,
            'final_score': final_score
        }
        
        return final_score, self.config.difficulty_levels[final_score], difficulty_breakdown
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze the difficulty level of a text.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            dict: Dictionary containing difficulty metrics and level
        """
        logger.info("Analyzing text difficulty...")
        
        # Basic text metrics
        word_count = self.count_words(text)
        sentence_count = self.count_sentences(text)
        avg_word_len = self.average_word_length(text)
        avg_sent_len = self.average_sentence_length(text)
        word_freq_score = self.calculate_word_frequency_score(text)
        
        # Readability metrics
        readability = self.calculate_readability_metrics(text)
        
        # Compile all metrics
        metrics = {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_word_length': avg_word_len,
            'avg_sentence_length': avg_sent_len,
            'word_frequency_score': word_freq_score,
            'readability': readability
        }
        
        # Determine difficulty level
        level_num, level_name, level_breakdown = self.determine_difficulty_level(metrics)
        
        # Create the result dictionary
        result = {
            'metrics': metrics,
            'difficulty_level': level_num,
            'difficulty_name': level_name,
            'difficulty_breakdown': level_breakdown
        }
        
        logger.info(f"Text analyzed. Difficulty level: {level_name} ({level_num}/5)")
        return result
    
    def analyze_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Analyze the difficulty level of a transcript file.
        
        Args:
            file_path (str or Path): Path to the transcript file
            
        Returns:
            dict: Difficulty analysis results
        """
        try:
            file_path = Path(file_path) if isinstance(file_path, str) else file_path
            
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            logger.info(f"Analyzing difficulty for transcript: {file_path.name}")
            return self.analyze_text(text)
        except Exception as e:
            logger.error(f"Error analyzing transcript difficulty: {str(e)}")
            raise 