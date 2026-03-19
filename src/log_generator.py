"""
Wissen Infotech SIEM Project
Log Generator — mimics Microsoft Sentinel log table structures
Tables: SigninLogs, SecurityEvent, AzureActivity, NetworkFlow
"""

import random
import time
import json
import uuid
from datetime import datetime, timezone
from faker import Faker

fake = Faker()

# ── Simulated users and IPs ──────────────────────────────────────────────────
USERS = [
    "alice.sharma@wissen-client.com",
    "bob.mehta@wissen-client.com",
    "carol.patel@wissen-client.com",
    "dave.kumar@wissen-client.com",
    "admin@wissen-client.com",
]

INTERNAL_IPS  = ["192.168.1.10","192.168.1.11","192.168.1.20","10.0.0.5","10.0.0.8"]
EXTERNAL_IPS  = ["185.220.101.34","45.142.212.100","91.108.4.15","103.21.244.0","198.51.100.42"]
LOCATIONS     = ["Mumbai, India","Delhi, India","Bangalore, India","Moscow, Russia","Beijing, China","Unknown"]
DEVICES       = ["WIN-PC-001","WIN-PC-002","WIN-SERVER-01","LINUX-SRV-01","MACBOOK-HR"]

def timestamp():
    return datetime.now(timezone.utc).isoformat()

# ── Log table generators ─────────────────────────────────────────────────────

def signin_log(user=None, success=True, ip=None, location=None):
    """Mimics Azure AD SigninLogs table"""
    return {
        "TableName"        : "SigninLogs",
        "TimeGenerated"    : timestamp(),
        "CorrelationId"    : str(uuid.uuid4()),
        "UserPrincipalName": user or random.choice(USERS),
        "IPAddress"        : ip or random.choice(INTERNAL_IPS + EXTERNAL_IPS),
        "Location"         : location or random.choice(LOCATIONS),
        "ResultType"       : "0" if success else str(random.choice([50126,50053,70011])),
        "ResultDescription": "Successfully signed in" if success else "Invalid credentials",
        "DeviceDetail"     : random.choice(DEVICES),
        "RiskLevelDuringSignIn": "none" if success else random.choice(["low","medium","high"]),
        "AppDisplayName"   : random.choice(["Microsoft 365","Azure Portal","Teams","SharePoint"]),
    }

def security_event(user=None, event_id=None, ip=None):
    """Mimics Windows SecurityEvent table"""
    events = {
        4625: "An account failed to log on",
        4624: "An account was successfully logged on",
        4672: "Special privileges assigned to new logon",
        4720: "A user account was created",
        4732: "A member was added to a security-enabled local group",
        4728: "A member was added to a security-enabled global group",
        1102: "The audit log was cleared",
    }
    eid = event_id or random.choice(list(events.keys()))
    return {
        "TableName"      : "SecurityEvent",
        "TimeGenerated"  : timestamp(),
        "EventID"        : eid,
        "Activity"       : events.get(eid, "Unknown event"),
        "Account"        : user or random.choice(USERS),
        "Computer"       : random.choice(DEVICES),
        "IpAddress"      : ip or random.choice(INTERNAL_IPS),
        "LogonType"      : random.choice([2, 3, 10]),
        "SubjectUserName": random.choice(USERS),
        "TargetUserName" : user or random.choice(USERS),
    }

def azure_activity(user=None, operation=None, status="Succeeded"):
    """Mimics AzureActivity table"""
    operations = [
        "Microsoft.Authorization/roleAssignments/write",
        "Microsoft.Compute/virtualMachines/delete",
        "Microsoft.KeyVault/vaults/secrets/read",
        "Microsoft.Network/networkSecurityGroups/write",
        "Microsoft.Storage/storageAccounts/delete",
        "Microsoft.Authorization/policyAssignments/write",
    ]
    return {
        "TableName"        : "AzureActivity",
        "TimeGenerated"    : timestamp(),
        "CorrelationId"    : str(uuid.uuid4()),
        "Caller"           : user or random.choice(USERS),
        "OperationName"    : operation or random.choice(operations),
        "ActivityStatus"   : status,
        "ResourceGroup"    : "wissen-client-rg",
        "SubscriptionId"   : str(uuid.uuid4()),
        "HTTPRequest"      : {"clientIpAddress": random.choice(EXTERNAL_IPS)},
    }

def network_flow(src_ip=None, dst_port=None, protocol="TCP"):
    """Mimics network flow / firewall log"""
    return {
        "TableName"    : "NetworkFlow",
        "TimeGenerated": timestamp(),
        "SrcIP"        : src_ip or random.choice(EXTERNAL_IPS),
        "DstIP"        : random.choice(INTERNAL_IPS),
        "SrcPort"      : random.randint(1024, 65535),
        "DstPort"      : dst_port or random.choice([80,443,22,3389,8080,445,139]),
        "Protocol"     : protocol,
        "Action"       : random.choice(["Allow","Allow","Allow","Deny"]),
        "BytesSent"    : random.randint(100, 9000),
        "BytesReceived": random.randint(100, 50000),
    }

# ── Normal traffic generator ─────────────────────────────────────────────────

def normal_log():
    """Generates a random benign log entry"""
    generators = [
        lambda: signin_log(success=True),
        lambda: security_event(event_id=4624),
        lambda: azure_activity(status="Succeeded"),
        lambda: network_flow(),
    ]
    return random.choice(generators)()
