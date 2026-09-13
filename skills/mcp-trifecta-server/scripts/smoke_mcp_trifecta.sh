#!/usr/bin/env bash
#
# Smoke Tests for Trifecta MCP Server - Reproducible Evidence
#
# These tests provide concrete evidence that MCP server works.
# Run them to verify implementation before committing.
#

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_PATH="${SERVER_PATH:-$(cd "${SCRIPT_DIR}/.." && pwd)}"
SERVER_SCRIPT="${SERVER_PATH}/server.py"
TEST_SEGMENT="${TEST_SEGMENT:-${SERVER_PATH}}"

# Colors
GREEN="\033[92m"
RED="\033[91m"
YELLOW="\033[93m"
RESET="\033[0m"

echo -e "${YELLOW}Trifecta MCP Server - Smoke Tests${RESET}"
echo "================================================"
echo "Server: ${SERVER_PATH}"
echo "Segment: ${TEST_SEGMENT}"
echo ""

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function
run_test() {
    local name="$1"
    local request="$2"
    local expected="$3"
    local test_num="$4"
    local mode="$5"  # mock or real

    echo -n "Test ${test_num}: ${name}..."
    echo "Request: ${request}"
    echo "Mode: ${mode}"

    # Send request and capture response
    response=$(echo "${request}" | python3 "${SERVER_SCRIPT}" 2>&1)
    local exit_code=$?

    # Check response
    if echo "${response}" | grep -q "${expected}"; then
        echo -e " ${GREEN}✓ PASS${RESET}"
        echo "Expected: ${expected}"
        echo "Response: ${response}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e " ${RED}✗ FAIL${RESET}"
        echo "Expected: ${expected}"
        echo "Got: ${response}"
        echo ""
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

echo "Pre-check: Verifying server file..."
if [ ! -f "${SERVER_SCRIPT}" ]; then
    echo -e "${RED}✗ FAIL${RESET} Server file not found: ${SERVER_SCRIPT}"
    exit 1
fi

echo "Pre-check: Verifying segment..."
if [ ! -d "${TEST_SEGMENT}" ]; then
    echo -e "${RED}✗ FAIL${RESET} Segment directory not found: ${TEST_SEGMENT}"
    exit 1
fi

echo ""
echo "================================================"
echo "Test 1: tools/list (Mock mode)"
echo "================================================"
run_test \
    "tools/list (mock)" \
    '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
    'tools' \
    1 \
    "mock"

echo ""
echo "================================================"
echo "Test 2: tools/list - validate structure (Mock mode)"
echo "================================================"
run_test \
    "tools/list structure (mock)" \
    '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
    'ctx_search' \
    2 \
    "mock"

echo ""
echo "================================================"
echo "Test 3: ctx_search - validation (empty query, Mock mode)"
echo "================================================"
run_test \
    "ctx_search validation (empty query, mock)" \
    '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"ctx_search","arguments":{"query":""}}}' \
    'query must be at least 3 chars' \
    3 \
    "mock"

echo ""
echo "================================================"
echo "Test 4: ctx_search - validation (query too short, Mock mode)"
echo "================================================"
run_test \
    "ctx_search validation (short query, mock)" \
    '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"ctx_search","arguments":{"query":"ab"}}}' \
    'query must be at least 3 chars' \
    4 \
    "mock"

echo ""
echo "================================================"
echo "Test 5: ctx_search - validation (query too long, Mock mode)"
echo "================================================"
LONG_QUERY=$(printf 'a%.0s' {1..501})
run_test \
    "ctx_search validation (long query, mock)" \
    "{\"jsonrpc\":\"2.0\",\"id\":5,\"method\":\"tools/call\",\"params\":{\"name\":\"ctx_search\",\"arguments\":{\"query\":\"${LONG_QUERY}\"}}}" \
    'query must be <= 500 chars' \
    5 \
    "mock"

echo ""
echo "================================================"
echo "Test 6: ctx_search - validation (k too small, Mock mode)"
echo "================================================"
run_test \
    "ctx_search validation (k too small, mock)" \
    '{"jsonrpc":"2.0","id":6,"method":"tools/call","params":{"name":"ctx_search","arguments":{"query":"test","k":0}}}' \
    'k must be between 1 and 100' \
    6 \
    "mock"

echo ""
echo "================================================"
echo "Test 7: ctx_search - validation (k too large, Mock mode)"
echo "================================================"
run_test \
    "ctx_search validation (k too large, mock)" \
    '{"jsonrpc":"2.0","id":7,"method":"tools/call","params":{"name":"ctx_search","arguments":{"query":"test","k":101}}}' \
    'k must be between 1 and 100' \
    7 \
    "mock"

echo ""
echo "================================================"
echo "Test 8: ctx_get - validation (empty ids, Mock mode)"
echo "================================================"
run_test \
    "ctx_get validation (empty ids, mock)" \
    '{"jsonrpc":"2.0","id":8,"method":"tools/call","params":{"name":"ctx_get","arguments":{"ids":[]}}}' \
    'ids must be a non-empty array' \
    8 \
    "mock"

echo ""
echo "================================================"
echo "Test 9: ctx_get - validation (too many ids, Mock mode)"
echo "================================================"
MANY_IDS=$(python3 -c "import json; print(json.dumps(['id' + str(i) for i in range(51)]))")
run_test \
    "ctx_get validation (too many ids, mock)" \
    "{\"jsonrpc\":\"2.0\",\"id\":9,\"method\":\"tools/call\",\"params\":{\"name\":\"ctx_get\",\"arguments\":{\"ids\":${MANY_IDS}}}}" \
    'ids max length is 50' \
    9 \
    "mock"

echo ""
echo "================================================"
echo "Test 10: ctx_get - validation (invalid mode, Mock mode)"
echo "================================================"
run_test \
    "ctx_get validation (invalid mode, mock)" \
    '{"jsonrpc":"2.0","id":10,"method":"tools/call","params":{"name":"ctx_get","arguments":{"ids":["id1"],"mode":"invalid"}}}' \
    'mode must be one of raw|excerpt|skeleton' \
    10 \
    "mock"

echo ""
echo "================================================"
echo "Test 11: ctx_get - validation (invalid chunk ID format, Mock mode)"
echo "================================================"
run_test \
    "ctx_get validation (empty id string, mock)" \
    '{"jsonrpc":"2.0","id":11,"method":"tools/call","params":{"name":"ctx_get","arguments":{"ids":[""]}}}' \
    'id must not be empty' \
    11 \
    "mock"

echo ""
echo "================================================"
echo "Test 12: Unknown tool error (Mock mode)"
echo "================================================"
run_test \
    "Unknown tool" \
    '{"jsonrpc":"2.0","id":12,"method":"tools/call","params":{"name":"unknown_tool","arguments":{}}}' \
    "Method not found: unknown tool 'unknown_tool'" \
    12 \
    "mock"

echo ""
echo "================================================"
echo "Summary"
echo "================================================"
echo "Tests Passed: ${TESTS_PASSED}"
echo "Tests Failed: ${TESTS_FAILED}"
echo ""
echo "Note: Tests run in MOCK mode by default."
echo "To test with REAL Trifecta CLI:"
echo "  python3 ${SERVER_SCRIPT} --mode=real"
echo ""

if [ ${TESTS_FAILED} -gt 0 ]; then
    echo -e "${RED}✗ SMOKE TESTS FAILED${RESET}"
    echo "Failed ${TESTS_FAILED} out of $((TESTS_PASSED + TESTS_FAILED)) tests"
    exit 1
else
    echo -e "${GREEN}✓ ALL SMOKE TESTS PASSED${RESET}"
    echo "All ${TESTS_PASSED} tests passed successfully"
    echo ""
    echo "Next step: Test with Real mode:"
    echo "  python3 ${SERVER_SCRIPT} --mode=real"
    exit 0
fi
