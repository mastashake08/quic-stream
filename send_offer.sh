
# Set the URL for the offer endpoint (adjust the host and port if needed)
url="https://localhost:8080/offer"

# Send the curl request with the passed JSON
curl -X POST https://localhost:8080/offer \
     -H "Content-Type: application/json" \
     -d 

# Notify the user the request has been sent
echo "Offer sent to $url"
