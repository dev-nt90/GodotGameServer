#!/usr/bin/env python3
"""Development server for Godot web exports.

Serves files with the correct MIME types, CORS headers for SharedArrayBuffer
support, and cache-busting headers to prevent stale assets during development.

Usage:
    python server.py [directory] [--port PORT]

    directory   Path to the Godot web export folder (default: current directory)
    --port PORT Port to serve on (default: 8008)
"""

import argparse
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from functools import partial


class GodotWebHandler(SimpleHTTPRequestHandler):
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".wasm": "application/wasm",
        ".pck": "application/octet-stream",
        ".js": "application/javascript",
    }

    def end_headers(self):
        # CORS headers required for SharedArrayBuffer (threaded builds)
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        # Cache-busting headers to prevent stale assets during development
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


def main():
    parser = argparse.ArgumentParser(description="Development server for Godot web exports")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to serve (default: current directory)")
    parser.add_argument("--port", type=int, default=8008, help="Port to serve on (default: 8008)")
    args = parser.parse_args()

    serve_dir = os.path.abspath(args.directory)
    if not os.path.isdir(serve_dir):
        print(f"Error: {serve_dir} is not a directory")
        return 1

    handler = partial(GodotWebHandler, directory=serve_dir)
    server = HTTPServer(("localhost", args.port), handler)

    print(f"Serving Godot web export from: {serve_dir}")
    print(f"http://localhost:{args.port}")
    print("Press Ctrl+C to stop")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down")
        server.shutdown()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
