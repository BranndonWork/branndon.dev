#!/bin/bash

# Development server management script for branndon.dev
# Manages Python HTTP server for resume PDF generation

PROJECT_DIR="/Volumes/Storage/Dropbox/workspace/projects/branndon.dev/webroot"
PID_FILE="/tmp/branndon-dev-server.pid"
PORT_FILE="/tmp/branndon-dev-server.port"

# Find a random free port in range 8100-9000
find_free_port() {
    while true; do
        local port=$(( RANDOM % 900 + 8100 ))
        if ! lsof -i :$port > /dev/null 2>&1; then
            echo $port
            return 0
        fi
    done
}

# Get the recorded port (or empty if none saved)
get_saved_port() {
    if [ -f "$PORT_FILE" ]; then
        cat "$PORT_FILE"
    fi
}

# Get current server URL from saved port
get_server_url() {
    local port=$(get_saved_port)
    if [ -n "$port" ]; then
        echo "http://localhost:$port"
    fi
}

# Check if OUR server is running and responsive (by saved PID + port)
check_server() {
    local saved_pid=$([ -f "$PID_FILE" ] && cat "$PID_FILE")
    local saved_port=$(get_saved_port)

    if [ -z "$saved_pid" ] || [ -z "$saved_port" ]; then
        return 1
    fi

    # Verify the saved PID is still our process
    if ! ps -p "$saved_pid" > /dev/null 2>&1; then
        return 1
    fi

    # Verify it responds correctly
    if curl -s "http://localhost:$saved_port" | grep -q "resume-wrapper"; then
        return 0
    fi

    return 1
}

# Stop only OUR server (by saved PID — never touches other processes)
stop_dev() {
    echo "Stopping branndon.dev server..."
    if [ -f "$PID_FILE" ]; then
        local saved_pid=$(cat "$PID_FILE")
        if ps -p "$saved_pid" > /dev/null 2>&1; then
            echo "Stopping PID $saved_pid"
            kill -TERM "$saved_pid"
            sleep 1
        fi
        rm -f "$PID_FILE"
    fi
    rm -f "$PORT_FILE"
    echo "Server stopped"
}

# Start server in background on a free port
start_dev_bg() {
    local port=$(find_free_port)
    echo "Starting branndon.dev server on port $port..."
    cd "$PROJECT_DIR" && poetry run python -m http.server "$port" > /tmp/branndon-dev-server.log 2>&1 &
    local new_pid=$!
    echo "$new_pid" > "$PID_FILE"
    echo "$port" > "$PORT_FILE"
    sleep 2
    if curl -s "http://localhost:$port" | grep -q "resume-wrapper"; then
        echo "Server running: http://localhost:$port (PID $new_pid)"
    else
        echo "Warning: Server started (PID $new_pid, port $port) but not yet responsive"
    fi
}

# Print saved server URL (for use by other scripts)
get_url() {
    local url=$(get_server_url)
    if [ -n "$url" ]; then
        echo "$url"
    else
        echo "No server running" >&2
        return 1
    fi
}

# Status check
status() {
    if check_server; then
        local port=$(get_saved_port)
        local pid=$(cat "$PID_FILE")
        echo "Server running at http://localhost:$port (PID $pid)"
        return 0
    else
        echo "Server not running"
        return 1
    fi
}

# Ensure server is running — starts one if not, never kills anything else
ensure_running() {
    if check_server; then
        local port=$(get_saved_port)
        echo "Server already running at http://localhost:$port"
        return 0
    else
        start_dev_bg
    fi
}

# Main script logic
case "$1" in
    "start"|"bg"|"background")
        start_dev_bg
        ;;
    "stop")
        stop_dev
        ;;
    "status")
        status
        ;;
    "url")
        get_url
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
        echo "Usage: $0 {start|stop|status|url|ensure|restart}"
        echo "  start   - Start server in background on a free port"
        echo "  stop    - Stop OUR server (never touches other processes)"
        echo "  status  - Check if our server is running"
        echo "  url     - Print the current server URL"
        echo "  ensure  - Start server if not already running (default)"
        echo "  restart - Stop and restart"
        ;;
esac