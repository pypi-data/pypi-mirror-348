#!/usr/bin/env python3
"""
Advanced example of using the Transcript Tagger SDK.
Shows custom configuration and batch processing.
"""

import os
import logging
import glob
from pathlib import Path
from typing import Dict, Any

from transcript_tagger_sdk import TranscriptTagger, Config, DifficultyAnalyzer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def create_custom_config() -> Config:
    """Create a custom configuration with adjusted thresholds."""
    config = Config()
    
    # Set API key from environment variable
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        config.set_api_key(api_key)
    
    # Use a more advanced model for better results
    config.set_model("gpt-4")
    
    # Custom storage path
    config.set_storage_path("./advanced_results")
    
    # Custom readability thresholds
    config.set_readability_thresholds({
        "初级/Beginner": 3.0,       # 0-3.0
        "初中级/Elementary": 6.0,    # 3.1-6.0
        "中级/Intermediate": 9.0,    # 6.1-9.0
        "中高级/Upper-Intermediate": 12.0,  # 9.1-12.0
        "高级/Advanced": 15.0,       # 12.1-15.0
    })
    
    # Custom word frequency thresholds
    config.set_word_frequency_thresholds({
        "初级/Beginner": 0.03,       # 0-3%
        "初中级/Elementary": 0.05,    # 3.1-5%
        "中级/Intermediate": 0.08,    # 5.1-8%
        "中高级/Upper-Intermediate": 0.10,  # 8.1-10%
        "高级/Advanced": 0.15,        # 10.1-15%
    })
    
    return config

def process_directory(tagger: TranscriptTagger, directory: str) -> Dict[str, Any]:
    """
    Process all transcript files in a directory.
    
    Args:
        tagger: The TranscriptTagger instance
        directory: Directory containing transcript files
        
    Returns:
        dict: Summary of results
    """
    # Get all .txt files in the directory
    transcript_files = glob.glob(f"{directory}/*.txt")
    
    if not transcript_files:
        logging.warning(f"No transcript files found in {directory}")
        return {}
    
    logging.info(f"Found {len(transcript_files)} transcript files to process")
    
    results = {}
    for file_path in transcript_files:
        try:
            path = Path(file_path)
            logging.info(f"Processing {path.name}...")
            
            # Process transcript
            result = tagger.process_transcript(path)
            
            # Store result summary
            video_id = result['video_id']
            results[video_id] = {
                'file_name': path.name,
                'difficulty_level': result.get('difficulty', {}).get('difficulty_level'),
                'difficulty_name': result.get('difficulty', {}).get('difficulty_name'),
                'tag_count': sum(len(tags) for tags in result.get('tags', {}).values())
            }
        except Exception as e:
            logging.error(f"Error processing {file_path}: {str(e)}")
    
    return results

def analyze_results(results: Dict[str, Dict[str, Any]]) -> None:
    """
    Analyze and display summary of processing results.
    
    Args:
        results: Dictionary of processing results
    """
    if not results:
        print("No results to analyze.")
        return
    
    print("\n===== Processing Summary =====")
    print(f"Total files processed: {len(results)}")
    
    # Count by difficulty level
    difficulty_counts = {}
    for video_id, data in results.items():
        level = data.get('difficulty_name', 'Unknown')
        difficulty_counts[level] = difficulty_counts.get(level, 0) + 1
    
    print("\nDifficulty Distribution:")
    for level, count in sorted(difficulty_counts.items(), 
                               key=lambda x: (x[0] != 'Unknown', x[0])):
        percentage = (count / len(results)) * 100
        print(f"  {level}: {count} files ({percentage:.1f}%)")
    
    # Average tag count
    total_tags = sum(data.get('tag_count', 0) for data in results.values())
    avg_tags = total_tags / len(results) if results else 0
    print(f"\nAverage tags per file: {avg_tags:.1f}")
    
    print("\nIndividual File Results:")
    for video_id, data in sorted(results.items()):
        print(f"  {data['file_name']}:")
        print(f"    - Difficulty: {data.get('difficulty_name', 'Unknown')}")
        print(f"    - Tags: {data.get('tag_count', 0)}")

def create_sample_transcripts(directory: str) -> None:
    """
    Create sample transcript files for demonstration.
    
    Args:
        directory: Directory to create sample files in
    """
    # Ensure directory exists
    os.makedirs(directory, exist_ok=True)
    
    # Sample transcript texts of varying difficulties
    samples = {
        "beginner_transcript.txt": """
        Hello! My name is John. I am a teacher. I teach English.
        I live in a small house. The house is near a park.
        I like to read books. Books are fun. I also like to watch TV.
        My favorite food is pizza. Pizza is yummy!
        """,
        
        "intermediate_transcript.txt": """
        Language learning requires dedication and consistent practice over time.
        There are various methods to improve your vocabulary, including reading
        books, watching movies with subtitles, and engaging in conversations with
        native speakers. Many learners find that immersion is the most effective approach.
        Cultural understanding is also essential when learning a new language.
        """,
        
        "advanced_transcript.txt": """
        The intricate relationship between linguistic proficiency and cognitive development
        has been extensively studied in academic literature. Research suggests that multilingual
        individuals demonstrate enhanced executive functioning, particularly in areas related to
        attention control and task switching. Furthermore, the acquisition of multiple languages
        during critical developmental periods may facilitate neuroplasticity, thereby establishing
        more robust neural networks for processing complex information.
        
        Contemporary pedagogical methodologies emphasize communicative competence over grammatical
        perfection, a paradigm shift from traditional language instruction. This approach prioritizes
        authentic interaction in relevant contexts, acknowledging that linguistic errors are an
        inherent component of the learning process rather than indicators of failure.
        """
    }
    
    # Create each sample file
    for filename, content in samples.items():
        file_path = Path(directory) / filename
        with open(file_path, "w") as f:
            f.write(content)
        
        logging.info(f"Created sample transcript: {filename}")

def main():
    # Create sample transcripts
    sample_dir = "./sample_transcripts"
    create_sample_transcripts(sample_dir)
    
    # Create custom configuration
    config = create_custom_config()
    
    # Create tagger with custom config
    tagger = TranscriptTagger(config)
    
    # Process all transcripts in the directory
    results = process_directory(tagger, sample_dir)
    
    # Analyze and display results
    analyze_results(results)
    
    print(f"\nDetailed results saved to: {config.storage_path}/transcript_tags.json")
    
    # Example of direct difficulty analysis
    print("\n===== Direct Difficulty Analysis =====")
    analyzer = DifficultyAnalyzer(config)
    
    sample_text = """
    This is a direct analysis example using the DifficultyAnalyzer class.
    You can analyze text directly without saving results to storage.
    """
    
    analysis = analyzer.analyze_text(sample_text)
    print(f"Difficulty: {analysis['difficulty_name']} ({analysis['difficulty_level']}/5)")
    print(f"Word count: {analysis['metrics']['word_count']}")
    print(f"Flesch-Kincaid Grade: {analysis['metrics']['readability']['flesch_kincaid_grade']:.2f}")

if __name__ == "__main__":
    main() 