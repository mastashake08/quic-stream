
# Set the URL for the offer endpoint (adjust the host and port if needed)


# Send the curl request with the passed JSON
curl -X POST http://localhost:8080/offer \
     -H "Content-Type: application/json" \
     -d $1

# Notify the user the request has been sent

