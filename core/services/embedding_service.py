from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np


class EmbeddingService:
    """Service for generating text embeddings using sentence-transformers."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """Initialize with a sentence-transformer model.
        
        'all-MiniLM-L6-v2' is a good balance of speed and quality:
        - Fast inference
        - 384 dimensions
        - Good for semantic similarity
        """
        print(f"🤖 Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        print(f"✅ Model loaded!")
    
    def generate_job_embedding(self, job) -> List[float]:
        """Generate embedding for a job posting."""
        # Combine relevant text fields
        text_parts = [
            job.title,
            job.description[:500] if job.description else "",  # Limit description length
            job.responsibilities or "",
            job.category or "",
            job.location or "",
        ]
        
        # Add requirements
        if job.requirements:
            req_text = " ".join([f"{k}: {v}" for k, v in job.requirements.items()])
            text_parts.append(req_text)
        
        # Combine into single text
        combined_text = " ".join(text_parts)
        
        # Generate embedding
        embedding = self.model.encode(combined_text, convert_to_numpy=True)
        
        return embedding.tolist()
    
    def generate_candidate_embedding(self, candidate) -> List[float]:
        """Generate embedding for a candidate profile."""
        # Combine relevant text fields
        text_parts = [
            candidate.name,
            candidate.education or "",
            candidate.location or "",
            candidate.experience or "",
        ]
        
        # Add skills
        if candidate.skills:
            skills_text = " ".join(candidate.skills)
            text_parts.append(skills_text)
        
        # Add answers
        if candidate.answers:
            answers_text = " ".join([f"{k}: {v}" for k, v in candidate.answers.items()])
            text_parts.append(answers_text)
        
        # Combine into single text
        combined_text = " ".join(text_parts)
        
        # Generate embedding
        embedding = self.model.encode(combined_text, convert_to_numpy=True)
        
        return embedding.tolist()
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings."""
        # Convert to numpy arrays
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        # Calculate cosine similarity
        similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        
        return float(similarity)