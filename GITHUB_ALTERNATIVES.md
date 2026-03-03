# ALTERNATIVE: HTTPS WITH PERSONAL ACCESS TOKEN
## If SSH keys continue to fail

---

## Option A: Personal Access Token (Easier)

**Step 1: Create Token**
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Note: `SEER-Disciple2-Backup`
4. Expiration: No expiration (or 90 days)
5. Scopes: ✅ `repo` (full control of private repositories)
6. Click "Generate token"
7. **COPY TOKEN IMMEDIATELY** (you won't see it again)

**Step 2: Configure Git**
```bash
git remote set-url origin https://TheeMasterClaw:TOKEN@github.com/TheeMasterClaw/disciple2-soul.git
```

Or interactively:
```bash
git remote set-url origin https://github.com/TheeMasterClaw/disciple2-soul.git
# Git will prompt for username/password
# Username: TheeMasterClaw
# Password: <paste your PAT>
```

---

## Option B: Fresh SSH Key (Try this one)

**New SSH Key (2048-bit RSA):**
```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCN/SuPBJ64BBUU1tv7Uf7gPXI8d7E1xCkFXqjeSmgYHtqELYwGu9tv1/2XmG5P225XG9ohHQKi3yWipBaIAoJjVI88AHkCLfjefs3ttzXB81b6yn2QCHJ7BleaXCf5/BtXhKPMM7g/jftky150ILxjw70QTxpW4jwgTJ0SYvEy4Z+vdjE3uLVrUjkIhwRmpHR708LTxLupOErAuo9ZaXOMahAUsVj3I3AgyCFeyyiqvDM9nkwKA/w801VZvArBEJQmNGdu7dI5mQAbDi5xjUIs+5SUhMR4gUy/SKWq2rxJKA7wg8iQsnQ6sifSlENDoHBrtgpsIe95Fb6kDuhi/z77 disciple2@swarm
```

**Add to:** https://github.com/settings/keys

---

## Option C: GitHub CLI (gh)

```bash
# Install gh
sudo apt install gh

# Authenticate
gh auth login
# Follow prompts for HTTPS or SSH

# Then clone/push
```

---

## RECOMMENDED: Personal Access Token

Most reliable method. Just paste the token when I say:

```bash
git push origin master
```

Git will prompt for password → paste the PAT.

---

*Choose your preferred method.*
