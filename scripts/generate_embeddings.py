import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from core.services.embedding_service import EmbeddingService
import requests
import time

API_BASE_URL = "http://localhost:8000/v1"

def generate_embeddings_for_all_jobs(limit=None):
    """Generate embeddings for all jobs in the database."""
    
    print("🤖 Initializing embedding service...")
    embedding_service = EmbeddingService()
    
    print(f"\n📊 Fetching jobs from API...")
    
    # Fetch all jobs
    response = requests.get(f"{API_BASE_URL}/jobs", params={"limit": limit or 10000})
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch jobs: {response.status_code}")
        return
    
    jobs = response.json()
    total = len(jobs)
    
    print(f"✅ Found {total} jobs")
    print("=" * 70)
    
    successful = 0
    failed = 0
    start_time = time.time()
    
    for i, job in enumerate(jobs):
        try:
            # Create a simple job object
            class SimpleJob:
                def __init__(self, data):
                    self.title = data.get('title', '')
                    self.description = data.get('description', '')
                    self.responsibilities = data.get('responsibilities')
                    self.requirements = data.get('requirements', {})
                    self.category = data.get('category')
                    self.location = data.get('location')
            
            job_obj = SimpleJob(job)
            
            # Generate embedding
            embedding = embedding_service.generate_job_embedding(job_obj)
            
            # Update job via API
            job_id = job['id']
            update_data = {"embedding": embedding}
            
            update_response = requests.patch(
                f"{API_BASE_URL}/jobs/{job_id}",
                json=update_data
            )
            
            if update_response.status_code == 200:
                successful += 1
            else:
                failed += 1
                print(f"⚠️  Failed to update job {job_id}: {update_response.status_code}")
            
            # Progress update every 50 jobs
            if (i + 1) % 50 == 0:
                elapsed = time.time() - start_time
                rate = (i + 1) / elapsed if elapsed > 0 else 0
                eta = (total - (i + 1)) / rate if rate > 0 else 0
                
                progress = (i + 1) / total * 100
                print(f"📊 Progress: {i + 1}/{total} ({progress:.1f}%) | "
                      f"✅ {successful} | ❌ {failed} | "
                      f"⏱️  {rate:.1f} jobs/s | ETA: {eta/60:.1f}min")
        
        except Exception as e:
            failed += 1
            print(f"❌ Error processing job {job.get('id')}: {e}")
    
    elapsed = time.time() - start_time
    
    print("\n" + "=" * 70)
    print(f"🎉 Embedding generation complete in {elapsed/60:.1f} minutes!")
    print(f"✅ Successfully processed: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Success rate: {(successful/total*100):.1f}%")

if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    
    if limit:
        print(f"🧪 TEST MODE: Processing {limit} jobs")
    else:
        print(f"🚀 FULL MODE: Processing all jobs")
    
    generate_embeddings_for_all_jobs(limit=limit)