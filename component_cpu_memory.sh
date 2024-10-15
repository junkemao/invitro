# kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
# kubectl edit deployment metrics-server -n kube-system
# containers:
# - args:
#   - --cert-dir=/tmp
#   - --secure-port=4443
#   - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
#   - --kubelet-use-node-status-port
#   - --kubelet-insecure-tls  # Add this line

#!/bin/bash
# Define log file location
LOG_DIR=./data/out/"$(date +%s)"
mkdir -p "$LOG_DIR"
# Define the invoker command (replace with your actual command or script)
INVOKER_COMMAND="go run cmd/loader.go --config cmd/config.json"
# Function to monitor kubectl top metrics
monitor_kubectl_top() {
    while true; do
        # Get current timestamp and append it to the log
        echo "==========================" >> $LOG_DIR/cpu_logging.txt
        echo "Timestamp: $(date)" >> $LOG_DIR/cpu_logging.txt
        echo "==========================" >> $LOG_DIR/cpu_logging.txt
        
        # Fetch 'kubectl top' for pods and append to the log file
        kubectl top pods --all-namespaces >> $LOG_DIR/cpu_logging.txt
        # Optionally, you can fetch node metrics as well
        # kubectl top nodes >> $LOG_FILE
        # Wait for 30 seconds before fetching the metrics again
        sleep 10
    done
}
# Start monitoring kubectl top in the background
monitor_kubectl_top &  # Run the monitoring function in the background
MONITOR_PID=$!         # Store the PID of the monitoring process
# Run the invoker command in the foreground
echo "Running the invoker command..."
$INVOKER_COMMAND  # No background execution for the invoker; runs in the foreground
# sleep 600
# After the invoker command finishes, stop the monitoring process
kill $MONITOR_PID
echo "Monitoring stopped. Logs saved."
