# Create a list of 2-element lists
declare -a list_of_rps=(
    "100"
)

# Path to the configuration JSON file
config_file="cmd/config.json"

# Function to modify the JSON configuration
modify_config() {
    local rps=$1

    # Construct the new TracePath value
    local trace_path="data/traces/example2/$rps"  # Adjust this as needed for your desired format

    # Update the TracePath in the config file
    jq --arg path "$trace_path" \
       '.TracePath = $path' "$config_file" > tmp.json && mv tmp.json "$config_file"
}

# Iterate over each pair
for rps in "${list_of_rps[@]}"; do
    # Run the Python script with the two elements
    echo "Running python_script.py with inputs: $rps"
    python3 generate_function_chains_rps.py "$rps"

    echo "Modifying config.json with $rps"
    modify_config "$rps"

    echo "Running loader"
    ./component_cpu_memory.sh
done