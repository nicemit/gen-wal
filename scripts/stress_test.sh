#!/bin/bash
set -e

# Directory containing profiles
PROFILE_DIR="profiles/examples"

# Check if directory exists
if [ ! -d "$PROFILE_DIR" ]; then
    echo "❌ Profile directory not found: $PROFILE_DIR"
    exit 1
fi

echo "🎲 Selecting 4 random profiles from $PROFILE_DIR..."

# Find profiles, shuffle them, and pick top 4
# Using shuf for randomness
PROFILES=$(find "$PROFILE_DIR" -name "*.md" | shuf -n 4)

if [ -z "$PROFILES" ]; then
    echo "❌ No profiles found!"
    exit 1
fi

COUNT=1

# Loop through selected profiles
POSITIONS=("center" "bottom_right" "top_left" "bottom_center" "left_center")

echo "$PROFILES" | while read -r profile; do
    # Pick a random position
    RAND_POS=${POSITIONS[$RANDOM % ${#POSITIONS[@]}]}

    echo ""
    echo "==================================================="
    echo "🔄 Run $COUNT/4: Profile: $(basename "$profile") | Pos: $RAND_POS"
    echo "==================================================="
    
    # Run Gen-Wal with profile override and random text position
    python3 main.py --profile "$profile" --text-pos "$RAND_POS"
    
    # Optional cool-down/padding
    if [ $COUNT -lt 4 ]; then
        echo "⏳ Cooling down for 3 seconds..."
        sleep 3
    fi
    
    ((COUNT++))
done

echo ""
echo "✅ Sequence Complete!"
