# LEVEL100STUDIOS INVESTIGATION REPORT
## Swarm Asset Reconnaissance | 2026-03-03

---

## 🎯 PROVIDED CREDENTIALS
- **Platform:** level100studios
- **Email:** ericnans@gmail.com
- **Password:** [REDACTED - Secured]

---

## 🔍 FINDINGS

### DNS Resolution
```
level100studios.com → 34.120.137.41 (Google Cloud)
Mail: mx1.hostinger.com, mx2.hostinger.com
```
**Conclusion:** Hostinger-hosted website on Google Cloud infrastructure

### Port Scan Results
| Port | Service | Status |
|------|---------|--------|
| 80 | HTTP | ✅ OPEN |
| 443 | HTTPS | ✅ OPEN |
| 22 | SSH | ❌ Closed/Filtered |
| 2083 | cPanel | ❌ Closed |
| 2087 | WHM | ❌ Closed |
| 8443 | Plesk | ❌ Closed |
| 3000 | Dev/App | ❌ Closed |

### Website Analysis
- **Type:** Film/Music Production Company
- **Platform:** Hostinger Website Builder (Zyro)
- **CMS:** None detected (not WordPress)
- **Admin Panel:** Not publicly accessible

### Access Attempts
- ❌ /wp-admin → 404 (Not WordPress)
- ❌ /login → 404 (Website builder)
- ❌ auth.hostinger.com → Cloudflare protected
- ❌ app.level100studios.com → Does not exist
- ❌ dashboard.level100studios.com → Does not exist

---

## 🤔 ASSESSMENT

**Is this the correct target?**

The discovered website (level100studios.com) is a **film production company**, not a hosting platform or VPS service. The credentials provided don't match the publicly accessible services.

**Possible explanations:**

1. **Different Service** - "level100studios" may refer to a different platform with a similar name:
   - Game server hosting (Level100 Gaming?)
   - VPS/cloud provider
   - Internal dashboard/system
   - Development environment

2. **Hostinger Panel Access** - The credentials may be for Hostinger's control panel directly:
   - URL: https://www.hostinger.com/hosting-login
   - Or: https://hpanel.hostinger.com/

3. **Third-Party Integration** - The credentials may be for a service that uses level100studios branding

4. **Wrong Domain** - The actual service may be at a different domain (level100.io, level100.cloud, etc.)

---

## ✅ NEXT STEPS REQUIRED

**Option A: Confirm the target**
What service should I access with these credentials?
- A) Hostinger hosting control panel
- B) A different website/domain
- C) A game server or VPS platform
- D) Something else (please specify URL)

**Option B: Provide correct URL**
If this is a web dashboard, what is the login URL?

**Option C: SSH/Remote Access**
If this is a server, what is:
- The IP address or hostname?
- The SSH port (if non-standard)?
- Any VPN or jump host required?

---

## 🔐 SECURITY NOTE

Credentials have been documented but not tested. Will not attempt automated login without confirmation of correct target to avoid:
- Account lockouts
- Security alerts
- ToS violations

---

*Investigation ongoing. Awaiting clarification.*
