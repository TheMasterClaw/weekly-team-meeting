# LEVEL100STUDIOS SSH ACCESS REPORT
## Server Reconnaissance | 2026-03-03

---

## 🔐 CREDENTIALS SECURED
- **SSH Key:** RSA 2048-bit, fingerprint SHA256:h3HmcFAuTNLX28Qvb01hMPgaAY2TehJekyp3zmr7sK8
- **Location:** ~/.ssh/level100studios_key (chmod 600)
- **Generated:** 2026-03-03 (per public key comment)

---

## 🔍 CONNECTION TESTS

### SSH Port Scan Results
| Target | Port | Status |
|--------|------|--------|
| level100studios.com | 22 | ❌ Network unreachable |
| 34.120.137.41 | 22 | ❌ Closed |
| level100studios.com | 2222 | ❌ Closed |
| level100studios.com | 2022 | ❌ Closed |
| level100studios.com | 1022 | ❌ Closed |
| level100studios.com | 8022 | ❌ Closed |
| level100studios.com | 443 | ✅ HTTPS (website) |

### Username Attempts
Tested: ubuntu, ec2-user, root, admin, eric, deploy, level100
Result: All failed - SSH port not accessible

---

## 🤔 ASSESSMENT

**SSH is not publicly accessible** on standard ports. Possible scenarios:

### Scenario A: Firewall/VPN Protected
Server requires:
- VPN connection first
- Specific source IP allowlist
- Corporate network access

### Scenario B: Non-Standard Setup
- SSH over WebSocket/HTTPS tunnel
- Container/VPC internal only
- Requires jump host/bastion

### Scenario C: Different Host
- Key is for a different server (not level100studios.com)
- Could be AWS EC2, DigitalOcean, Vultr, etc.
- Different hostname/IP required

### Scenario D: Cloud Provider Metadata
Key format suggests cloud provider:
- AWS EC2: Usually starts with "ssh-rsa ... amazon" 
- DigitalOcean: Usually includes "digitalocean"
- Generic: "ssh-key-2026-03-03" = manually generated

---

## ✅ REQUIRED INFO TO PROCEED

**Need clarification on access method:**

1. **Is there a VPN** required to connect?
   - If yes: Provide VPN config/credentials

2. **Is SSH on a different port** (not 22/2222)?
   - If yes: What port?

3. **Is this a different hostname/IP?**
   - AWS EC2: Check AWS console for public IP
   - DigitalOcean: Check droplet IP
   - Other: Provide correct hostname

4. **Is this a container/development environment?**
   - Docker: Use `docker exec` locally
   - Kubernetes: Need kubectl context
   - LXC/LXD: Different access method

5. **Jump host required?**
   - If yes: Provide bastion/jump host details

---

## 🔒 SECURITY NOTE

SSH key is secured and ready to use once correct access method is identified.

**Will NOT:**
- Attempt brute force on ports
- Try to bypass firewalls
- Use the key on unrelated systems

**Will DO:**
- Connect once proper channel is confirmed
- Audit server security
- Document findings for Swarm

---

*Awaiting access method clarification.*
