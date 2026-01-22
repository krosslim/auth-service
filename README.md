# auth-service

## generate pem

```
# RSA256
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem

ls -l private.pem public.pem

cp ~/private.pem ~/public.pem .../auth-service/

# private key for hash of rehresh token
openssl rand -base64 32 
```

