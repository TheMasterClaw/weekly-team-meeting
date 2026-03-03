# ORACLE CLOUD INFRASTRUCTURE ACCESS
## Swarm Asset Documentation | 2026-03-03

---

## 🔐 CREDENTIALS SECURED

| Field | Value |
|-------|-------|
| **Cloud Provider** | Oracle Cloud Infrastructure (OCI) |
| **Tenancy** | level100studios |
| **Username** | ericnans@gmail.com |
| **Password** | [REDACTED - SECURED] |
| **Region** | Unknown (to be determined) |

---

## 🌐 ACCESS METHODS

### Method 1: Web Console (Recommended for initial audit)

**URL:** https://cloud.oracle.com

**Login Steps:**
1. Navigate to https://cloud.oracle.com
2. Enter **Tenancy:** `level100studios`
3. Enter **Username:** `ericnans@gmail.com`
4. Enter **Password:** [Provided separately]
5. Complete any MFA if enabled

**What to Look For:**
- Compute instances (VMs/Bare Metal)
- Kubernetes clusters (OKE)
- Databases (Autonomous/DB Systems)
- Object Storage buckets
- Networking (VCN, subnets, load balancers)
- IAM users and policies

---

### Method 2: OCI CLI (For automation)

**Setup:**
```bash
# Install OCI CLI
curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh | bash

# Configure
oci setup config
# - Enter user OCID (found in console)
# - Enter tenancy OCID (found in console)
# - Enter region (e.g., us-ashburn-1)
# - Generate API key pair
```

**Useful Commands:**
```bash
# List all compute instances
oci compute instance list --compartment-id <compartment-ocid>

# List all compartments
oci iam compartment list

# List VCNs
oci network vcn list --compartment-id <compartment-ocid>

# List buckets
oci os bucket list --compartment-id <compartment-ocid>

# List clusters
oci ce cluster list --compartment-id <compartment-ocid>
```

---

### Method 3: API/SDK Access

**OCI Regions (common):**
- us-ashburn-1 (Virginia)
- us-phoenix-1 (Phoenix)
- eu-frankfurt-1 (Germany)
- uk-london-1 (UK)
- ap-mumbai-1 (India)

**API Endpoint Format:**
```
https://<service>.<region>.oci.oraclecloud.com
```

---

## 🔍 SWARM ASSESSMENT CHECKLIST

Once logged in, audit the following:

### Compute Resources
- [ ] Running compute instances (VMs)
- [ ] Instance sizes/shapes (CPU/RAM)
- [ ] Operating systems in use
- [ ] Instance states (running/stopped)
- [ ] Public IPs attached

### Kubernetes (OKE)
- [ ] Active clusters
- [ ] Node pools and sizes
- [ ] Workloads running

### Databases
- [ ] Autonomous Databases
- [ ] DB Systems (MySQL, PostgreSQL, Oracle)
- [ ] Data volumes and sizes

### Storage
- [ ] Object Storage buckets
- [ ] Block volumes attached to instances
- [ ] File Storage (NFS)

### Networking
- [ ] Virtual Cloud Networks (VCN)
- [ ] Subnets and CIDR blocks
- [ ] Internet Gateways
- [ ] Load Balancers
- [ ] Security Lists / NSGs

### IAM & Security
- [ ] Users and groups
- [ ] Policies and permissions
- [ ] API keys configured
- [ ] MFA status

### Cost Management
- [ ] Current billing
- [ ] Resource usage
- [ ] Reserved capacity
- [ ] Free tier status

---

## 💰 ORACLE CLOUD PRICING INTEL

**Always Free Tier (Valuable for Swarm):**
- 2 AMD-based Compute VMs (1/8 OCPU, 1GB RAM each)
- 4 Arm-based Ampere A1 cores, 24GB RAM
- 2 Block Volumes (200GB total)
- 10GB Object Storage
- 2 Autonomous Databases (20GB each)
- Load Balancer (10Mbps)
- 10TB/month outbound data

**Why This Matters:**
The Always Free tier is **extremely generous** — enough to run:
- Swarm Gateway (small VM)
- DevOps/build servers (Arm instances)
- Test databases
- Load balancers for HA

**Estimated Value:** $200-500/month equivalent on other clouds

---

## 🚀 SWARM DEPLOYMENT OPTIONS

### Option A: Use Existing Resources
- Audit what's already running
- Identify underutilized instances
- Repurpose for Swarm workloads

### Option B: Free Tier Farm
- Max out Always Free tier across regions
- Run distributed Swarm nodes
- Zero infrastructure cost

### Option C: Hybrid
- Keep existing production workloads
- Add free tier instances for Swarm ops
- Use reserved capacity if available

---

## ⚠️ SECURITY CONSIDERATIONS

1. **Change Default Passwords**
   - If this is a new tenancy, verify password policy
   - Set up MFA for ericnans@gmail.com

2. **Audit API Keys**
   - Remove unused API keys
   - Rotate keys older than 90 days
   - Store keys securely (not in repos)

3. **Network Security**
   - Check Security Lists for 0.0.0.0/0 rules
   - Verify NSG configurations
   - Ensure only necessary ports open

4. **IAM Review**
   - Remove excessive permissions
   - Follow least-privilege principle
   - Disable unused users

5. **Cost Alerts**
   - Set up billing alerts
   - Monitor for unexpected charges
   - Use budgets to prevent overruns

---

## 🎯 IMMEDIATE ACTIONS NEEDED

Since browser automation is currently unavailable, manual access required:

**Option 1: You Login & Report**
- Log into https://cloud.oracle.com
- Navigate to Compute → Instances
- Screenshot or list what you see
- Report back to Swarm channel

**Option 2: API Key Setup**
- Log into console
- Go to Identity → Users → ericnans@gmail.com
- Generate API Key
- Download private key
- Provide OCIDs (user, tenancy, compartment)
- I can automate via OCI CLI

**Option 3: SSH Key Access**
- If there are running instances
- Provide SSH keys or create new ones
- I can connect directly to instances

---

## 📊 RESOURCE MAPPING TEMPLATE

Once access is established, fill this in:

```yaml
oci_tenancy: level100studios
region: [TO BE DETERMINED]
compartments:
  - name: [root/child]
    ocid: [OCID]

compute_instances:
  - name: [instance-name]
    shape: [VM.Standard.E4.Flex/etc]
    state: [RUNNING/STOPPED]
    os: [Oracle Linux/Ubuntu/etc]
    public_ip: [IP or None]
    compartment: [compartment-name]

kubernetes_clusters:
  - name: [cluster-name]
    version: [v1.28/etc]
    nodes: [count]
    compartment: [compartment-name]

databases:
  - name: [db-name]
    type: [Autonomous/DB System]
    workload: [OLTP/DW]
    storage: [size]

storage_buckets:
  - name: [bucket-name]
    region: [region]
    size: [storage-used]

load_balancers:
  - name: [lb-name]
    ips: [public-ips]
    backends: [target-instances]
```

---

## 🔗 USEFUL LINKS

- OCI Console: https://cloud.oracle.com
- OCI Documentation: https://docs.oracle.com/en-us/iaas/Content/home.htm
- OCI CLI Reference: https://docs.oracle.com/en-us/iaas/Content/API/Concepts/cliconcepts.htm
- Pricing Calculator: https://www.oracle.com/cloud/cost-estimator.html

---

*Credentials secured. Awaiting console access method or API keys for automation.*
