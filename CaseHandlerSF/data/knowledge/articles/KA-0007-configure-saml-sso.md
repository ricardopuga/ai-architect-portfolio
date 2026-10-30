---
article_number: KA-0007
title: Setting up SAML single sign-on
url_name: configure-saml-sso
article_type: How-to
category: Sign-in & Security
plans: [Business, Enterprise]
last_reviewed: 2026-09-18
related_cases: [CASE-1018]
summary: How to connect Lumora Workspace to a SAML 2.0 identity provider (Okta, Microsoft Entra ID, Google Workspace and others), with fixes for the most common setup errors.
---

## Before you start

- You need Business or Enterprise, and the workspace **Owner** role.
- Claim and verify your email domain first: **Settings > Security > Domains**. You verify it with a DNS TXT record.

## Values to enter in your IdP

| Field | Value |
|---|---|
| Entity ID / Audience URI | `https://<subdomain>.lumora.example/sso/saml/metadata` |
| ACS (Reply) URL | `https://<subdomain>.lumora.example/sso/saml/acs` |
| Single Logout URL (optional) | `https://<subdomain>.lumora.example/sso/saml/slo` |
| NameID format | `emailAddress` |
| Required attributes | `email`, `firstName`, `lastName` |

## Steps in Lumora

1. Go to **Settings > Security > Single sign-on > Add SAML connection**.
2. Upload the IdP metadata XML, **or** paste the SSO URL, the IdP entity ID and the X.509 signing certificate.
3. Click **Test connection** in a private browser window.
4. When the test passes, choose the enforcement level: **Optional** or **Required for verified domains**.

Keep at least one Owner account able to sign in with a password ("break-glass") until you've confirmed SSO works.

## Common errors

| Error | Cause | Fix |
|---|---|---|
| `Audience mismatch` | The entity ID in the IdP doesn't match exactly | Copy the value again. It is case-sensitive and must have no trailing slash |
| `Signature validation failed` | The certificate was rotated or the wrong one was pasted | Upload fresh IdP metadata |
| `Assertion expired` | The IdP server's clock is off | Fix NTP on the IdP. Allowed skew is 3 minutes |
| `User not provisioned` | Just-in-time provisioning is off and the user doesn't exist | Invite the user first, or turn on **JIT provisioning** |
| `Email not in verified domain` | The user's email domain hasn't been claimed | Verify the domain under **Domains** |

## OIDC

OIDC setup is under **Add OIDC connection**. The redirect URI is `https://<subdomain>.lumora.example/sso/oidc/callback`.

## Related

- KA-0008 SSO logout does not fully end the session (known issue)
