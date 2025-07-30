"""
Configuration settings for the transcript tagging system.
"""

import os
from pathlib import Path
from typing import Dict, List, Union, Optional
import json

class Config:
    """Configuration class for the transcript tagger SDK."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize configuration with default settings.
        
        Args:
            api_key (str, optional): OpenAI API key. If not provided, will look for
                                     OPENAI_API_KEY environment variable.
        """
        # API Settings
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4o"
        self.max_tokens = 3000
        
        # Content difficulty settings
        self.difficulty_levels = {
            1: "初级/Beginner",       # 简单的日常词汇和句式，适合初学者
            2: "中级/Intermediate",   # 一般词汇和句式，适合有基础的学习者
            3: "高级/Advanced",       # 复杂词汇和句式，包含一些专业术语，适合进阶学习者
            4: "专业/Professional",   # 大量专业词汇和复杂句式，适合该领域的专业人士或研究人员
            5: "学术/Academic"        # 高度专业化的内容，大量学术词汇，复杂句式和推理，适合学者和专家
        }
        
        # Readability thresholds (基于Flesch-Kincaid Grade Level)
        self.readability_thresholds = {
            "初级/Beginner": 6,       # 相当于小学水平
            "中级/Intermediate": 10,  # 相当于初中水平
            "高级/Advanced": 14,      # 相当于高中或大学低年级水平
            "专业/Professional": 18,  # 相当于大学高年级或研究生水平
            "学术/Academic": 22       # 相当于博士或专业学术水平
        }
        
        # Word frequency thresholds - percentage of infrequent words
        self.word_frequency_thresholds = {
            "初级/Beginner": 0.05,     # 少于5%的生词
            "中级/Intermediate": 0.10, # 少于10%的生词
            "高级/Advanced": 0.15,     # 少于15%的生词
            "专业/Professional": 0.20, # 少于20%的生词
            "学术/Academic": 0.25      # 少于25%的生词
        }
        
        # Sentence complexity thresholds - average words per sentence
        self.sentence_complexity_thresholds = {
            "初级/Beginner": 12,       # 平均每句12个单词或更少
            "中级/Intermediate": 18,   # 平均每句18个单词或更少
            "高级/Advanced": 22,       # 平均每句22个单词或更少
            "专业/Professional": 26,   # 平均每句26个单词或更少
            "学术/Academic": 30        # 平均每句30个单词或更多
        }
        
        # Tag categories and tags
        self.tag_categories = {
            "Topic": [
                "Technology", "Science", "Health", "Finance", "Business", 
                "Politics", "Entertainment", "Sports", "Education", "History",
                "Philosophy", "Psychology", "Art", "Literature", "Environment",
                "Travel", "Food", "Fashion", "Relationships", "Personal Development"
            ],
            
            "Format": [
                "Interview", "Lecture", "Debate", "Panel Discussion", "Monologue",
                "Q&A Session", "Tutorial", "Storytelling", "News Report", "Analysis",
                "Review", "Conversation"
            ],
            
            "Audience": [
                "General", "Academic", "Professional", "Students", "Children",
                "Experts", "Beginners", "Enthusiasts", "Practitioners"
            ],
            
            "Depth": [
                "Introductory", "Intermediate", "Advanced", "In-depth", "Overview",
                "Detailed", "Technical", "Theoretical", "Practical", "Conceptual"
            ],
            
            "Tone": [
                "Formal", "Informal", "Serious", "Humorous", "Inspirational",
                "Critical", "Neutral", "Enthusiastic", "Contemplative", "Controversial",
                "Educational", "Conversational"
            ],
            
            "Time Period": [
                "Historical", "Contemporary", "Future-oriented", "Timeless"
            ]
        }
        
        # Flatten the tag list for easy checking
        self.all_predefined_tags = [tag for category in self.tag_categories.values() for tag in category]
        
        # Default path for storage
        self.storage_path = None
    
    def set_api_key(self, api_key: str) -> None:
        """Set the OpenAI API key."""
        self.api_key = api_key
    
    def set_model(self, model: str) -> None:
        """Set the OpenAI model to use."""
        self.model = model
    
    def set_custom_thresholds(self, 
                              beginner_readability: Optional[float] = None,
                              intermediate_readability: Optional[float] = None,
                              advanced_readability: Optional[float] = None,
                              professional_readability: Optional[float] = None,
                              academic_readability: Optional[float] = None) -> None:
        """
        Set custom readability thresholds for difficulty levels.
        
        Args:
            beginner_readability (float, optional): Flesch-Kincaid grade level for Beginner
            intermediate_readability (float, optional): Flesch-Kincaid grade level for Intermediate
            advanced_readability (float, optional): Flesch-Kincaid grade level for Advanced
            professional_readability (float, optional): Flesch-Kincaid grade level for Professional
            academic_readability (float, optional): Flesch-Kincaid grade level for Academic
        """
        if beginner_readability is not None:
            self.readability_thresholds["初级/Beginner"] = beginner_readability
        
        if intermediate_readability is not None:
            self.readability_thresholds["中级/Intermediate"] = intermediate_readability
        
        if advanced_readability is not None:
            self.readability_thresholds["高级/Advanced"] = advanced_readability
        
        if professional_readability is not None:
            self.readability_thresholds["专业/Professional"] = professional_readability
        
        if academic_readability is not None:
            self.readability_thresholds["学术/Academic"] = academic_readability
    
    def set_storage_path(self, path: Union[str, Path]) -> None:
        """
        Set the path for storing tag and difficulty results.
        
        Args:
            path (str or Path): Path to the storage directory
        """
        if isinstance(path, str):
            path = Path(path)
        
        # Ensure the directory exists
        path.mkdir(parents=True, exist_ok=True)
        self.storage_path = path
    
    def get_tag_prompt(self, transcript: str) -> str:
        """
        Generate the prompt for tag analysis.
        
        Args:
            transcript (str): The transcript text
            
        Returns:
            str: Formatted prompt for OpenAI
        """
        # Format tag categories for the prompt
        tag_categories_str = ""
        for category, tags in self.tag_categories.items():
            tag_categories_str += f"{category}: {', '.join(tags)}\n"
        
        # Return formatted prompt
        return f"""
You're analyzing a transcript to identify relevant tags.

Here are the predefined tag categories:
{tag_categories_str}

INSTRUCTIONS:
1. Analyze the transcript carefully.
2. Select the most relevant tags from the predefined categories that best describe the content.
3. IMPORTANT: Return ONLY the tag names themselves, NOT the category names. For example, return "History" NOT "Topic: History".
4. Suggest up to 5 additional custom tags that are highly specific to the content and would help in searching.
5. Format your response as a JSON object with two keys:
   - "predefined_tags": Array of tags selected from the predefined list (just the tag names, not categories)
   - "custom_tags": Array of specific custom tags you suggest adding

Transcript to analyze:
---
{transcript[:self.max_tokens]}
---

Respond ONLY with the JSON object, nothing else.
""" 