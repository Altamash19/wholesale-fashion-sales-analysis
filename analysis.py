"""
Serenity Threads Sdn. Bhd. (fictional) — FY2025 Financial Analysis
Portfolio project — data anonymized from a real wholesale/retail apparel business (names and exact figures altered).

Sources: Creditor (Supplier) Ledger, Debtor (Customer) Ledger, Trading P&L — FY2025.
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["axes.facecolor"] = "white"
plt.rcParams["font.size"] = 10

NAVY, ACCENT, RED, GREEN, GREY = "#1F3864", "#2E5AAC", "#C0392B", "#3C8A5B", "#8A93A6"
money = lambda x, _: f"{x/1000:,.0f}k"

suppliers = pd.read_csv("data/suppliers.csv")
customers = pd.read_csv("data/customers.csv")
pnl = pd.read_csv("data/pnl.csv")

findings = []

# ---------- 1. P&L Waterfall ----------
sales = pnl.loc[pnl.category == "Revenue", "amount_myr"].sum()
cogs = pnl.loc[pnl.category == "COGS", "amount_myr"].sum()
gross = sales - cogs
opex = pnl.loc[pnl.category == "Expense", "amount_myr"].sum()
net = gross - opex

labels = ["Sales", "COGS", "Gross\nProfit/(Loss)", "Operating\nExpenses", "Net\nProfit/(Loss)"]
values = [sales, -cogs, gross, -opex, net]
running = [sales, sales - cogs, gross, gross - opex, net]

fig, ax = plt.subplots(figsize=(9, 5))
bar_colors = [ACCENT, RED, NAVY if gross >= 0 else RED, RED, GREEN if net >= 0 else RED]
starts = [0, sales, 0, gross, 0]
heights = [sales, cogs, gross, opex, abs(net)]
bottoms = [0, sales - cogs, 0, gross - opex, min(net, 0)]
bar_vals = [sales, -cogs, gross, -opex, net]

x = range(len(labels))
prev = 0
for i, (lab, val) in enumerate(zip(labels, bar_vals)):
    if lab in ("Sales", "Gross\nProfit/(Loss)", "Net\nProfit/(Loss)"):
        bottom = 0
        height = val
        ax.bar(i, height, bottom=bottom, color=bar_colors[i])
        prev = val
    else:
        top = prev
        bottom = prev + val  # val negative
        ax.bar(i, val, bottom=top, color=bar_colors[i])
        prev = bottom
ax.axhline(0, color="black", linewidth=0.8)
ax.set_xticks(list(x))
ax.set_xticklabels(labels)
ax.set_title("FY2025 P&L Waterfall — Serenity Threads Sdn. Bhd. (fictional)", fontweight="bold", color=NAVY)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(money))
ax.set_ylabel("RM (thousands)")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("charts/01_pnl_waterfall.png", dpi=150)
plt.close()

findings.append(
    f"**FY2025 result: Net Loss of RM{abs(net):,.0f}.** Sales were RM{sales:,.0f} but purchases "
    f"and direct costs (COGS) totaled RM{cogs:,.0f} — a gross loss of RM{abs(gross):,.0f} before "
    f"any operating expenses. Operating expenses (rent, salaries, etc.) of RM{opex:,.0f} added to "
    "that, bringing the net loss to the figure above. This is the single most important number in "
    "the accounts and is worth discussing directly with whoever manages the business finances."
)

# ---------- 2. Expense breakdown (opex only) ----------
exp = pnl.loc[pnl.category == "Expense"].copy()
exp = exp[exp.amount_myr > 0].sort_values("amount_myr", ascending=False).head(8)
fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(exp.line_item[::-1], exp.amount_myr[::-1], color=NAVY)
ax.set_title("Top Operating Expenses, FY2025", fontweight="bold", color=NAVY)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(money))
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("charts/02_top_expenses.png", dpi=150)
plt.close()

top_exp = exp.iloc[0]
salaries_pct = pnl.loc[pnl.line_item.str.contains("SALARIES", na=False), "amount_myr"].sum() / sales * 100
findings.append(
    f"**Salaries, wages & allowances (RM{pnl.loc[pnl.line_item.str.contains('SALARIES', na=False), 'amount_myr'].sum():,.0f}) "
    f"is the largest operating expense at {salaries_pct:.0f}% of total sales**, followed by shop rental "
    f"(RM{pnl.loc[pnl.line_item=='RENTAL - SHOP','amount_myr'].sum():,.0f}). Together these two fixed costs "
    "alone consume a large share of revenue regardless of how sales perform month to month."
)

# ---------- 3. Top suppliers by purchase volume ----------
top_sup = suppliers.sort_values("total_purchases_myr", ascending=False).head(8)
fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(top_sup.supplier_name[::-1], top_sup.total_purchases_myr[::-1], color=ACCENT)
ax.set_title("Top 8 Suppliers by Purchase Volume, FY2025", fontweight="bold", color=NAVY)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(money))
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("charts/03_top_suppliers.png", dpi=150)
plt.close()

total_purchases_ledger = suppliers.total_purchases_myr.sum()
top1_sup = top_sup.iloc[0]
top1_sup_share = top1_sup.total_purchases_myr / total_purchases_ledger * 100
findings.append(
    f"**{top1_sup.supplier_name} accounts for {top1_sup_share:.0f}% of all supplier purchases** "
    f"(RM{top1_sup.total_purchases_myr:,.0f} of RM{total_purchases_ledger:,.0f} total). This is a very "
    "high concentration in a single supplier — a pricing, quality, or supply disruption from this one "
    "vendor would have an outsized effect on the whole business."
)

# ---------- 4. Top customers by sales ----------
top_cust = customers.sort_values("total_sales_myr", ascending=False).head(8)
fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(top_cust.customer_name[::-1], top_cust.total_sales_myr[::-1], color=NAVY)
ax.set_title("Top 8 Customers by Sales, FY2025", fontweight="bold", color=NAVY)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(money))
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("charts/04_top_customers.png", dpi=150)
plt.close()

total_sales_ledger = customers.total_sales_myr.sum()
top1_cust = top_cust.iloc[0]
top1_cust_share = top1_cust.total_sales_myr / total_sales_ledger * 100
findings.append(
    f"**{top1_cust.customer_name} is the largest customer at {top1_cust_share:.0f}% of ledger sales** "
    f"(RM{top1_cust.total_sales_myr:,.0f}). Note this ledger total (RM{total_sales_ledger:,.0f}) is lower "
    f"than the P&L sales figure (RM{sales:,.0f}) — likely because some sales (e.g. daily TikTok/Shopee "
    "Live or till transactions) are batched elsewhere rather than posted per named customer. Worth "
    "confirming with the bookkeeper before treating the customer-level split as complete."
)

# ---------- 5. Outstanding receivables & payables ----------
receivable = customers.loc[customers.ending_balance_myr > 0, "ending_balance_myr"].sum()
payable = -suppliers.loc[suppliers.ending_balance_myr < 0, "ending_balance_myr"].sum()

fig, ax = plt.subplots(figsize=(6, 4.5))
cats = ["Owed TO business\n(Receivables)", "Owed BY business\n(Payables)"]
vals = [receivable, payable]
ax.bar(cats, vals, color=[GREEN, RED])
for i, v in enumerate(vals):
    ax.text(i, v, f"RM{v:,.0f}", ha="center", va="bottom", fontsize=9)
ax.set_title("Outstanding Balances at Period End", fontweight="bold", color=NAVY)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(money))
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("charts/05_receivables_payables.png", dpi=150)
plt.close()

biggest_payable = suppliers.loc[suppliers.ending_balance_myr.idxmin()]
biggest_receivable = customers.loc[customers.ending_balance_myr.idxmax()]
credit_balances = customers.loc[customers.ending_balance_myr < 0].sort_values("ending_balance_myr").head(1)
credit_note = ""
if len(credit_balances):
    cb = credit_balances.iloc[0]
    credit_note = (
        f" Separately, {cb.customer_name} is showing a RM{abs(cb.ending_balance_myr):,.0f} *credit* "
        "balance as a customer (paid more than they've been invoiced for) — a deposit/advance held, "
        "not money owed to the business."
    )

findings.append(
    f"**Outstanding receivables (RM{receivable:,.0f}) vs. payables (RM{payable:,.0f})** at period end. "
    f"On the payable side, RM{abs(biggest_payable.ending_balance_myr):,.0f} alone is owed to "
    f"{biggest_payable.supplier_name}. On the receivable side, {biggest_receivable.customer_name} "
    f"owes RM{biggest_receivable.ending_balance_myr:,.0f}.{credit_note} A small number of large "
    "one-off relationships dominate both sides of the ledger rather than broad-based amounts "
    "across many accounts."
)

with open("insights.md", "w") as f:
    f.write("# Serenity Threads Sdn. Bhd. (fictional) — FY2025 Key Findings\n\n**CONFIDENTIAL — internal use only**\n\n")
    for i, ins in enumerate(findings, 1):
        f.write(f"{i}. {ins}\n\n")

print("\n\n".join(findings))
