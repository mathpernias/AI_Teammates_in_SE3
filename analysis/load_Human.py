import pandas as pd
import requests
import re
from tqdm import tqdm
import dotenv
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

dotenv.load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

pd.set_option('display.max_columns', None)

# Configuration
MAX_WORKERS = 5  # Parallel requests
RETRY_DELAY = 2  # Seconds between retries
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30  # Seconds

def run_query(query, variables, retry_count=0):
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    
    try:
        response = requests.post(
            url, 
            json={"query": query, "variables": variables}, 
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
        
        if "errors" in data:
            raise Exception(data["errors"])
        return data["data"]
    
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
        if retry_count < MAX_RETRIES:
            print(f"Timeout/Connection error, retrying in {RETRY_DELAY}s... (attempt {retry_count + 1}/{MAX_RETRIES})")
            time.sleep(RETRY_DELAY)
            return run_query(query, variables, retry_count + 1)
        else:
            raise e
    
    except requests.exceptions.HTTPError as e:
        # Handle rate limiting
        if response.status_code == 429 or response.status_code == 403:
            retry_after = int(response.headers.get('Retry-After', 60))
            print(f"Rate limited. Waiting {retry_after} seconds...")
            time.sleep(retry_after)
            if retry_count < MAX_RETRIES:
                return run_query(query, variables, retry_count + 1)
        raise e

def parse_pr_url(url):
    match = re.search(r"github\.com/([^/]+)/([^/]+)/pull/(\d+)", url)
    if match:
        return match.group(1), match.group(2), int(match.group(3))
    return None, None, None

PR_QUERY = """
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      number
      additions
      deletions
      changedFiles
      commits { totalCount }
      comments { totalCount }
      reviews(first: 100) {
        totalCount
        nodes {
          author { login }
        }
      }
      reviewRequests(first: 100) {
        nodes {
          requestedReviewer {
            __typename
            ... on User { login }
            ... on Team { name }
            ... on Mannequin { login }
            ... on Bot { login }
          }
        }
      }
    }
  }
}
"""

def get_pr_stats(url):
    owner, repo, number = parse_pr_url(url)

    if owner is None:
        return {
            "additions": None,
            "deletions": None,
            "changed_files": None,
            "commit_count": None,
            "review_count": None,
            "comment_count": None,
            "reviewer_count_ui": None
        }

    variables = {"owner": owner, "repo": repo, "number": number}

    try:
        data = run_query(PR_QUERY, variables)
        pr = data["repository"]["pullRequest"]

        pending_reviewers = {
            r["requestedReviewer"]["login"]
            for r in pr["reviewRequests"]["nodes"]
            if r["requestedReviewer"] is not None
               and "login" in r["requestedReviewer"]
        }

        submitted_reviewers = {
            r["author"]["login"]
            for r in pr["reviews"]["nodes"]
            if r["author"] is not None
        }

        ui_reviewers = pending_reviewers | submitted_reviewers

        return {
            "additions": pr["additions"],
            "deletions": pr["deletions"],
            "changed_files": pr["changedFiles"],
            "commit_count": pr["commits"]["totalCount"],
            "review_count": pr["reviews"]["totalCount"],
            "comment_count": pr["comments"]["totalCount"],
            "reviewer_count_ui": len(ui_reviewers)
        }

    except Exception as e:
        print(f"ERROR for PR: {url}")
        print(f"Error: {e}")
        return {
            "additions": None,
            "deletions": None,
            "changed_files": None,
            "commit_count": None,
            "review_count": None,
            "comment_count": None,
            "reviewer_count_ui": None
        }

def process_single_row(row, url_column):
    """Process a single row - for parallel execution"""
    url = row[url_column]
    stats = get_pr_stats(url)
    return stats

def enrich_df_with_pr_stats(df, url_column="html_url", max_workers=MAX_WORKERS):
    """
    Enrich dataframe with PR stats using parallel requests
    """
    results = [None] * len(df)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_idx = {
            executor.submit(process_single_row, row, url_column): idx
            for idx, row in df.iterrows()
        }
        
        # Process completed tasks with progress bar
        for future in tqdm(as_completed(future_to_idx), total=len(df), desc="Fetching PR stats"):
            idx = future_to_idx[future]
            try:
                results[idx] = future.result()
            except Exception as e:
                print(f"Failed to process row {idx}: {e}")
                results[idx] = {
                    "additions": None,
                    "deletions": None,
                    "changed_files": None,
                    "commit_count": None,
                    "review_count": None,
                    "comment_count": None,
                    "reviewer_count_ui": None
                }

    stats_df = pd.DataFrame(results)
    enriched = pd.concat([df.reset_index(drop=True), stats_df], axis=1)
    return enriched

if __name__ == "__main__":
    human_pr_df = pd.read_parquet("hf://datasets/hao-li/AIDev/human_pull_request.parquet")
    limited_df = human_pr_df.head(15)  # For testing
    
    # Process with parallel requests
    enriched = enrich_df_with_pr_stats(human_pr_df, url_column="html_url", max_workers=5)
    enriched.to_csv("human_prs_enriched.csv", index=False)
