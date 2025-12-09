from typing import List, Dict, Any, Optional
from core.domain.candidate import Candidate
from core.domain.job import Job
from core.ports.repositories.candidate_repository import CandidateRepository
from core.ports.repositories.job_repository import JobRepository
from core.services.embedding_service import EmbeddingService


class MatchJobs:
    """Use case for matching jobs to candidates using semantic similarity."""

    def __init__(
        self,
        job_repository: JobRepository,
        candidate_repository: CandidateRepository,
        embedding_service: Optional[EmbeddingService] = None
    ):
        self.job_repository = job_repository
        self.candidate_repository = candidate_repository
        self.embedding_service = embedding_service or EmbeddingService()

    async def match_jobs_for_profile(
        self, candidate: Candidate, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Match jobs for a candidate using semantic similarity.

        Returns a list of matches with structure:
        [{"job": Job, "score": float, "match_reasons": List[str]}]
        """
        # Generate candidate embedding if not exists
        if not candidate.embedding:
            candidate.embedding = self.embedding_service.generate_candidate_embedding(candidate)
            if candidate.id:
                await self.candidate_repository.update(candidate.id, candidate)

        # Get all available jobs
        available_jobs = await self.job_repository.find_available()

        # Calculate match scores
        matches = []
        for job in available_jobs:
            # Skip jobs without embeddings
            if not job.embedding:
                continue

            # Calculate semantic similarity
            similarity = self.embedding_service.calculate_similarity(
                candidate.embedding,
                job.embedding
            )

            # Convert to percentage score (0-100)
            semantic_score = similarity * 100

            # Traditional matching factors
            traditional_score = self._calculate_traditional_score(candidate, job)

            # Combined score: 70% semantic, 30% traditional
            combined_score = (semantic_score * 0.7) + (traditional_score * 0.3)

            # Only include matches with reasonable scores
            if combined_score > 30:
                match_reasons = self._get_match_reasons(candidate, job, semantic_score, traditional_score)
                matches.append({
                    "job": job,
                    "score": combined_score,
                    "match_reasons": match_reasons
                })

        # Sort by score (descending)
        matches.sort(key=lambda x: x["score"], reverse=True)

        # Return top matches
        return matches[:limit]

    def _calculate_traditional_score(self, candidate: Candidate, job: Job) -> float:
        """Calculate traditional rule-based match score."""
        score = 0.0

        # Match based on location (weight: 10)
        if candidate.location and job.location:
            if candidate.location.lower() in job.location.lower():
                score += 10.0

        # Match based on skills (weight: 5 per skill)
        job_text = f"{job.title} {job.description}".lower()
        for skill in candidate.skills:
            if skill.lower() in job_text:
                score += 5.0

        # Match based on education (weight: 8)
        if candidate.education and job.requirements.get("education"):
            if candidate.education.lower() in job.requirements.get("education", "").lower():
                score += 8.0

        # Match based on experience (weight: 6)
        if candidate.experience and job.requirements.get("experience"):
            if candidate.experience.lower() in job.requirements.get("experience", "").lower():
                score += 6.0

        return score

    def _get_match_reasons(
        self, 
        candidate: Candidate, 
        job: Job, 
        semantic_score: float,
        traditional_score: float
    ) -> List[str]:
        """Get the reasons for a match."""
        reasons = []

        # Semantic match reason
        if semantic_score > 80:
            reasons.append(f"🎯 Excellent semantic match ({semantic_score:.1f}%)")
        elif semantic_score > 60:
            reasons.append(f"✅ Good semantic match ({semantic_score:.1f}%)")
        elif semantic_score > 40:
            reasons.append(f"👍 Moderate semantic match ({semantic_score:.1f}%)")

        # Location match
        if candidate.location and job.location:
            if candidate.location.lower() in job.location.lower():
                reasons.append(f"📍 Location match: {job.location}")

        # Skills match
        job_text = f"{job.title} {job.description}".lower()
        matched_skills = [s for s in candidate.skills if s.lower() in job_text]
        if matched_skills:
            skills_str = ", ".join(matched_skills[:3])
            if len(matched_skills) > 3:
                skills_str += f" (+{len(matched_skills) - 3} more)"
            reasons.append(f"💡 Matching skills: {skills_str}")

        # Education match
        if candidate.education and job.requirements.get("education"):
            if candidate.education.lower() in job.requirements.get("education", "").lower():
                reasons.append(f"🎓 Education match: {candidate.education}")

        # Experience match
        if candidate.experience and job.requirements.get("experience"):
            if candidate.experience.lower() in job.requirements.get("experience", "").lower():
                reasons.append(f"💼 Experience level matches")

        return reasons

    async def fallback_match(
        self, candidate: Candidate, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Fallback method when sophisticated matching is unavailable.

        Uses a basic rule-based approach without embeddings.
        """
        # Get all jobs (not just available ones, for broader fallback)
        all_jobs = await self.job_repository.list()

        # Basic matching based on simple rules
        matches = []
        for job in all_jobs:
            match_score = 0
            match_reasons = []

            # Check for skill matches in title and description
            job_text = f"{job.title} {job.description}".lower()
            for skill in candidate.skills:
                if skill.lower() in job_text:
                    match_score += 10
                    match_reasons.append(f"Your skill '{skill}' matches this job")

            # Location match
            if candidate.location and job.location:
                if candidate.location.lower() in job.location.lower():
                    match_score += 15
                    match_reasons.append(f"Location match: {job.location}")

            # If we have any match at all, include it
            if match_score > 0:
                matches.append({
                    "job": job,
                    "score": match_score,
                    "match_reasons": match_reasons,
                })

        # Sort by score (descending)
        matches.sort(key=lambda x: x["score"], reverse=True)

        # Return top matches or empty list if none found
        return matches[:limit]