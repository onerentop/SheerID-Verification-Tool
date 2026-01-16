#!/bin/bash
# SheerID Verification Tool Entrypoint
# Usage: docker run sheerid-tool <tool-name> <url> [--proxy <proxy>]

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_banner() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║      SheerID Verification Tool - Docker Edition        ║"
    echo "║              github.com/ThanhNguyxn                    ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_help() {
    print_banner
    echo -e "${GREEN}Available Tools:${NC}"
    echo "  spotify     - Spotify Premium Student Verification"
    echo "  youtube     - YouTube Premium Student Verification"
    echo "  one         - Google One (Gemini) Student Verification"
    echo "  boltnew     - Bolt.new Teacher Verification"
    echo "  k12         - ChatGPT Plus K-12 Teacher Verification"
    echo "  veterans    - ChatGPT Plus Military Verification"
    echo "  perplexity  - Perplexity Student Verification"
    echo "  canva       - Canva Education Teacher Verification"
    echo ""
    echo -e "${GREEN}Usage:${NC}"
    echo "  docker run sheerid-tool <tool> <url> [options]"
    echo ""
    echo -e "${GREEN}Examples:${NC}"
    echo "  docker run sheerid-tool one \"https://services.sheerid.com/verify/...?verificationId=xxx\""
    echo "  docker run sheerid-tool spotify \"URL\" --proxy http://user:pass@host:port"
    echo "  docker run -e PROXY=http://host:port sheerid-tool youtube \"URL\""
    echo ""
    echo -e "${GREEN}Environment Variables:${NC}"
    echo "  PROXY       - Proxy server (http://user:pass@host:port)"
    echo "  TOOL        - Default tool to use (default: one)"
    echo ""
    echo -e "${GREEN}Anti-Detection Info:${NC}"
    python /app/anti_detect.py 2>/dev/null || echo "  Module loaded successfully"
}

# Map tool names to directories
get_tool_path() {
    case "$1" in
        spotify)     echo "spotify-verify-tool" ;;
        youtube)     echo "youtube-verify-tool" ;;
        one|gemini)  echo "one-verify-tool" ;;
        boltnew)     echo "boltnew-verify-tool" ;;
        k12)         echo "k12-verify-tool" ;;
        veterans|military) echo "veterans-verify-tool" ;;
        perplexity)  echo "perplexity-verify-tool" ;;
        canva)       echo "canva-teacher-tool" ;;
        *)           echo "" ;;
    esac
}

# Main logic
if [ $# -eq 0 ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    print_help
    exit 0
fi

TOOL_NAME="$1"
shift

TOOL_PATH=$(get_tool_path "$TOOL_NAME")

if [ -z "$TOOL_PATH" ]; then
    echo -e "${RED}Error: Unknown tool '$TOOL_NAME'${NC}"
    echo "Run with --help to see available tools"
    exit 1
fi

if [ ! -d "/app/$TOOL_PATH" ]; then
    echo -e "${RED}Error: Tool directory not found: $TOOL_PATH${NC}"
    exit 1
fi

print_banner
echo -e "${GREEN}Running:${NC} $TOOL_NAME"
echo -e "${GREEN}Path:${NC} /app/$TOOL_PATH"

# Build command
CMD="python /app/$TOOL_PATH/main.py"

# Add proxy from environment if set and not already in args
if [ -n "$PROXY" ] && [[ ! " $* " =~ " --proxy " ]]; then
    echo -e "${YELLOW}Using proxy from environment: ${PROXY:0:30}...${NC}"
    CMD="$CMD --proxy $PROXY"
fi

# Execute
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
exec $CMD "$@"
