Development server for Godot web exports.

Serves files with the correct MIME types, CORS headers for SharedArrayBuffer
support, and cache-busting headers to prevent stale assets during development.

Usage:
    python server.py [directory] [--port PORT]

    directory   Path to the Godot web export folder (default: current directory)
    --port PORT Port to serve on (default: 8008)
