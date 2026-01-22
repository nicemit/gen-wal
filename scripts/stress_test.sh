#!/bin/bash
set -e

# Resolve Project Root (Parent of the directory containing this script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"
echo "📂 Working in: $PROJECT_ROOT"

# Directory containing profiles
PROFILE_DIR="profiles/examples"

# Check if directory exists
if [ ! -d "$PROFILE_DIR" ]; then
    echo "❌ Profile directory not found: $PROFILE_DIR"
    exit 1
fi

# Define 6 specific scenarios (Size:Position)
SCENARIOS=(
    "20:bottom_right"    # Smallest
    "35:bottom_center"   # Bit bigger
    "50:bottom_left"     # Bigger
    "80:center"          # Large
    "120:top_center"     # Massive
    "180:top_right"      # Biggest
)

TOTAL_RUNS=${#SCENARIOS[@]}
count=0

# Get all profiles into an array
mapfile -t ALL_PROFILES < <(find "$PROFILE_DIR" -name "*.md" | shuf)
NUM_PROFILES=${#ALL_PROFILES[@]}

echo "🔎 Found $NUM_PROFILES profiles."

if [ "$NUM_PROFILES" -eq 0 ]; then
    echo "❌ No profiles found in $PROFILE_DIR!"
    exit 1
fi

for scenario in "${SCENARIOS[@]}"; do
    count=$((count + 1))
    
    # Split scenario string using cut
    font_size=$(echo "$scenario" | cut -d: -f1)
    position=$(echo "$scenario" | cut -d: -f2)
    
    # Rotate through profiles
    profile_index=$(( (count - 1) % NUM_PROFILES ))
    profile="${ALL_PROFILES[$profile_index]}"
    
    echo ""
    echo "==================================================="
    echo "🔄 Run $count/$TOTAL_RUNS: Profile: $(basename "$profile")"
    echo "   📍 Position: $position | 🔠 Font Size: $font_size"
    echo "==================================================="
    
    # Run Gen-Wal
    if [ -f "venv/bin/python" ]; then
        venv/bin/python main.py --profile "$profile" --text-pos "$position" --font-size "$font_size"
    else
        python3 main.py --profile "$profile" --text-pos "$position" --font-size "$font_size"
    fi
    
    # Optional cool-down
    if [ $count -lt $TOTAL_RUNS ]; then
        echo "⏳ Cooling down for 3 seconds..."
        sleep 3
    fi
done

echo ""
echo "✅ Sequence Complete!"
