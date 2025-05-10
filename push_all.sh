# Push to GitHub
echo "Pushing to GitHub (origin)..."
git push -u origin main

# Push to DagsHub
echo "Pushing to DagsHub (dagshub)..."
git push dagshub main

echo "✅ Push complete to both remotes."