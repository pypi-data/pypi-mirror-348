import os
import json
from datetime import datetime
from pathlib import Path
from transmeet.utils.json_parser import extract_json_from_text

ROOT_DIR = Path(__file__).resolve().parent.parent

prompts_dir = ROOT_DIR / "prompts"

def generate_meeting_minutes(transcribed_text, llm_client, model_name, meeting_datetime=None):
    system_prompt = "You are an expert assistant responsible for drafting professional and concise meeting minutes."
    
    with open(prompts_dir / "transcription_to_meeting_minutes.md", "r") as f:
        user_prompt = f.read()
    user_prompt = user_prompt.replace("{transcribed_text}", transcribed_text)

    user_prompt = user_prompt.replace("{meeting_datetime}", meeting_datetime) \
        if meeting_datetime else user_prompt.replace("{meeting_datetime}", 
                                                     datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    response = llm_client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content.strip()


def segment_conversation_by_speaker(transcribed_text, llm_client, model_name):
    system_prompt = """You are an assistant tasked with segmenting a conversation by speaker.
    Identify the speakers based on context and transitions in the dialogue. Label each speaker with a unique identifier (e.g., Speaker 1, Speaker 2, Speaker 3, etc.) 
    and clearly divide the conversation between them. Make sure the segmentation respects the flow of the conversation and clearly marks speaker changes."""
    
    user_prompt = f"""
    TRANSCRIPT TEXT: {transcribed_text}
    Please segment the following conversation by speaker, identifying the shifts in speaker and labeling each section accordingly.
    Ensure you handle multiple speakers and clearly mark the transitions.
    """

    response = llm_client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def create_podcast_dialogue(transcribed_text, llm_client, model_name):
    
    system_prompt = """
        You are a podcast scriptwriter skilled in converting corporate meeting transcripts into
        engaging, two-person podcast conversations. Your tone is friendly, intelligent, and conversational,
        designed for a general audience interested in technology, leadership, and innovation.
        """
    
    with open(prompts_dir / "synteatic_audio_generation.md", "r") as f:
        user_prompt = f.read()

    user_prompt = user_prompt.replace("{transcribed_text}", transcribed_text)

    response = llm_client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message.content.strip()

def transform_transcript_to_mind_map(transcribed_text, llm_client, model_name):
    # System prompt to instruct the LLM to organize the transcript into a hierarchical mind map
    system_prompt = """
    You are a highly skilled assistant who specializes in transforming long, unstructured text (such as meeting transcriptions) 
    into a well-organized mind map structure. Your task is to extract the main topics and subtopics, organize them hierarchically, 
    and return the result in JSON format. The output should reflect the main themes, subpoints, and their relationships.
    """
    
    # User prompt that includes the transcript text and specific instructions
    with open(prompts_dir / "transcript_to_mind_map.md", "r") as f:
        user_prompt = f.read()
    user_prompt = user_prompt.replace("{transcribed_text}", transcribed_text)
    
    # Requesting LLM to generate the mind map in JSON format
    response = llm_client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    # Parsing and returning the mind map output
    mind_map = response.choices[0].message.content.strip()
    
    print(mind_map)

    # Optionally convert the result into a dictionary (JSON)
    mind_map_json = extract_json_from_text(mind_map)
    
    return mind_map_json
