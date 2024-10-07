#!/bin/bash

# Create a list of 2-element lists
declare -a list_of_pairs=(
    "2,200"
)

# Path to the configuration JSON file
config_file="cmd/config.json"

# Function to modify the JSON configuration
modify_config() {
    local combined_string=$1

    # Construct the new TracePath value
    local trace_path="data/traces/example2/$combined_string"  # Adjust this as needed for your desired format

    # Update the TracePath in the config file
    jq --arg path "$trace_path" \
       '.TracePath = $path' "$config_file" > tmp.json && mv tmp.json "$config_file"
}

# Iterate over each pair
for pair in "${list_of_pairs[@]}"; do
    # Split the pair into two elements
    IFS=',' read -r element1 element2 <<< "$pair"

    # Run the Python script with the two elements
    echo "Running python_script.py with inputs: $element1, $element2"
    python3 generate_function_chains.py "$element1" "$element2"

    # Modify the config JSON with the current pair
    combined_string="${element1}_${element2}"
    echo "Modifying config.json with $element1 and $element2"
    modify_config "$combined_string"

    echo "Running loader"
    go run cmd/loader.go --config cmd/config.json
done