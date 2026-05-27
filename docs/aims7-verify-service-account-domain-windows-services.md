# Locating and Verifying the Service Account Domain in AIMS 7 Windows Services

## Summary

When configuring Quadient service accounts for AIMS version 7, the Windows Services properties panel provides a reliable method to navigate to the correct domain and verify the exact service account name. This approach eliminates manual domain path entry and reduces the risk of typos in account names, which are among the most common causes of service authentication failures in AIMS 7 deployments.

---

## Applies To

| Field | Detail |
|---|---|
| Product | Quadient AIMS |
| Version | AIMS 7 |
| Component | Windows Services / Service Account Configuration |
| Platform | Windows (Active Directory environment) |

---

## Steps to Verify the Service Account

1. **Open Windows Services** — Press `Win + R`, type `services.msc`, and press **Enter**.
2. **Locate the AIMS service** — Scroll through the services list to find the relevant Quadient AIMS service entry.
3. **Open Properties** — Right-click the service and select **Properties**.
4. **Go to the Log On tab** — Click the **Log On** tab in the Properties window.
5. **Read the "This account:" field** — The field displays the exact domain and username configured for this service in `DOMAIN\username` format. This is the authoritative value Windows uses to authenticate and run the service.

---

## Understanding the "This Account:" Field

The value shown in the **This account:** field is what Windows is actively using to authenticate the service at runtime. This makes it the most reliable reference point when troubleshooting service startup failures or reconfiguring credentials.

> **Important:** If this value does not match the account as it exists in Active Directory — including the correct domain prefix — the service will fail to start and log an authentication error.

---

## Common Causes of Service Account Mismatch

| Cause | Description |
|---|---|
| Incorrect domain prefix | The domain name entered does not match the actual AD domain |
| Misspelled username | Typographical error in the account name portion of the field |
| Account renamed in AD | The account was renamed in Active Directory after the service was last configured |
| Account moved in AD | The account was relocated to a different Organizational Unit or domain |

---

## Troubleshooting Tips

- Always cross-reference the `DOMAIN\username` value shown in the **Log On** tab against the account as it appears in **Active Directory Users and Computers** before making changes.
- If the service fails to start with a logon error, confirm the account has the **Log on as a service** right granted in Local Security Policy.
- After updating the service account credentials, restart the service and check **Event Viewer > Windows Logs > System** for authentication errors.

---