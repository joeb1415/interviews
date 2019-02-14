# circuit_breaker

Run `remote_service` API on port 5001.
Run `local_service` API on port 5000. 
Make calls to remote_service with various wait times (slow responses) and status codes (server errors). Handle these in local_service via circuitbreaker methods.