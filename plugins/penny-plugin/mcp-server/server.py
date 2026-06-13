#!/usr/bin/env python3
"""
Penny QBO MCP Server
A proper QuickBooks Online API wrapper for Penny the AI Bookkeeper.

Credentials are read from ~/.penny-qbo/config.json (never hardcoded).
Tokens are stored at ~/.penny-qbo/tokens.json (auto-refreshed).
"""

import json
import os
import time
import webbrowser
import urllib.parse
from pathlib import Path
from typing import Optional

import httpx
from mcp.server.fastmcp import FastMCP

# ─── Configuration ────────────────────────────────────────────────────────────

CONFIG_DIR = Path.home() / ".penny-qbo"
CONFIG_FILE = CONFIG_DIR / "config.json"
TOKENS_FILE = CONFIG_DIR / "tokens.json"

REDIRECT_URI = "https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl"
SCOPES = "com.intuit.quickbooks.accounting"

INTUIT_AUTH_URL = "https://appcenter.intuit.com/connect/oauth2"
INTUIT_TOKEN_URL = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
QBO_API_BASE = "https://quickbooks.api.intuit.com/v3/company"

mcp = FastMCP("penny-qbo")


def load_credentials() -> tuple[str, str]:
    """Load Client ID and Secret from env vars or config file."""
    client_id = os.environ.get("QBO_CLIENT_ID")
    client_secret = os.environ.get("QBO_CLIENT_SECRET")
    if client_id and client_secret:
        return client_id, client_secret
    if CONFIG_FILE.exists():
        cfg = json.loads(CONFIG_FILE.read_text())
        return cfg.get("client_id", ""), cfg.get("client_secret", "")
    raise ValueError(
        "QBO credentials not found. Run setup.sh or set QBO_CLIENT_ID and QBO_CLIENT_SECRET env vars."
    )


# ─── Token Management ─────────────────────────────────────────────────────────

def load_tokens() -> dict:
    if TOKENS_FILE.exists():
        return json.loads(TOKENS_FILE.read_text())
    return {}


def save_tokens(tokens: dict):
    CONFIG_DIR.mkdir(exist_ok=True)
    TOKENS_FILE.write_text(json.dumps(tokens, indent=2))
    TOKENS_FILE.chmod(0o600)


def get_valid_access_token() -> Optional[str]:
    """Return a valid access token, refreshing automatically if expired."""
    tokens = load_tokens()
    if not tokens:
        return None

    # Still valid with 60s buffer
    if time.time() < tokens.get("expires_at", 0) - 60:
        return tokens["access_token"]

    # Refresh
    refresh_token = tokens.get("refresh_token")
    if not refresh_token:
        return None

    client_id, client_secret = load_credentials()
    response = httpx.post(
        INTUIT_TOKEN_URL,
        data={"grant_type": "refresh_token", "refresh_token": refresh_token},
        auth=(client_id, client_secret),
        headers={"Accept": "application/json"},
    )

    if response.status_code == 200:
        new_tokens = response.json()
        tokens.update({
            "access_token": new_tokens["access_token"],
            "refresh_token": new_tokens.get("refresh_token", refresh_token),
            "expires_at": time.time() + new_tokens.get("expires_in", 3600),
        })
        save_tokens(tokens)
        return tokens["access_token"]

    return None


def get_realm_id() -> Optional[str]:
    return load_tokens().get("realm_id")


def qbo_request(method: str, endpoint: str, **kwargs) -> dict:
    """Make an authenticated QBO API request."""
    access_token = get_valid_access_token()
    if not access_token:
        raise ValueError("Not authenticated. Call qbo_authenticate first.")
    realm_id = get_realm_id()
    if not realm_id:
        raise ValueError("No realm ID. Call qbo_authenticate first.")

    url = f"{QBO_API_BASE}/{realm_id}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    response = httpx.request(method, url, headers=headers, **kwargs)
    response.raise_for_status()
    return response.json()


# ─── OAuth Flow ───────────────────────────────────────────────────────────────

@mcp.tool()
def qbo_authenticate() -> str:
    """
    Step 1 of 2: Start the QuickBooks Online OAuth connection.
    Opens a browser window. After you authorize, you'll land on the
    Intuit OAuth Playground page — look at the URL bar and copy the
    values for 'code' and 'realmId', then call qbo_complete_auth().
    Only needs to be done once — tokens auto-refresh after that.
    """
    client_id, _ = load_credentials()

    auth_params = urllib.parse.urlencode({
        "client_id": client_id,
        "response_type": "code",
        "scope": SCOPES,
        "redirect_uri": REDIRECT_URI,
        "state": "penny-qbo-auth",
    })
    auth_url = f"{INTUIT_AUTH_URL}?{auth_params}"
    webbrowser.open(auth_url)

    return (
        "✅ Browser opened for QuickBooks authorization.\n\n"
        "After you click 'Connect' in the browser:\n"
        "  1. You'll land on the Intuit OAuth Playground page\n"
        "  2. Look at the URL in the browser bar — it will contain:\n"
        "       ?code=AB11...&realmId=123456...&state=penny-qbo-auth\n"
        "  3. Copy the 'code' value and the 'realmId' value\n"
        "  4. Call qbo_complete_auth(auth_code='...', realm_id='...') with those values\n\n"
        "The code expires in 10 minutes, so complete step 4 promptly."
    )


@mcp.tool()
def qbo_complete_auth(auth_code: str, realm_id: str) -> str:
    """
    Step 2 of 2: Complete the QuickBooks connection using the code from the browser.
    Call this after qbo_authenticate() — paste in the 'code' and 'realmId'
    values from the OAuth Playground URL.

    Args:
        auth_code: The 'code' value from the redirect URL
        realm_id:  The 'realmId' value from the redirect URL
    """
    client_id, client_secret = load_credentials()

    response = httpx.post(
        INTUIT_TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": REDIRECT_URI,
        },
        auth=(client_id, client_secret),
        headers={"Accept": "application/json"},
    )

    if response.status_code != 200:
        return f"Token exchange failed: {response.text}"

    token_data = response.json()
    save_tokens({
        "access_token": token_data["access_token"],
        "refresh_token": token_data["refresh_token"],
        "expires_at": time.time() + token_data.get("expires_in", 3600),
        "realm_id": realm_id,
    })

    return f"✅ Successfully connected to QuickBooks! Company Realm ID: {realm_id}"


# ─── QBO Tools ────────────────────────────────────────────────────────────────

@mcp.tool()
def qbo_get_company_info() -> str:
    """Get the connected QBO company name and details. Always call this first to verify the right company is connected."""
    realm_id = get_realm_id()
    result = qbo_request("GET", f"companyinfo/{realm_id}")
    info = result.get("CompanyInfo", {})
    return json.dumps({
        "company_name": info.get("CompanyName"),
        "legal_name": info.get("LegalName"),
        "fiscal_year_start_month": info.get("FiscalYearStartMonth"),
        "country": info.get("Country"),
        "email": info.get("Email", {}).get("Address"),
    }, indent=2)


@mcp.tool()
def qbo_query(sql: str) -> str:
    """
    Run a QBO SQL-style query against any entity.

    Examples:
      SELECT * FROM Account WHERE AccountType = 'Bank'
      SELECT * FROM Vendor WHERE Active = true
      SELECT * FROM Purchase WHERE TxnDate >= '2026-04-01' AND TxnDate <= '2026-04-30'
      SELECT * FROM Deposit WHERE TxnDate >= '2026-04-01'
      SELECT * FROM JournalEntry ORDER BY TxnDate DESC MAXRESULTS 20
      SELECT * FROM Employee WHERE Active = true
    """
    result = qbo_request("GET", "query", params={"query": sql})
    return json.dumps(result.get("QueryResponse", {}), indent=2)


@mcp.tool()
def qbo_get_profit_loss(start_date: str, end_date: str) -> str:
    """
    Get Profit & Loss report for a date range.
    Args:
        start_date: YYYY-MM-DD (e.g., 2026-04-01)
        end_date:   YYYY-MM-DD (e.g., 2026-04-30)
    """
    result = qbo_request("GET", "reports/ProfitAndLoss", params={
        "start_date": start_date,
        "end_date": end_date,
        "accounting_method": "Accrual",
    })
    return json.dumps(result, indent=2)


@mcp.tool()
def qbo_get_balance_sheet(as_of_date: str) -> str:
    """
    Get Balance Sheet as of a specific date.
    Args:
        as_of_date: YYYY-MM-DD (e.g., 2026-04-30)
    """
    result = qbo_request("GET", "reports/BalanceSheet", params={
        "end_date": as_of_date,
        "accounting_method": "Accrual",
    })
    return json.dumps(result, indent=2)


@mcp.tool()
def qbo_list_accounts(account_type: str = "") -> str:
    """
    List chart of accounts.
    Args:
        account_type: Optional filter — Bank, Expense, Income, OtherCurrentLiability,
                      LongTermLiability, Equity, OtherAsset, CostOfGoodsSold
    """
    sql = "SELECT * FROM Account WHERE Active = true"
    if account_type:
        sql += f" AND AccountType = '{account_type}'"
    sql += " MAXRESULTS 200"
    return qbo_query(sql)


@mcp.tool()
def qbo_list_vendors() -> str:
    """List all active vendors in QBO."""
    return qbo_query("SELECT * FROM Vendor WHERE Active = true MAXRESULTS 200")


@mcp.tool()
def qbo_list_transactions(start_date: str, end_date: str, transaction_type: str = "Purchase") -> str:
    """
    List transactions for a date range.
    Args:
        start_date:       YYYY-MM-DD
        end_date:         YYYY-MM-DD
        transaction_type: Purchase (expenses), Deposit, JournalEntry, Invoice, Payment, Transfer
    """
    sql = (
        f"SELECT * FROM {transaction_type} "
        f"WHERE TxnDate >= '{start_date}' AND TxnDate <= '{end_date}' "
        f"MAXRESULTS 100"
    )
    return qbo_query(sql)


@mcp.tool()
def qbo_create_journal_entry(
    txn_date: str,
    memo: str,
    debit_account_id: str,
    credit_account_id: str,
    amount: float,
) -> str:
    """
    Create a journal entry in QBO.
    Args:
        txn_date:          YYYY-MM-DD
        memo:              Description (appears in QBO and reports)
        debit_account_id:  QBO account ID to debit  (get IDs from qbo_list_accounts)
        credit_account_id: QBO account ID to credit
        amount:            Dollar amount (positive number)
    """
    payload = {
        "TxnDate": txn_date,
        "PrivateNote": memo,
        "Line": [
            {
                "Description": memo,
                "Amount": amount,
                "DetailType": "JournalEntryLineDetail",
                "JournalEntryLineDetail": {
                    "PostingType": "Debit",
                    "AccountRef": {"value": debit_account_id},
                },
            },
            {
                "Description": memo,
                "Amount": amount,
                "DetailType": "JournalEntryLineDetail",
                "JournalEntryLineDetail": {
                    "PostingType": "Credit",
                    "AccountRef": {"value": credit_account_id},
                },
            },
        ],
    }
    result = qbo_request("POST", "journalentry", json=payload)
    je = result.get("JournalEntry", {})
    return json.dumps({
        "success": True,
        "id": je.get("Id"),
        "txn_date": je.get("TxnDate"),
        "amount": amount,
        "memo": memo,
    }, indent=2)


@mcp.tool()
def qbo_create_expense(
    txn_date: str,
    vendor_name: str,
    expense_account_id: str,
    payment_account_id: str,
    amount: float,
    memo: str,
) -> str:
    """
    Create an expense (Purchase) transaction in QBO.
    Args:
        txn_date:           YYYY-MM-DD
        vendor_name:        Exact vendor display name as it appears in QBO
        expense_account_id: Expense account ID (from qbo_list_accounts)
        payment_account_id: Bank account the payment came from (account ID)
        amount:             Dollar amount
        memo:               Transaction description
    """
    vendor_result = json.loads(qbo_query(f"SELECT * FROM Vendor WHERE DisplayName = '{vendor_name}'"))
    vendors = vendor_result.get("Vendor", [])
    if not vendors:
        return json.dumps({
            "error": f"Vendor '{vendor_name}' not found. Check spelling or create vendor first using qbo_create_vendor."
        })

    vendor_id = vendors[0]["Id"]
    payload = {
        "TxnDate": txn_date,
        "PrivateNote": memo,
        "PaymentType": "Cash",
        "AccountRef": {"value": payment_account_id},
        "EntityRef": {"value": vendor_id, "type": "Vendor"},
        "Line": [{
            "Amount": amount,
            "DetailType": "AccountBasedExpenseLineDetail",
            "AccountBasedExpenseLineDetail": {
                "AccountRef": {"value": expense_account_id},
                "BillableStatus": "NotBillable",
            },
            "Description": memo,
        }],
    }
    result = qbo_request("POST", "purchase", json=payload)
    purchase = result.get("Purchase", {})
    return json.dumps({
        "success": True,
        "id": purchase.get("Id"),
        "txn_date": purchase.get("TxnDate"),
        "amount": amount,
        "vendor": vendor_name,
    }, indent=2)


@mcp.tool()
def qbo_create_deposit(
    txn_date: str,
    deposit_account_id: str,
    income_account_id: str,
    amount: float,
    memo: str,
) -> str:
    """
    Record a deposit (money coming into the bank) in QBO.
    Args:
        txn_date:           YYYY-MM-DD
        deposit_account_id: Bank account receiving the deposit (account ID)
        income_account_id:  Income account to credit (account ID)
        amount:             Dollar amount
        memo:               Description (e.g., "Stripe payout — April subscription revenue")
    """
    payload = {
        "TxnDate": txn_date,
        "DepositToAccountRef": {"value": deposit_account_id},
        "PrivateNote": memo,
        "Line": [{
            "Amount": amount,
            "DetailType": "DepositLineDetail",
            "DepositLineDetail": {
                "AccountRef": {"value": income_account_id},
            },
            "Description": memo,
        }],
    }
    result = qbo_request("POST", "deposit", json=payload)
    deposit = result.get("Deposit", {})
    return json.dumps({
        "success": True,
        "id": deposit.get("Id"),
        "txn_date": deposit.get("TxnDate"),
        "amount": amount,
        "memo": memo,
    }, indent=2)


@mcp.tool()
def qbo_create_vendor(display_name: str, email: str = "", company_name: str = "") -> str:
    """
    Create a new vendor in QBO.
    Args:
        display_name: How the vendor appears in QBO (required)
        email:        Vendor email (optional)
        company_name: Legal company name if different from display name (optional)
    """
    payload = {"DisplayName": display_name}
    if email:
        payload["PrimaryEmailAddr"] = {"Address": email}
    if company_name:
        payload["CompanyName"] = company_name

    result = qbo_request("POST", "vendor", json=payload)
    vendor = result.get("Vendor", {})
    return json.dumps({
        "success": True,
        "id": vendor.get("Id"),
        "display_name": vendor.get("DisplayName"),
    }, indent=2)


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
