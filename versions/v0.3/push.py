#!/usr/bin/env python3
import subprocess
import sys

def run_git(args):
    """Runs a git command with a list of args. No shell quoting issues."""
    result = subprocess.run(["git"] + args, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"\n❌ Error: git {' '.join(args)}")
        print(f"Details:\n{result.stderr.strip()}")
        sys.exit(1)
    return result.stdout.strip()

def main():
    print("🚀 =========================================")
    print("🚀  MELLOTECH GIT DEPLOYMENT HELPER")
    print("🚀 =========================================\n")

    # 1. Show current git status
    print("📋 Checking current status...")
    status = run_git(["status", "-s"])
    if not status:
        git_status_full = run_git(["status"])
        if "Your branch is ahead of" not in git_status_full:
            print("✅ No changes to commit or push. Everything is up to date!")
            sys.exit(0)

    if status:
        print("\nModified/New Files:")
        print(status)
        print("")

        # 2. Get commit message
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
        run_git(["add", "-A"])

        # 4. Commit changes
        print(f"💾 Committing changes: '{commit_message}'...")
        commit_out = run_git(["commit", "-m", commit_message])
        print(commit_out)

    # 5. Push to all configured remotes
    remotes = run_git(["remote"]).split()
    branch = run_git(["branch", "--show-current"])

    if not remotes:
        print("❌ No git remotes configured to push to!")
        sys.exit(1)

    for remote in remotes:
        print(f"\n⚡ Pushing to {remote.upper()} ({remote} branch: {branch})...")
        run_git(["push", remote, branch])
        print(f"✅ Successfully pushed to {remote}!")

    print("\n🚀 Deployment workflows triggered on active remotes!")

if __name__ == "__main__":
    main()
