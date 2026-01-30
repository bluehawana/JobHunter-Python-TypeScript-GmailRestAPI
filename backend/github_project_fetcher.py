#!/usr/bin/env python3
"""
GitHub Project Fetcher
Reads real project information from github.com/bluehawana
Uses actual README content for authentic project descriptions
"""
import asyncio
import aiohttp
import re
import json
from typing import Dict, List, Optional
from pathlib import Path

class GitHubProjectFetcher:
    def __init__(self, username: str = "bluehawana"):
        self.username = username
        self.github_api_base = "https://api.github.com"
        self.github_raw_base = "https://raw.githubusercontent.com"
        
        # Key project repositories based on your actual GitHub projects
        self.priority_projects = [
            # Your most important recent projects
            "bluehawana.github.io",
            "ekorental-backend", 
            "epub-ttsreader-androidauto",
            "ekorental-next",
            "JobHunter-Python-TypeScript-GmailRestAPI",
            "smartmart-next-frontend",
            "carplayer-kotlin-androidauto",
            "smartmart-springboot-postgresql",
            "carbot-js-ai",
            "GothenburgTaxiPooling-Java-ReacNative",
            "FleetManager-Java-Mysql-Kafka-K8",
            "AnyNewsBot-Python-Epub-TTS-Podcast",
            "StockBot-Finviz-Python-Heroku",
            "AndroidAuto-Ebot",
            "rentingcarsystem",
            "SmtMart-Next-Go-Mysql-Strip"
        ]
        
        # Project categorization by focus areas
        self.project_focus_mapping = {
            "devops": [
                "FleetManager-Java-Mysql-Kafka-K8",  # Kubernetes, Kafka
                "kubernetes-certification-guide",
                "cicd-terraform"
            ],
            "fullstack": [
                "GothenburgTaxiPooling-Java-ReacNative",  # Java + React Native
                "JobHunter-Python-TypeScript-GmailRestAPI",  # Python + TypeScript
                "smartmart-springboot-postgresql",  # Spring Boot + DB
                "SmtMart-Next-Go-Mysql-Strip",  # Go + Next.js
                "ekorental-next",  # Next.js fullstack
                "rentingcarsystem"  # Full rental system
            ],
            "backend": [
                "smartmart-springboot-postgresql",  # Spring Boot
                "ekorental-backend",  # Backend service
                "StockBot-Finviz-Python-Heroku",  # Python backend
                "AnyNewsBot-Python-Epub-TTS-Podcast",  # Python API
                "API-Integration-H2DB-authentication",  # API backend
                "FleetManager-Java-Mysql-Kafka-K8"  # Java backend
            ],
            "frontend": [
                "smartmart-next-frontend",  # Next.js frontend
                "ekorental-next",  # Next.js app
                "bluehawana.github.io",  # Personal website
                "SmtMart-Next-Go-Mysql-Strip"  # Next.js frontend
            ],
            "android": [
                "carplayer-kotlin-androidauto",  # Kotlin Android Auto
                "epub-ttsreader-androidauto",  # Android Auto app
                "AndroidAuto-Ebot",  # Android Auto
                "carbot-js-ai"  # Car-related Android
            ],
            "api": [
                "AnyNewsBot-Python-Epub-TTS-Podcast",  # API integration
                "StockBot-Finviz-Python-Heroku",  # API service
                "API-Integration-H2DB-authentication",  # API auth
                "JobHunter-Python-TypeScript-GmailRestAPI"  # Gmail API
            ]
        }
    
    async def fetch_user_repositories(self) -> List[Dict]:
        """Fetch all repositories for the user"""
        
        url = f"{self.github_api_base}/users/{self.username}/repos"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        repos = await response.json()
                        print(f"✅ Found {len(repos)} repositories for {self.username}")
                        return repos
                    else:
                        print(f"❌ Failed to fetch repositories: {response.status}")
                        return []
        except Exception as e:
            print(f"❌ Error fetching repositories: {e}")
            return []
    
    async def fetch_readme_content(self, repo_name: str, branch: str = "main") -> Optional[str]:
        """Fetch README content from a specific repository"""
        
        # Try common README file names
        readme_files = ["README.md", "readme.md", "README.MD", "README.txt", "README"]
        
        for readme_file in readme_files:
            url = f"{self.github_raw_base}/{self.username}/{repo_name}/{branch}/{readme_file}"
            
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            content = await response.text()
                            print(f"✅ Found README for {repo_name}")
                            return content
            except Exception as e:
                continue
        
        # Try with master branch if main doesn't work
        if branch == "main":
            return await self.fetch_readme_content(repo_name, "master")
        
        print(f"❌ No README found for {repo_name}")
        return None
    
    def extract_project_info(self, readme_content: str, repo_name: str, repo_data: Dict) -> Dict:
        """Extract structured information from README content"""
        
        if not readme_content:
            return {}
        
        info = {
            "name": repo_name,
            "description": repo_data.get("description", ""),
            "url": repo_data.get("html_url", ""),
            "languages": [],
            "technologies": [],
            "features": [],
            "achievements": []
        }
        
        # Extract technologies mentioned in README
        tech_patterns = [
            r'\b(Java|JavaScript|Python|Kotlin|React|Angular|Vue|Spring|Docker|Kubernetes|AWS|Azure|GCP)\b',
            r'\b(PostgreSQL|MySQL|MongoDB|Redis|Elasticsearch)\b',
            r'\b(Jenkins|GitLab|GitHub Actions|CI/CD|DevOps)\b',
            r'\b(REST|API|GraphQL|Microservices)\b',
            r'\b(Stripe|Payment|Integration)\b'
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, readme_content, re.IGNORECASE)
            info["technologies"].extend(list(set(matches)))
        
        # Extract features from bullet points or numbered lists
        feature_patterns = [
            r'[*-]\s+([^\\n]+)',  # Bullet points
            r'\\d+\\.\s+([^\\n]+)',  # Numbered lists
            r'##\s+Features?\\s*\\n([^#]+)',  # Features section
            r'##\s+What.*does\\s*\\n([^#]+)'  # What it does section
        ]
        
        for pattern in feature_patterns:
            matches = re.findall(pattern, readme_content, re.MULTILINE | re.IGNORECASE)
            if matches:
                info["features"].extend([match.strip() for match in matches if len(match.strip()) > 10])
        
        # Extract achievements/results
        achievement_patterns = [
            r'(reduced.*by.*%)',
            r'(improved.*by.*%)',
            r'(increased.*by.*%)',
            r'(optimized.*performance)',
            r'(scalable.*architecture)',
            r'(real-time.*processing)'
        ]
        
        for pattern in achievement_patterns:
            matches = re.findall(pattern, readme_content, re.IGNORECASE)
            info["achievements"].extend(matches)
        
        # Clean up and deduplicate
        info["technologies"] = list(set([tech.title() for tech in info["technologies"]]))
        info["features"] = list(set(info["features"][:5]))  # Top 5 features
        info["achievements"] = list(set(info["achievements"][:3]))  # Top 3 achievements
        
        return info
    
    def categorize_projects_by_focus(self, projects: List[Dict]) -> Dict[str, List[Dict]]:
        """Categorize projects by focus areas using predefined mapping"""
        
        categorized = {
            "devops": [],
            "fullstack": [],
            "backend": [],
            "frontend": [],
            "android": [],
            "api": []
        }
        
        # Create reverse mapping for quick lookup
        project_to_focus = {}
        for focus, project_names in self.project_focus_mapping.items():
            for project_name in project_names:
                if project_name not in project_to_focus:
                    project_to_focus[project_name] = []
                project_to_focus[project_name].append(focus)
        
        for project in projects:
            project_name = project.get("name", "")
            
            # Check if project is in our predefined mapping
            if project_name in project_to_focus:
                for focus in project_to_focus[project_name]:
                    categorized[focus].append(project)
            else:
                # Fallback to keyword-based categorization
                technologies = set([tech.lower() for tech in project.get("technologies", [])])
                desc = project.get("description") or ""
                features = " ".join(project.get("features", []))
                description = (desc + " " + features).lower()
                
                # Auto-categorize based on keywords
                if any(keyword in description.lower() for keyword in ["kubernetes", "docker", "devops", "k8", "kafka"]):
                    categorized["devops"].append(project)
                elif any(keyword in description.lower() for keyword in ["android", "kotlin", "androidauto"]):
                    categorized["android"].append(project)
                elif any(keyword in description.lower() for keyword in ["api", "rest", "integration"]):
                    categorized["api"].append(project)
                elif any(keyword in description.lower() for keyword in ["react", "next", "frontend", "ui"]):
                    categorized["frontend"].append(project)
                elif any(keyword in description.lower() for keyword in ["spring", "backend", "server", "java"]):
                    categorized["backend"].append(project)
                elif any(keyword in description.lower() for keyword in ["fullstack", "full-stack", "end-to-end"]):
                    categorized["fullstack"].append(project)
        
        return categorized
    
    async def fetch_all_project_data(self) -> Dict[str, List[Dict]]:
        """Fetch and process all project data from GitHub"""
        
        print(f"🔍 Fetching project data from github.com/{self.username}")
        
        # Get all repositories
        repos = await self.fetch_user_repositories()
        
        if not repos:
            print("❌ No repositories found")
            return {}
        
        # Process priority projects first, then others
        projects = []
        processed_repos = set()
        
        # Process priority projects first
        for repo in repos:
            repo_name = repo["name"]
            
            if repo_name in self.priority_projects:
                print(f"🎯 Processing PRIORITY project: {repo_name}...")
                
                # Fetch README content
                readme_content = await self.fetch_readme_content(repo_name)
                
                # Extract project information
                project_info = self.extract_project_info(readme_content, repo_name, repo)
                
                if project_info:
                    projects.append(project_info)
                    processed_repos.add(repo_name)
                    print(f"✅ Priority project processed: {repo_name} - {len(project_info.get('technologies', []))} technologies, {len(project_info.get('features', []))} features")
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(0.3)
        
        # Process remaining repos (non-priority)
        for repo in repos:
            repo_name = repo["name"]
            
            # Skip if already processed, is fork, or very small
            if repo_name in processed_repos or repo["fork"] or repo["size"] < 10:
                continue
            
            # Limit additional repos to avoid rate limits
            if len(projects) >= 25:
                break
                
            print(f"📖 Processing additional: {repo_name}...")
            
            # Fetch README content
            readme_content = await self.fetch_readme_content(repo_name)
            
            # Extract project information
            project_info = self.extract_project_info(readme_content, repo_name, repo)
            
            if project_info and (project_info.get("technologies") or project_info.get("features")):
                projects.append(project_info)
                print(f"✅ Additional project processed: {repo_name}")
            
            # Small delay to avoid rate limiting
            await asyncio.sleep(0.5)
        
        # Categorize projects by focus areas
        categorized_projects = self.categorize_projects_by_focus(projects)
        
        # Print summary
        for role, role_projects in categorized_projects.items():
            print(f"📊 {role.title()}: {len(role_projects)} projects")
        
        return categorized_projects
    
    async def save_project_data(self, project_data: Dict, filename: str = "github_projects.json"):
        """Save project data to JSON file"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Project data saved to {filename}")
    
    async def load_project_data(self, filename: str = "github_projects.json") -> Dict:
        """Load project data from JSON file"""
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"📂 Project data loaded from {filename}")
            return data
        except FileNotFoundError:
            print(f"📁 No existing project data found, will fetch from GitHub")
            return {}

async def main():
    """Test GitHub project fetcher"""
    
    fetcher = GitHubProjectFetcher("bluehawana")
    
    # Fetch all project data
    project_data = await fetcher.fetch_all_project_data()
    
    # Save to file
    await fetcher.save_project_data(project_data)
    
    # Print summary
    print("\\n🎯 PROJECT SUMMARY:")
    print("=" * 50)
    
    for role, projects in project_data.items():
        print(f"\\n{role.upper()} PROJECTS ({len(projects)}):")
        for project in projects[:3]:  # Show top 3 per category
            print(f"  📁 {project['name']}")
            print(f"     🔧 Technologies: {', '.join(project['technologies'][:5])}")
            print(f"     ✨ Features: {len(project['features'])} identified")
            if project['achievements']:
                print(f"     🏆 Achievements: {project['achievements'][0]}")

if __name__ == "__main__":
    asyncio.run(main())