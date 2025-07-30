#!/usr/bin/env python3
"""
Basic example of using the Transcript Tagger SDK.
"""

import os
import logging
from pathlib import Path
from transcript_tagger_sdk import TranscriptTagger, Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    # Get API key from environment variable
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logging.warning("No OpenAI API key found. Set OPENAI_API_KEY environment variable.")
        logging.warning("Proceeding with difficulty analysis only.")
    
    # Create configuration
    config = Config()
    if api_key:
        config.set_api_key(api_key)
    
    # Set custom storage path
    config.set_storage_path("./results")
    
    # Create tagger instance
    tagger = TranscriptTagger(config)
    
    # Example transcript file path
    # Replace with your actual transcript file path
    transcript_path = Path("./sample_transcript.txt")
    
    if not transcript_path.exists():
        # Create a sample transcript for demonstration
        logging.info("Sample transcript not found. Creating one for demonstration.")
        sample_text = """
        This is a sample transcript for demonstration purposes.
        It contains simple sentences with basic vocabulary.
        The sentences are short and easy to understand.
        This would typically be classified as beginner level content.
        """
        
        transcript_path = Path("./sample_transcript.txt")
        with open(transcript_path, "w") as f:
            f.write(sample_text)
    
    # Process the transcript
    logging.info(f"Processing transcript: {transcript_path}")
    result = tagger.process_transcript(
        transcript_path,
        analyze_tags=bool(api_key),  # Only analyze tags if API key is available
        analyze_difficulty=True
    )
    
    # Display results
    print("\nProcessing completed!")
    print(f"Video ID: {result['video_id']}")
    
    if 'tags' in result and result['tags']:
        print("\nTags:")
        for category, tags in result['tags'].items():
            print(f"  {category}:")
            for tag in tags:
                print(f"    - {tag}")
    
    if 'difficulty' in result and result['difficulty']:
        difficulty = result['difficulty']
        print("\nDifficulty Analysis:")
        print(f"  Level: {difficulty.get('difficulty_name')} ({difficulty.get('difficulty_level')}/5)")
        
        metrics = difficulty.get('metrics', {})
        if metrics:
            print("  Metrics:")
            print(f"    - Word Count: {metrics.get('word_count')}")
            print(f"    - Sentence Count: {metrics.get('sentence_count')}")
            print(f"    - Average Word Length: {metrics.get('avg_word_length'):.2f}")
            print(f"    - Average Sentence Length: {metrics.get('avg_sentence_length'):.2f}")
    
    print(f"\nResults saved to: {config.storage_path}/transcript_tags.json")

if __name__ == "__main__":
    main() 