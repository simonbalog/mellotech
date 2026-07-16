#!/usr/bin/env python3
import subprocess
import sys

def run_command(cmd):
    """Runs a shell command and returns output, raising an exception on error."""
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"\n❌ Error executing command: {cmd}")
        print(f"Details:\n{result.stderr.strip()}")
        sys.exit(1)
    return result.stdout.strip()

def main():
    print("🚀 =========================================")
    print("🚀  MELLOTECH GIT DEPLOYMENT HELPER")
    print("🚀 =========================================\n")

    # 1. Show current git status
    print("📋 Checking current status...")
    status = run_command("git status -s")
    if not status:
        print("✅ No changes to commit. Everything is up to date!")
        sys.exit(0)
    
    print("\nModified/New Files:")
    print(status)
    print("")

    # 2. Get commit message
    # Check if message was provided as command line arguments
    if len(sys.argv) > 1:
        commit_message = " ".join(sys.argv[1:])
    else:
        try:
            commit_message = input("💬 Enter commit message: ").strip()
        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")
            sys.exit(0)
            
        if not commit_message:
            commit_message = "Update Mellotech website"
            print(f"⚠️ No message entered. Using default: '{commit_message}'")

    # 3. Add all changes
    print("\n📦 Staging changes (git add -A)...")
    run_command("git add -A")

    # 4. Commit changes
    print(f"💾 Committing changes: '{commit_message}'...")
    commit_out = run_command(f'git commit -m "{commit_message}"')
    print(commit_out)

    # 5. Push to remote
    # Find current branch name
    branch = run_command("git branch --show-current")
    print(f"\n⚡ Pushing to GitHub (origin {branch})...")
    push_out = run_command(f"git push origin {branch}")
    print("✅ Pushed successfully!")
    print("\n🚀 Deploying to GitHub Pages started via GitHub Actions.")

if __name__ == "__main__":
    main()
