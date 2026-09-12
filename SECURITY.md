# Security Notes

- JWT is used for admin API operations.
- Passwords are stored as bcrypt hashes.
- Public read endpoints do not expose credentials.
- RHP/DRHP uploads require `application/pdf` and are size limited.
- Secrets are loaded from environment variables.
- CORS is restricted through `CORS_ORIGINS`.
- Production deployments must use HTTPS, a strong secret, non-demo credentials, private database networking, and durable object storage for uploaded documents.
