"""
Command Line Interface for Transcript Tagger.
Provides commands for tagging and analyzing transcripts from the command line.
"""

import argparse
import logging
import sys
import os
from pathlib import Path
from typing import Optional, List

from .config import Config
from .transcript_tagger import TranscriptTagger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(stream=sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def setup_parser() -> argparse.ArgumentParser:
    """Set up the command line argument parser."""
    parser = argparse.ArgumentParser(
        description='Transcript Tagger: Analyze and tag transcript content using AI'
    )
    
    parser.add_argument(
        '--api-key', 
        type=str, 
        help='OpenAI API key. If not provided, will use OPENAI_API_KEY environment variable.'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default='gpt-3.5-turbo',
        help='OpenAI model to use (default: gpt-3.5-turbo)'
    )
    
    parser.add_argument(
        '--storage-path',
        type=str,
        default='./data',
        help='Path to store tagging results (default: ./data)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Process command
    process_parser = subparsers.add_parser('process', help='Process transcript file(s)')
    process_parser.add_argument(
        'files', 
        nargs='+', 
        help='Path(s) to transcript file(s)'
    )
    process_parser.add_argument(
        '--tags-only',
        action='store_true',
        help='Only analyze tags, skip difficulty analysis'
    )
    process_parser.add_argument(
        '--difficulty-only',
        action='store_true',
        help='Only analyze difficulty, skip tag analysis'
    )
    
    # View results command
    view_parser = subparsers.add_parser('view', help='View tagging results')
    view_parser.add_argument(
        '--video-id',
        type=str,
        help='View results for specific video ID'
    )
    
    return parser

def process_files(
    tagger: TranscriptTagger, 
    files: List[str],
    tags_only: bool = False,
    difficulty_only: bool = False
) -> None:
    """
    Process transcript files with the tagger.
    
    Args:
        tagger: The TranscriptTagger instance
        files: List of file paths to process
        tags_only: If True, only analyze tags
        difficulty_only: If True, only analyze difficulty
    """
    for file_path in files:
        path = Path(file_path)
        if not path.exists():
            logger.error(f"File not found: {file_path}")
            continue
        
        try:
            logger.info(f"Processing file: {path.name}")
            result = tagger.process_transcript(
                path,
                analyze_tags=not difficulty_only,
                analyze_difficulty=not tags_only
            )
            
            # Print a summary of the results
            difficulty_level = result.get('difficulty', {}).get('difficulty_name', 'Unknown')
            tag_count = sum(len(tags) for tags in result.get('tags', {}).values())
            
            print(f"\nResults for {path.name}:")
            print(f"Video ID: {result['video_id']}")
            
            if not difficulty_only:
                print(f"Tags: {tag_count} tags in {len(result.get('tags', {}))} categories")
            
            if not tags_only:
                print(f"Difficulty: {difficulty_level}")
            
            print(f"Results saved to: {tagger.storage_path / 'transcript_tags.json'}")
        except Exception as e:
            logger.error(f"Error processing {path.name}: {str(e)}")

def view_results(tagger: TranscriptTagger, video_id: Optional[str] = None) -> None:
    """
    View tagging results.
    
    Args:
        tagger: The TranscriptTagger instance
        video_id: If provided, view results for this video ID. Otherwise, view all results.
    """
    results = tagger.get_results(video_id)
    
    if not results:
        print("No results found.")
        return
    
    if video_id:
        # Display detailed results for a single video
        print(f"\nResults for Video ID: {video_id}")
        print(f"File: {results.get('file_name', 'Unknown')}")
        
        # Display tags
        tags = results.get('tags', {})
        print("\nTags:")
        if tags:
            for category, tag_list in tags.items():
                print(f"  {category}:")
                for tag in tag_list:
                    print(f"    - {tag}")
        else:
            print("  No tags available")
        
        # Display difficulty
        difficulty = results.get('difficulty', {})
        if difficulty:
            print("\nDifficulty Analysis:")
            print(f"  Level: {difficulty.get('difficulty_name', 'Unknown')} ({difficulty.get('difficulty_level', 'Unknown')}/5)")
            
            metrics = difficulty.get('metrics', {})
            if metrics:
                print("  Metrics:")
                print(f"    - Word Count: {metrics.get('word_count', 'Unknown')}")
                print(f"    - Sentence Count: {metrics.get('sentence_count', 'Unknown')}")
                print(f"    - Average Word Length: {metrics.get('avg_word_length', 'Unknown'):.2f}")
                print(f"    - Average Sentence Length: {metrics.get('avg_sentence_length', 'Unknown'):.2f}")
                
                readability = metrics.get('readability', {})
                if readability:
                    print("    - Readability:")
                    print(f"      - Flesch Reading Ease: {readability.get('flesch_reading_ease', 'Unknown'):.2f}")
                    print(f"      - Flesch-Kincaid Grade: {readability.get('flesch_kincaid_grade', 'Unknown'):.2f}")
        else:
            print("\nDifficulty Analysis: Not available")
    else:
        # Display summary of all results
        print("\nAll Tagging Results:")
        print(f"Total Videos: {len(results)}")
        
        for video_id, result in results.items():
            difficulty = result.get('difficulty', {}).get('difficulty_name', 'Unknown')
            tag_count = sum(len(tags) for tags in result.get('tags', {}).values())
            
            print(f"\nVideo ID: {video_id}")
            print(f"  File: {result.get('file_name', 'Unknown')}")
            print(f"  Tags: {tag_count} tags")
            print(f"  Difficulty: {difficulty}")

def main() -> None:
    """Main entry point for the CLI application."""
    parser = setup_parser()
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return
    
    # Create configuration
    config = Config()
    
    if args.api_key:
        config.set_api_key(args.api_key)
    
    if args.model:
        config.set_model(args.model)
    
    if args.storage_path:
        config.set_storage_path(args.storage_path)
    
    # Create tagger
    tagger = TranscriptTagger(config)
    
    # Execute command
    if args.command == 'process':
        process_files(
            tagger, 
            args.files,
            tags_only=args.tags_only,
            difficulty_only=args.difficulty_only
        )
    elif args.command == 'view':
        view_results(tagger, args.video_id)

if __name__ == '__main__':
    main() 