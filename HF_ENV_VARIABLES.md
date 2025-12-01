# 🔐 Hugging Face Spaces Environment Variables

## Required Secrets (Add in Settings → Repository Secrets)

### 1. DATABASE_URL
**Purpose:** PostgreSQL connection string for external database

**Format:**
```
DATABASE_URL=postgresql://username:password@host:port/database
```

**Real Examples:**

**Render PostgreSQL:**
```
DATABASE_URL=postgresql://myuser:mypass123@dpg-abcd1234.oregon-postgres.render.com/mydb
```

**Neon PostgreSQL:**
```
DATABASE_URL=postgresql://myuser:mypass123@ep-xyz789.us-east-2.aws.neon.tech/mydb?sslmode=require
```

**⚠️ Important:**
- MUST start with `postgresql://` (NOT `postgres://`)
- The app auto-converts `postgres://` → `postgresql://`
- Include port if different from 5432
- Add `?sslmode=require` for secure connections

---

### 2. SECRET_KEY
**Purpose:** JWT token signing and session security

**Format:**
```
SECRET_KEY=your-super-secret-random-string-min-32-characters
```

**How to Generate:**
```bash
# Method 1: Using Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Method 2: Using OpenSSL
openssl rand -base64 32

# Method 3: Using pwgen
pwgen -s 64 1
```

**Example Output:**
```
SECRET_KEY=xK7mP9vR2nQ5wT8yU4eL6hG3jN0bM1cF5sA9dH2kV7pW4qX8zR6tY3nM5
```

**⚠️ Security Rules:**
- NEVER commit to Git
- Minimum 32 characters
- Use cryptographically secure random generation
- Different for each environment (dev/staging/prod)

---

## Optional Environment Variables

### PORT (Pre-configured)
**Default:** `7860` (Required by Hugging Face Spaces)
**DO NOT CHANGE** - The Dockerfile is already configured

### PYTHONUNBUFFERED (Pre-configured)
**Default:** `1`
**Purpose:** Real-time log output in HF Spaces

---

## How to Add Secrets in Hugging Face Spaces

1. **Navigate to Settings:**
   - Go to your Space: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE`
   - Click **Settings** (gear icon)

2. **Add Repository Secrets:**
   - Scroll to **Repository Secrets** section
   - Click **New Secret**
   
3. **Add DATABASE_URL:**
   - Name: `DATABASE_URL`
   - Value: `postgresql://user:pass@host:port/db`
   - Click **Add Secret**

4. **Add SECRET_KEY:**
   - Name: `SECRET_KEY`
   - Value: (your generated secret key)
   - Click **Add Secret**

5. **Verify:**
   - Secrets should show as `***` (hidden)
   - They will be injected at runtime
   - NOT visible in logs

---

## Verification Checklist

After adding secrets, verify:

- [ ] `DATABASE_URL` starts with `postgresql://`
- [ ] `DATABASE_URL` includes username and password
- [ ] `DATABASE_URL` has correct host and port
- [ ] `SECRET_KEY` is at least 32 characters
- [ ] `SECRET_KEY` is randomly generated
- [ ] Secrets are marked as **hidden** in Settings
- [ ] No secrets are in Git repository

---

## Testing Database Connection

**Before deploying**, test your database URL locally:

```bash
# Test with psql (if installed)
psql "postgresql://user:pass@host:port/db"

# Test with Python
python -c "
from sqlalchemy import create_engine
url = 'postgresql://user:pass@host:port/db'
engine = create_engine(url)
with engine.connect() as conn:
    print('✅ Connection successful!')
"
```

---

## Troubleshooting

### Error: "could not translate host name"
**Cause:** Invalid host in DATABASE_URL
**Fix:** Verify host from your database provider

### Error: "password authentication failed"
**Cause:** Wrong username or password
**Fix:** Check credentials in your database dashboard

### Error: "no pg_hba.conf entry for host"
**Cause:** Database firewall blocks external connections
**Fix:** Whitelist all IPs (0.0.0.0/0) in database settings

### Error: "JWT token invalid"
**Cause:** SECRET_KEY mismatch or expired token
**Fix:** Ensure SECRET_KEY is consistent and not changed

---

## Security Best Practices

✅ **DO:**
- Use HF Spaces Secrets for sensitive data
- Generate strong random keys
- Use SSL for database connections (`sslmode=require`)
- Rotate SECRET_KEY periodically
- Use different keys per environment

❌ **DON'T:**
- Hardcode secrets in code
- Commit `.env` files to Git
- Share SECRET_KEY publicly
- Use weak/predictable keys
- Reuse keys across projects

---

**Last Updated:** December 2025
