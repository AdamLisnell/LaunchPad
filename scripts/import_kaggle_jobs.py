import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import time
from typing import Dict, Any, Optional
import sys

# API Configuration
API_BASE_URL = "http://localhost:8000/v1"
BATCH_SIZE = 100

def load_linkedin_data(file_path: str) -> pd.DataFrame:
    """Load LinkedIn job postings."""
    print(f"📂 Loading data from {file_path}...")
    df = pd.read_csv(file_path)
    print(f"✅ Loaded {len(df)} job postings")
    return df

def transform_to_launchpad_format(row: pd.Series) -> Optional[Dict[str, Any]]:
    """Transform LinkedIn data to LaunchPad format."""
    try:
        # Extract and clean data
        title = str(row.get('title', 'Unknown Position'))
        if title == 'nan' or not title:
            return None
            
        description = str(row.get('description', ''))
        if description == 'nan':
            description = f"Position: {title}"
        
        # Build job data
        job_data = {
            "title": title[:255],  # Limit length
            "description": description[:2000] if description else f"Position: {title}",
            "responsibilities": str(row.get('formatted_work_type', ''))[:1000],
            "requirements": {
                "experience": str(row.get('formatted_experience_level', '')),
                "work_type": str(row.get('formatted_work_type', '')),
            },
            "salary": extract_salary(row),
            "company": str(row.get('company_name', 'Unknown Company'))[:255],
            "category": extract_category(row),
            "location": str(row.get('location', 'Remote'))[:255],
            "application_end_date": generate_end_date()
        }
        
        return job_data
        
    except Exception as e:
        print(f"⚠️  Error transforming row: {e}")
        return None

def extract_salary(row: pd.Series) -> Optional[float]:
    """Extract salary if available."""
    try:
        if 'max_salary' in row and pd.notna(row['max_salary']):
            return float(row['max_salary'])
        elif 'med_salary' in row and pd.notna(row['med_salary']):
            return float(row['med_salary'])
    except:
        pass
    return None

def extract_category(row: pd.Series) -> str:
    """Extract job category."""
    work_type = str(row.get('formatted_work_type', ''))
    if work_type and work_type != 'nan':
        return work_type[:100]
    return "General"

def generate_end_date() -> str:
    """Generate application end date."""
    import random
    days_ahead = random.randint(30, 90)
    end_date = datetime.now() + timedelta(days=days_ahead)
    return end_date.strftime('%Y-%m-%d')

def create_job_via_api(job_data: Dict[str, Any]) -> bool:
    """Create job via LaunchPad API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/jobs",
            json=job_data,
            timeout=10
        )
        
        return response.status_code == 201
            
    except Exception as e:
        return False

def import_jobs(csv_path: str, limit: Optional[int] = None):
    """Import jobs from CSV to LaunchPad."""
    
    # Load data
    df = load_linkedin_data(csv_path)
    
    # Clean: Remove rows without titles
    df = df[df['title'].notna()]
    
    # Limit if specified
    if limit:
        df = df.head(limit)
        print(f"🧪 TEST MODE: Limiting to {limit} jobs")
    
    # Remove duplicates
    if 'job_id' in df.columns:
        df = df.drop_duplicates(subset=['job_id'])
    
    total = len(df)
    successful = 0
    failed = 0
    
    print(f"\n🚀 Starting import of {total} jobs...")
    print("=" * 70)
    
    start_time = time.time()
    
    for i, (idx, row) in enumerate(df.iterrows()):
        job_data = transform_to_launchpad_format(row)
        
        if job_data is None:
            failed += 1
            continue
        
        if create_job_via_api(job_data):
            successful += 1
        else:
            failed += 1
        
        # Progress update every 10 jobs
        if (i + 1) % 10 == 0:
            elapsed = time.time() - start_time
            rate = successful / elapsed if elapsed > 0 else 0
            eta = (total - (i + 1)) / rate if rate > 0 else 0
            
            progress = (i + 1) / total * 100
            print(f"📊 Progress: {i + 1}/{total} ({progress:.1f}%) | "
                f"✅ {successful} | ❌ {failed} | "
                f"⏱️  {rate:.1f} jobs/s | ETA: {eta/60:.1f}min")
        
        # Rate limiting
        if (i + 1) % BATCH_SIZE == 0:
            time.sleep(1)
    
    elapsed = time.time() - start_time
    
    print("\n" + "=" * 70)
    print(f"🎉 Import complete in {elapsed/60:.1f} minutes!")
    print(f"✅ Successfully imported: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Success rate: {(successful/total*100):.1f}%")

if __name__ == "__main__":
    csv_path = "data/kaggle_jobs/postings.csv"
    
    # Get limit from command line
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    
    if limit:
        print(f"🧪 TEST MODE: Importing {limit} jobs")
    else:
        print(f"🚀 FULL IMPORT MODE")
        confirm = input("⚠️  This will import ALL jobs. Continue? (yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ Import cancelled")
            sys.exit(0)
    
    import_jobs(csv_path, limit=limit)