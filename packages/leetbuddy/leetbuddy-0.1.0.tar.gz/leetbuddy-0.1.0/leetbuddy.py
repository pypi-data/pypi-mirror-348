#!/usr/bin/env python3

import os
import json
import click
import requests
import subprocess
import getpass
import time
import re
from pathlib import Path
from typing import Dict, Any, Mapping
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

CONFIG_FILE = os.path.expanduser("~/.leetbuddy_config.json")
LEETCODE_BASE_URL = "https://leetcode.com"
LEETCODE_API_URL = f"{LEETCODE_BASE_URL}/graphql"

# Initialize retry strategy and session
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[403, 500, 502, 503, 504],
    allowed_methods=["GET", "POST"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("https://", adapter)

def load_config() -> Dict[str, Any]:
    """Load configuration from the config file."""
    config_path = Path.home() / '.leetbuddy' / 'config.json'
    if not config_path.exists():
        return {}
    
    with open(config_path) as f:
        return json.load(f)

def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to the config file."""
    config_path = Path.home() / '.leetbuddy'
    config_path.mkdir(parents=True, exist_ok=True)
    
    with open(config_path / 'config.json', 'w') as f:
        json.dump(config, f)

def get_leetcode_session() -> requests.Session:
    """Create and return a configured LeetCode session."""
    config = load_config()
    if not config.get('session_token') or not config.get('csrf_token'):
        raise Exception("Please sign in first using 'leetbuddy signin'")
    
    session = requests.Session()
    
    # Clear any existing cookies first
    session.cookies.clear()
    
    # Set cookies
    session.cookies.set('LEETCODE_SESSION', config['session_token'], domain='.leetcode.com', path='/')
    session.cookies.set('csrftoken', config['csrf_token'], domain='.leetcode.com', path='/')
    
    # Set headers after cookies to ensure CSRF token is available
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": LEETCODE_BASE_URL,
        "Referer": f"{LEETCODE_BASE_URL}/problemset/all/",
        "X-CSRFToken": config['csrf_token']
    }
    session.headers.update(headers)
    
    return session

@click.group()
def cli():
    """LeetBuddy - Your LeetCode companion CLI tool"""
    pass

@cli.command()
def signin():
    """
    Sign in to LeetCode by providing session cookies.
    Example: leetbuddy signin
    """
    try:
        click.echo("Please provide your LeetCode session information.")
        click.echo("To get these values:")
        click.echo("1. Log in to LeetCode in your browser")
        click.echo("2. Open Developer Tools (F12 or Cmd+Option+I on Mac)")
        click.echo("3. Go to Application/Storage -> Cookies -> https://leetcode.com")
        click.echo("4. Find and copy the values for LEETCODE_SESSION and csrftoken")
        
        # Get session token
        session_token = click.prompt("Enter your LEETCODE_SESSION value", type=str)
        csrf_token = click.prompt("Enter your csrftoken value", type=str)
        
        if not session_token or not csrf_token:
            raise Exception("Both LEETCODE_SESSION and csrftoken are required")

        # Initialize session
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Origin": LEETCODE_BASE_URL,
            "Referer": f"{LEETCODE_BASE_URL}/problemset/all/",
            "X-CSRFToken": csrf_token
        })
        
        # Set cookies
        session.cookies.set('LEETCODE_SESSION', session_token, domain='.leetcode.com', path='/')
        session.cookies.set('csrftoken', csrf_token, domain='.leetcode.com', path='/')

        # Verify session using GraphQL
        verify_query = """
        query {
            userStatus {
                isSignedIn
                username
            }
        }
        """
        
        verify_response = session.post(
            LEETCODE_API_URL,
            json={"query": verify_query}
        )
        verify_response.raise_for_status()
        
        verify_data = verify_response.json()
        if not verify_data.get('data', {}).get('userStatus', {}).get('isSignedIn'):
            raise Exception("Session verification failed. Please check your session values and try again.")
        
        username = verify_data['data']['userStatus']['username']
        
        # Save credentials and session
        config = load_config()
        config.update({
            'username': username,
            'session_token': session_token,
            'csrf_token': csrf_token
        })
        save_config(config)
        
        click.echo(f"Login successful! Logged in as: {username}")
        click.echo("Session saved successfully.")

    except requests.exceptions.RequestException as e:
        click.echo(f"Network error during login: {str(e)}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")

@cli.command()
def today():
    """Get today's Problem of the Day and set up workspace"""
    config = load_config()
    if not config.get('session_token') or not config.get('csrf_token'):
        click.echo("Please sign in first using 'leetbuddy signin'")
        return

    try:
        click.echo("Authenticating for 'today' command...")
        session = get_leetcode_session()
        click.echo("Authentication successful.")
        
        daily_query = """
        query questionOfToday {
            activeDailyCodingChallengeQuestion {
                date
                link
                question {
                    title
                    titleSlug
                    content
                    difficulty
                    exampleTestcases
                    codeSnippets {
                        lang
                        code
                        langSlug
                    }
                    topicTags {
                        name
                        slug
                    }
                    hints
                    sampleTestCase
                    metaData 
                }
            }
        }
        """
        
        # Prepare headers for GraphQL request
        graphql_headers = {
            "Content-Type": "application/json",
            "X-CSRFToken": session.cookies.get("csrftoken"), # Crucial for authenticated GraphQL
            "Origin": LEETCODE_BASE_URL,
            "Referer": f"{LEETCODE_BASE_URL}/problemset/all/", # A common referer
            "User-Agent": session.headers.get("User-Agent", ""),
            "Accept": session.headers.get("Accept", "application/json")
        }

        response = session.post(LEETCODE_API_URL, json={"query": daily_query}, headers=graphql_headers)
        response.raise_for_status() # Check for HTTP errors
        data = response.json()
        
        if 'errors' in data:
            # Check for auth errors specifically
            for error in data['errors']:
                if "authentication required" in error.get('message','').lower() or \
                   "unauthenticated" in error.get('message','').lower():
                    click.echo("Authentication error with GraphQL. Your session might be invalid. Try 'leetbuddy signin' again.")
                    # Optionally, clear saved invalid session here
                    # save_config({'username': config['username'], 'password': config['password']}) # Clears cookies
                    return
            raise Exception(f"GraphQL error: {data['errors'][0]['message']}")
        
        if not data.get('data') or not data['data'].get('activeDailyCodingChallengeQuestion'):
            raise Exception("Could not retrieve daily problem data. Response format might have changed or no daily problem active.")

        problem_data = data['data']['activeDailyCodingChallengeQuestion']
        problem = problem_data['question']
        
        click.echo(f"Today's problem: {problem['title']} ({problem['difficulty']})")
        
        problem_dir = problem['titleSlug']
        os.makedirs(problem_dir, exist_ok=True)
        
        with open(os.path.join(problem_dir, "README.md"), "w", encoding="utf-8") as f:
            f.write(f"# {problem['title']}\n\n")
            f.write(f"**Link:** {LEETCODE_BASE_URL}{problem_data['link']}\n\n")
            f.write(f"**Difficulty:** {problem['difficulty']}\n\n")
            f.write("## Problem Statement\n\n")
            f.write(problem['content'] if problem['content'] else "Not available.") # Handle null content
            f.write("\n\n## Example Test Cases\n\n")
            f.write("```\n")
            f.write(problem['exampleTestcases'] if problem['exampleTestcases'] else "Not available.")
            f.write("\n```")
            
            if problem.get('hints'):
                f.write("\n\n## Hints\n\n")
                for i, hint in enumerate(problem['hints'], 1):
                    f.write(f"{i}. {hint}\n")
            
            if problem.get('topicTags'):
                f.write("\n\n## Topics\n\n")
                f.write(", ".join(tag['name'] for tag in problem['topicTags']))
        
        cpp_template = None
        if problem.get('codeSnippets'):
            for snippet in problem['codeSnippets']:
                if snippet['langSlug'] == 'cpp':
                    cpp_template = snippet['code']
                    break
        
        if not cpp_template:
            click.echo("C++ template not found for this problem. Creating a basic placeholder.")
            # Fallback C++ template
            cpp_template = "// Default C++ template\n#include <vector>\n#include <string>\n// Add other necessary headers\n\nclass Solution {\npublic:\n    // Adjust function signature based on problem description\n    void solve() {\n        // Your code here\n    }\n};"


        with open(os.path.join(problem_dir, "solution.cpp"), "w", encoding="utf-8") as f:
            f.write(cpp_template)
        
        click.echo(f"Workspace created at: {os.path.abspath(problem_dir)}")
        
        try:
            subprocess.run(["code", problem_dir], check=True)
        except FileNotFoundError:
            click.echo("'code' command not found. Please open the directory in VS Code manually.")
        except subprocess.CalledProcessError:
            click.echo("Error opening VS Code. Please open the directory manually.")
            
    except requests.exceptions.RequestException as e:
        click.echo(f"Network error: {str(e)}")
    except Exception as e:
        click.echo(f"Error processing 'today' command: {str(e)}")
        # import traceback
        # traceback.print_exc() # For debugging

@cli.command()
def submit():
    """Submit your solution to LeetCode (always from today's POTD directory)"""
    config = load_config()
    if not config.get('session_token') or not config.get('csrf_token'):
        click.echo("Please sign in first using 'leetbuddy signin'")
        return

    original_dir = os.getcwd()
    solution_path = None
    problem_slug = None

    click.echo("Starting submission process...")  # DEBUG

    # Create a fresh session for submission
    session = requests.Session()
    session.cookies.clear()  # Ensure no duplicate cookies
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": LEETCODE_BASE_URL,
        "Referer": f"{LEETCODE_BASE_URL}/problemset/all/",
        "X-CSRFToken": config['csrf_token']
    })
    session.cookies.set('LEETCODE_SESSION', config['session_token'], domain='.leetcode.com', path='/')
    session.cookies.set('csrftoken', config['csrf_token'], domain='.leetcode.com', path='/')

    try:
        click.echo("Fetching today's POTD slug...")  # DEBUG
        # 1. Fetch today's POTD slug
        daily_query = """
        query questionOfToday {
            activeDailyCodingChallengeQuestion {
                question {
                    titleSlug
                }
            }
        }
        """
        gql_headers = {
            "Content-Type": "application/json",
            "X-CSRFToken": config['csrf_token'],
            "Origin": LEETCODE_BASE_URL,
            "Referer": f"{LEETCODE_BASE_URL}/problemset/all/",
            "User-Agent": session.headers.get("User-Agent", ""),
            "Accept": session.headers.get("Accept", "application/json")
        }
        response = session.post(LEETCODE_API_URL, json={"query": daily_query}, headers=gql_headers)
        click.echo(f"GraphQL response status: {response.status_code}")  # DEBUG
        response.raise_for_status()
        data = response.json()
        click.echo(f"GraphQL response data: {data}")  # DEBUG
        potd_slug = data['data']['activeDailyCodingChallengeQuestion']['question']['titleSlug']
        if not potd_slug:
            raise Exception("Could not determine today's POTD slug.")

        click.echo(f"Searching for directory: {potd_slug}")  # DEBUG
        # 2. Search for the directory matching the slug and containing solution.cpp
        potd_dir = None
        for root, dirs, files in os.walk("."):
            if os.path.basename(root) == potd_slug and "solution.cpp" in files:
                potd_dir = os.path.abspath(root)
                break
        if not potd_dir:
            raise Exception(f"Could not find today's POTD directory '{potd_slug}' with solution.cpp. Run 'leetbuddy today' first.")

        os.chdir(potd_dir)
        solution_path = os.path.join(potd_dir, "solution.cpp")
        problem_slug = potd_slug
        click.echo(f"Found today's POTD solution: {solution_path}")

        with open("solution.cpp", "r", encoding="utf-8") as f:
            solution_code = f.read()

        click.echo("Authenticating for submission...")
        click.echo("Authentication successful.")

        # Fetch problem details including questionId using GraphQL
        graphql_query_problem_details = """
        query getQuestionDetails($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                titleSlug
            }
        }
        """
        response_problem_details = session.post(
            LEETCODE_API_URL,
            json={"query": graphql_query_problem_details, "variables": {"titleSlug": problem_slug}},
            headers=gql_headers
        )
        click.echo(f"Problem details response status: {response_problem_details.status_code}")  # DEBUG
        response_problem_details.raise_for_status()
        problem_details_data = response_problem_details.json()
        click.echo(f"Problem details data: {problem_details_data}")  # DEBUG
        if 'errors' in problem_details_data:
            raise Exception(f"GraphQL error fetching problem details: {problem_details_data['errors'][0]['message']}")
        question_data = problem_details_data.get('data', {}).get('question')
        if not question_data or not question_data.get('questionId'):
            raise Exception(f"Could not retrieve question ID for slug '{problem_slug}'. Is the slug correct?")
        question_id = question_data['questionId']
        click.echo(f"Obtained question ID: {question_id}")

        # Submit solution using REST API
        submit_url = f"{LEETCODE_BASE_URL}/problems/{problem_slug}/submit/"
        submit_headers = {
            "Content-Type": "application/json",
            "X-CSRFToken": config['csrf_token'],
            "Origin": LEETCODE_BASE_URL,
            "Referer": f"{LEETCODE_BASE_URL}/problems/{problem_slug}/description/",
            "User-Agent": session.headers.get("User-Agent", ""),
            "Accept": session.headers.get("Accept", "application/json")
        }
        submit_payload = {
            "lang": "cpp",
            "question_id": str(question_id),
            "typed_code": solution_code
        }
        click.echo("Submitting solution...")
        response_submit = session.post(submit_url, json=submit_payload, headers=submit_headers)
        click.echo(f"Submission response status: {response_submit.status_code}")  # DEBUG
        response_submit.raise_for_status()
        try:
            submission_response_data = response_submit.json()
            click.echo(f"Submission response data: {submission_response_data}")  # DEBUG
            if 'error' in submission_response_data:
                raise Exception(submission_response_data['error'])
            submission_id = submission_response_data.get('submission_id')
            if not submission_id:
                if "detail" in submission_response_data:
                    raise Exception(f"Submission failed: {submission_response_data['detail']}")
                raise Exception("Failed to get submission ID from response.")
        except json.JSONDecodeError:
            if "csrftoken" in response_submit.text.lower() or "csrf" in response_submit.text.lower():
                raise Exception("Submission failed: CSRF token issue detected. Please try 'leetbuddy signin' again.")
            raise Exception(f"Failed to parse submission response. Status: {response_submit.status_code}")
        click.echo(f"Submission successful. ID: {submission_id}. Checking status...")
        status_url_template = f"{LEETCODE_BASE_URL}/submissions/detail/{{submission_id}}/check/"
        status_url = status_url_template.format(submission_id=submission_id)
        check_headers = {
            "Referer": f"{LEETCODE_BASE_URL}/problems/{problem_slug}/submissions/",
            "Accept": "application/json",
            "User-Agent": session.headers.get("User-Agent", ""),
            "X-CSRFToken": config['csrf_token']
        }
        max_retries = 30
        retries = 0
        while retries < max_retries:
            time.sleep(1)
            response_status = session.get(status_url, headers=check_headers)
            click.echo(f"Status poll response: {response_status.status_code}")  # DEBUG
            response_status.raise_for_status()
            status_data = response_status.json()
            click.echo(f"Status data: {status_data}")  # DEBUG
            if status_data.get('state') != 'PENDING' and status_data.get('state') != 'STARTED':
                break
            click.echo(f"Status: {status_data.get('state', 'Polling...')} (Attempt {retries + 1}/{max_retries})")
            retries += 1
        else:
            click.echo("Timed out waiting for submission result.")
            return
        click.echo("\n--- Submission Results ---")
        click.echo(f"Status: {status_data.get('status_display', 'Unknown')}")
        if status_data.get('status_display') == 'Accepted':
            click.echo(f"Runtime: {status_data.get('status_runtime', 'N/A')}")
            click.echo(f"Memory: {status_data.get('status_memory', 'N/A')}")
            click.echo(f"Runtime Percentile: {status_data.get('runtime_percentile', 'N/A')}%")
            click.echo(f"Memory Percentile: {status_data.get('memory_percentile', 'N/A')}%")
        elif status_data.get('compile_error'):
            click.echo(f"Compile Error:\n{status_data['compile_error']}")
        elif status_data.get('runtime_error'):
            click.echo(f"Runtime Error:\n{status_data['runtime_error']}")
        elif status_data.get('full_compile_error'):
            click.echo(f"Full Compile Error:\n{status_data['full_compile_error']}")
        elif status_data.get('full_runtime_error'):
            click.echo(f"Full Runtime Error:\n{status_data['full_runtime_error']}")
        if status_data.get('status_display') != 'Accepted' and status_data.get('last_testcase'):
            click.echo(f"Last Test Case:\n{status_data['last_testcase']}")
    except requests.exceptions.RequestException as e:
        click.echo(f"Network error during submission: {str(e)}")
    except Exception as e:
        click.echo(f"Error during submission: {str(e)}")
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    cli()

