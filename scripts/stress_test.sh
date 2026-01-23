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
    "60:bottom_right"    # Large
    "80:bottom_center"   # Hero
    "40:top_right"       # Medium
    "100:center"         # Statement (Big)
    "25:bottom_left"     # Subtle
    "50:bottom_right"    # Standard
)

TOTAL_RUNS=${#SCENARIOS[@]}
count=0

# Helper function to get full path
get_profile() { echo "$PROJECT_ROOT/$PROFILE_DIR/$1"; }

# Explicitly selected profiles for demo
ALL_PROFILES=(
    "$(get_profile "stoic.md")"
    "$(get_profile "deep_work.md")"
    "$(get_profile "builder.md")"
    "$(get_profile "zen.md")"
)
NUM_PROFILES=${#ALL_PROFILES[@]}

echo "🔎 Selected $NUM_PROFILES curated profiles."

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
        venv/bin/python main.py --profile "$profile" \
            --text-pos "$position" \
            --font-size "$font_size" \
            --watermark-pos bottom_center \
            --watermark-opacity 30
    else
        python3 main.py --profile "$profile" \
            --text-pos "$position" \
            --font-size "$font_size" \
            --watermark-pos bottom_center \
            --watermark-opacity 30
    fi
    
    # Optional cool-down
    if [ $count -lt $TOTAL_RUNS ]; then
        echo "⏳ Cooling down for 3 seconds..."
        sleep 3
    fi
done

echo ""
echo "✅ Sequence Complete!"
