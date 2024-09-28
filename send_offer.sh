#!/bin/bash

# Bash script to send a WebRTC offer using a POST request

# Check if the user passed a JSON string as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 '<json_string>'"
  exit 1
fi

# Store the passed JSON string in a variable
offer_json=$1

# Set the URL for the offer endpoint (adjust the host and port if needed)
url="https://localhost:8080/offer"

# Send the curl request with the passed JSON
curl -X POST "$url" \
     -H "Content-Type: application/json" \
     -d "$offer_json"

# Notify the user the request has been sent
echo "Offer sent to $url"
