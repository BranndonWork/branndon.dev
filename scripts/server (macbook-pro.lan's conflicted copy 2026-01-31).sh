#!/bin/bash

# Development server management script for branndon.dev
# Manages Python HTTP server for resume PDF generation

PROJECT_DIR="/Volumes/Storage/Dropbox/workspace/projects/branndon.dev/webroot"
PID_FILE="$PROJECT_DIR/../.dev.pid"
SERVER_PORT=8000
SERVER_URL="http://localhost:$SERVER_PORT"

# Function to check if server is running and responsive
check_server() {
    if curl -s "$SERVER_URL" | grep -q "resume-wrapper"; then
        return 0  # Server is running and responsive
    else
        return 1  # Server not running or not responsive
    fi
}

# Function to gracefully stop our dev server
stop_dev() {
    echo "Stopping branndon.dev server..."
    
    # Check if we have a saved PID
    if [ -f "$PID_FILE" ]; then
        local saved_pid=$(cat "$PID_FILE")
        if ps -p $saved_pid > /dev/null 2>&1; then
            echo "Gracefully stopping PID $saved_pid"
            kill -TERM $saved_pid
            sleep 2
            # If still running, force kill
            if ps -p $saved_pid > /dev/null 2>&1; then
                kill -KILL $saved_pid
            fi
        fi
        rm -f "$PID_FILE"
    fi
    
    # Find Python HTTP server processes on our port
    local server_pids=$(lsof -ti:$SERVER_PORT 2>/dev/null)
    if [ ! -z "$server_pids" ]; then
        for pid in $server_pids; do
            if ps -p $pid > /dev/null 2>&1; then
                echo "Stopping server process PID $pid on port $SERVER_PORT"
                kill -TERM $pid
            fi
        done
        sleep 1
    fi
}

# Function to start dev server
start_dev() {
    echo "Starting branndon.dev HTTP server on port $SERVER_PORT..."
    cd "$PROJECT_DIR" && python3 -m http.server $SERVER_PORT
}

# Function to start dev server in background
start_dev_bg() {
    stop_dev
    echo "Starting branndon.dev server in background on port $SERVER_PORT..."
    cd "$PROJECT_DIR" && python3 -m http.server $SERVER_PORT > ../dev.log 2>&1 &
    local new_pid=$!
    echo $new_pid > "$PID_FILE"
    echo "Server started with PID $new_pid"
    echo "Server URL: $SERVER_URL"
    
    # Wait a moment and verify server is responsive
    sleep 2
    if check_server; then
        echo "Server is running and responsive"
    else
        echo "Warning: Server may not be fully ready yet"
    fi
}

# Function to get server status and URL
status() {
    if check_server; then
        echo "Server is running and responsive at $SERVER_URL"
        if [ -f "$PID_FILE" ]; then
            local saved_pid=$(cat "$PID_FILE")
            echo "PID: $saved_pid"
        fi
        return 0
    else
        echo "Server is not running or not responsive"
        return 1
    fi
}

# Function to ensure server is running (main use case)
ensure_running() {
    if check_server; then
        echo "Server already running at $SERVER_URL"
        return 0
    else
        echo "Starting server..."
        start_dev_bg
        return $?
    fi
}

# Main script logic
case "$1" in
    "start")
        start_dev
        ;;
    "stop"|"kill")
        stop_dev
        ;;
    "bg"|"background")
        start_dev_bg
        ;;
    "status")
        status
        ;;
    "ensure"|"")
        ensure_running
        ;;
    "restart")
        stop_dev
        sleep 1
        start_dev_bg
        ;;
    *)
        echo "Usage: $0 {start|stop|bg|status|ensure|restart}"
        echo "  start     - Start server in foreground"
        echo "  stop      - Stop server"
        echo "  bg        - Start server in background"
        echo "  status    - Check server status"
        echo "  ensure    - Ensure server is running (default)"
        echo "  restart   - Restart server"
        ;;
esac