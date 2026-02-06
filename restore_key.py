import subprocess
import os

def restore_file(commit_path, output_path):
    print(f"Restoring {commit_path} to {output_path}...")
    try:
        # Get bytes from git
        result = subprocess.run(['git', 'show', commit_path], capture_output=True, check=True)
        content_bytes = result.stdout
        
        # Determine if it's already UTF-16 or something weird and fix it
        # Actually, git show should give raw bytes as stored.
        # Let's just write them out.
        with open(output_path, 'wb') as f:
            f.write(content_bytes)
        print(f"✅ Success! Wrote {len(content_bytes)} bytes.")
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    restore_file("c46e005:serviceAccountKey.json", "serviceAccountKey.json")
