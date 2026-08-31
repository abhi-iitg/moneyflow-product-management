import pandas as pd
import streamlit as st

st.set_page_config(page_title="MoneyFlow — Financial Check-in", page_icon="💸", layout="wide")

CATEGORIES = ["Income", "Housing", "Food", "Transport", "Shopping", "Entertainment", "Bills", "Health", "Education", "Travel", "Subscriptions", "Other"]

DEMO_DATA = [
    ["2026-08-01", "Salary", 60000, "Income"], ["2026-08-02", "Rent", -18000, "Housing"],
    ["2026-08-03", "Swiggy", -620, "Food"], ["2026-08-04", "Uber", -280, "Transport"],
    ["2026-08-05", "Netflix", -499, "Subscriptions"], ["2026-08-06", "Amazon", -1450, "Shopping"],
    ["2026-08-07", "Electricity", -1800, "Bills"], ["2026-08-08", "Zomato", -740, "Food"],
    ["2026-08-10", "Gym", -1200, "Health"], ["2026-08-11", "College Books", -900, "Education"],
    ["2026-08-13", "Uber", -310, "Transport"], ["2026-08-15", "Restaurant", -1250, "Food"],
    ["2026-08-17", "Amazon", -890, "Shopping"], ["2026-08-19", "Flight Booking", -5200, "Travel"],
    ["2026-08-21", "Electricity", -1650, "Bills"], ["2026-08-23", "Swiggy", -680, "Food"],
    ["2026-08-25", "Uber", -290, "Transport"], ["2026-08-26", "Subscription", -299, "Subscriptions"],
    ["2026-08-27", "Zomato", -560, "Food"], ["2026-08-28", "Shopping", -1750, "Shopping"],
]

DEFAULT_BUDGETS = {"Housing": 18000, "Food": 5000, "Transport": 2500, "Shopping": 4000, "Entertainment": 2000, "Bills": 3500, "Health": 2000, "Education": 2000, "Travel": 6000, "Subscriptions": 1000, "Other": 2000}


def money(x):
    return f"₹{float(x):,.0f}"


def infer_category(merchant, amount):
    m = str(merchant).lower()
    rules = {
        "Income": ["salary", "stipend", "scholarship", "refund", "interest"],
        "Housing": ["rent", "hostel", "housing"],
        "Food": ["swiggy", "zomato", "restaurant", "cafe", "food", "domino"],
        "Transport": ["uber", "ola", "metro", "bus", "fuel", "petrol"],
        "Subscriptions": ["netflix", "spotify", "prime", "subscription", "hotstar"],
        "Shopping": ["amazon", "flipkart", "myntra", "shopping"],
        "Bills": ["electricity", "internet", "mobile", "water", "recharge"],
        "Health": ["gym", "pharmacy", "hospital", "health"],
        "Education": ["book", "course", "tuition", "college"],
        "Travel": ["flight", "hotel", "train", "travel"],
        "Entertainment": ["movie", "cinema", "game"],
    }
    for category, keywords in rules.items():
        if any(k in m for k in keywords):
            return category
    return "Other" if float(amount) < 0 else "Income"


def normalize_transactions(df):
    aliases = {
        "date": ["date", "transaction_date", "transaction date"],
        "merchant": ["merchant", "description", "payee", "transaction", "name"],
        "amount": ["amount", "value", "transaction_amount"],
        "category": ["category", "type", "spend_category"],
    }
    lower = {str(c).strip().lower(): c for c in df.columns}
    mapped = {}
    for target, candidates in aliases.items():
        for c in candidates:
            if c in lower:
                mapped[target] = lower[c]
                break
    missing = [x for x in ["date", "merchant", "amount"] if x not in mapped]
    if missing:
        raise ValueError("CSV is missing required columns: " + ", ".join(missing) + ". Required columns: date, merchant, amount. Optional: category.")

    out = pd.DataFrame()
    out["date"] = pd.to_datetime(df[mapped["date"]], errors="coerce")
    out["merchant"] = df[mapped["merchant"]].fillna("").astype(str).str.strip()
    out["amount"] = pd.to_numeric(df[mapped["amount"]].astype(str).str.replace(",", "", regex=False), errors="coerce")
    out["category"] = df[mapped["category"]].fillna("").astype(str).str.strip() if "category" in mapped else ""

    invalid = out["date"].isna() | out["merchant"].eq("") | out["amount"].isna()
    if invalid.any():
        st.warning(f"{int(invalid.sum())} row(s) failed validation and were removed.")
    out = out.loc[~invalid].copy()

    out["category"] = out["category"].where(out["category"].isin(CATEGORIES), "")
    out["category"] = out.apply(lambda r: r["category"] if r["category"] else infer_category(r["merchant"], r["amount"]), axis=1)
    out.loc[out["amount"] > 0, "category"] = "Income"
    bad_income = (out["amount"] < 0) & (out["category"] == "Income")
    out.loc[bad_income, "category"] = out.loc[bad_income].apply(lambda r: infer_category(r["merchant"], r["amount"]), axis=1)
    return out.sort_values("date").reset_index(drop=True)


def load_demo():
    return normalize_transactions(pd.DataFrame(DEMO_DATA, columns=["date", "merchant", "amount", "category"]))


def init_state():
    defaults = {
        "transactions": load_demo(), "budgets": DEFAULT_BUDGETS.copy(), "goal_name": "Emergency Fund",
        "goal_target": 50000.0, "goal_saved": 15000.0, "actions": set(), "editor_version": 0,
        "last_upload_signature": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_metrics(df):
    income = float(df.loc[df.amount > 0, "amount"].sum())
    expenses = float(-df.loc[df.amount < 0, "amount"].sum())
    return income, expenses, income - expenses


def get_spending(df):
    exp = df.loc[df.amount < 0]
    if exp.empty:
        return pd.Series(dtype=float)
    return -exp.groupby("category")["amount"].sum().sort_values(ascending=False)


def build_insights(df):
    income, expenses, net = get_metrics(df)
    spending = get_spending(df)
    items = []
    if net > 0:
        items.append(("💡", "Positive cash flow", f"You have {money(net)} left after recorded expenses.", "Update savings goal"))
    elif net < 0:
        items.append(("⚠️", "Negative cash flow", f"Your recorded expenses exceed income by {money(abs(net))}.", "Review transactions"))
    else:
        items.append(("⚖️", "Cash flow is balanced", "Your recorded income currently equals your recorded expenses.", "Review transactions"))

    if not spending.empty:
        top_cat, top_val = str(spending.index[0]), float(spending.iloc[0])
        items.append(("📌", f"{top_cat} is your largest spending category", f"You spent {money(top_val)} here in the loaded period.", "Review category"))

    subscriptions = float(spending.get("Subscriptions", 0))
    if subscriptions > 1000 and (spending.empty or str(spending.index[0]) != "Subscriptions"):
        items.append(("🔁", "Recurring subscription spend is notable", f"You spent {money(subscriptions)} on subscriptions. Review services you actively use.", "Review subscriptions"))

    pressure = []
    for category, budget in st.session_state.budgets.items():
        spent = float(spending.get(category, 0))
        if budget > 0 and spent > budget:
            pressure.append((spent - budget, category, spent, budget))
    if pressure:
        _, category, spent, budget = sorted(pressure, reverse=True)[0]
        items.append(("📊", f"{category} is over its budget", f"You spent {money(spent)} against a {money(budget)} planning limit.", "Review budget"))
    return items[:3]


def save_edited_transactions(view, edited):
    updated = st.session_state.transactions.copy()
    errors = []
    for idx, row in edited.iterrows():
        if idx not in view.index:
            continue
        new_date = pd.to_datetime(row["date"], errors="coerce")
        new_merchant = str(row["merchant"]).strip()
        new_amount = pd.to_numeric(row["amount"], errors="coerce")
        new_category = str(row["category"]).strip()
        if pd.isna(new_date): errors.append(f"Row {idx + 1}: invalid date.")
        if not new_merchant: errors.append(f"Row {idx + 1}: merchant cannot be blank.")
        if pd.isna(new_amount): errors.append(f"Row {idx + 1}: amount must be numeric.")
        if new_category not in CATEGORIES: errors.append(f"Row {idx + 1}: invalid category.")
        if pd.isna(new_amount) or float(new_amount) == 0: errors.append(f"Row {idx + 1}: amount cannot be ₹0. Use positive for income or negative for spending.")
        if errors and errors[-1].startswith(f"Row {idx + 1}:"):
            continue
        new_amount = float(new_amount)
        if new_amount > 0:
            new_category = "Income"
        elif new_category == "Income":
            new_category = infer_category(new_merchant, new_amount)
        updated.loc[idx, "date"] = new_date.normalize()
        updated.loc[idx, "merchant"] = new_merchant
        updated.loc[idx, "amount"] = new_amount
        updated.loc[idx, "category"] = new_category
    if errors:
        return None, errors
    updated["date"] = pd.to_datetime(updated["date"], errors="coerce")
    updated["amount"] = pd.to_numeric(updated["amount"], errors="coerce")
    return updated.sort_values("date").reset_index(drop=True), []


init_state()
st.title("💸 MoneyFlow")
st.caption("Privacy-first personal finance check-in • Working MVP • Synthetic demo data")

with st.sidebar:
    st.header("Data")
    uploaded = st.file_uploader("Upload a CSV", type=["csv"], help="Required columns: date, merchant, amount. Optional: category.")
    if uploaded is not None:
        signature = f"{uploaded.name}-{uploaded.size}"
        if st.session_state.last_upload_signature != signature:
            try:
                st.session_state.transactions = normalize_transactions(pd.read_csv(uploaded))
                st.session_state.actions.add("csv_upload")
                st.session_state.last_upload_signature = signature
                st.session_state.editor_version += 1
                st.success("CSV loaded successfully.")
                st.rerun()
            except Exception as exc:
                st.error(str(exc))
    if st.button("Reset to demo data", use_container_width=True):
        st.session_state.transactions = load_demo()
        st.session_state.actions = set()
        st.session_state.last_upload_signature = None
        st.session_state.editor_version += 1
        st.rerun()
    st.divider()
    st.info("Demo only. Use synthetic or non-sensitive data. Do not upload bank credentials, OTPs, card numbers, or other secrets.")

df = st.session_state.transactions.copy()
income, expenses, net = get_metrics(df)
spending = get_spending(df)

st.subheader("Your financial check-in")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Income", money(income))
c2.metric("Expenses", money(expenses))
c3.metric("Net cash flow", money(net))
c4.metric("Illustrative safe-to-spend", money(max(net * 0.35, 0)), help="Demo heuristic only, not financial advice.")

st.divider()
left, right = st.columns([1.3, 1])
with left:
    st.subheader("What changed?")
    for icon, title, body, action in build_insights(df):
        with st.container(border=True):
            st.markdown(f"### {icon} {title}")
            st.write(body)
            key = f"{title}-{action}"
            if st.button(action, key=key):
                st.session_state.actions.add(key)
                st.success("Action recorded for this demo session.")
with right:
    st.subheader("Spending by category")
    if not spending.empty:
        st.bar_chart(spending)
    else:
        st.info("No expenses available.")

st.divider()
tab1, tab2, tab3, tab4 = st.tabs(["Transactions", "Plan", "Goal", "Product Metrics"])

with tab1:
    st.subheader("Transactions")
    st.caption("Edit Date, Merchant, Amount and Category directly. Positive amounts are income; negative amounts are spending.")
    search = st.text_input("Search merchant", "")
    view = df.copy()
    if search:
        view = view[view.merchant.str.contains(search, case=False, na=False)]
    editor_data = view[["date", "merchant", "amount", "category"]].copy()
    editor_data["date"] = pd.to_datetime(editor_data["date"]).dt.date
    edited = st.data_editor(
        editor_data, use_container_width=True, hide_index=True,
        column_config={
            "date": st.column_config.DateColumn("Date", format="DD MMM YYYY", required=True),
            "merchant": st.column_config.TextColumn("Merchant", required=True),
            "amount": st.column_config.NumberColumn("Amount (₹)", format="₹%.0f", required=True),
            "category": st.column_config.SelectboxColumn("Category", options=CATEGORIES, required=True),
        }, disabled=[], key=f"transaction_editor_{st.session_state.editor_version}",
    )
    if st.button("💾 Save transaction changes", type="primary"):
        updated, errors = save_edited_transactions(view, edited)
        if errors:
            for e in errors: st.error(e)
        else:
            before = st.session_state.transactions.copy()
            changed = not before.equals(updated)
            category_changed = not before["category"].reset_index(drop=True).equals(updated["category"].reset_index(drop=True))
            st.session_state.transactions = updated
            if changed:
                st.session_state.actions.add("transaction_edit")
            if category_changed:
                st.session_state.actions.add("category_correction")
            st.session_state.editor_version += 1
            st.success("Transaction changes saved successfully." if changed else "No transaction changes were detected.")
            st.rerun()
    st.caption("After saving, Income, Expenses, Net cash flow, insights, category spending and product instrumentation recalculate from the updated transactions.")

with tab2:
    st.subheader("Flexible budget")
    st.write("Set monthly category limits. These are planning inputs, not financial advice.")
    for category in sorted(st.session_state.budgets):
        spent = float(spending.get(category, 0))
        old = float(st.session_state.budgets[category])
        col1, col2, col3 = st.columns([2, 1, 2])
        col1.write(category)
        new = col2.number_input(f"Budget for {category}", min_value=0.0, value=old, step=500.0, key=f"budget_{category}", label_visibility="collapsed")
        if new != old:
            st.session_state.budgets[category] = new
            st.session_state.actions.add("budget_adjustment")
        remaining = max(float(new) - spent, 0)
        col3.progress(min(spent / new, 1.0) if new else 0, text=f"{money(spent)} spent • {money(remaining)} remaining")

with tab3:
    st.subheader("Savings goal")
    old_name, old_target, old_saved = st.session_state.goal_name, float(st.session_state.goal_target), float(st.session_state.goal_saved)
    new_name = st.text_input("Goal name", old_name)
    new_target = st.number_input("Target amount (₹)", min_value=1.0, value=old_target, step=1000.0)
    new_saved = st.number_input("Amount saved so far (₹)", min_value=0.0, value=old_saved, step=500.0)
    if new_name != old_name or new_target != old_target or new_saved != old_saved:
        st.session_state.goal_name, st.session_state.goal_target, st.session_state.goal_saved = new_name, new_target, new_saved
        st.session_state.actions.add("goal_update")
    progress = min(st.session_state.goal_saved / st.session_state.goal_target, 1.0)
    st.progress(progress, text=f"{progress:.0%} complete")
    st.metric("Remaining", money(max(st.session_state.goal_target - st.session_state.goal_saved, 0)))

with tab4:
    st.subheader("Product analytics — demo session")
    actionable = len(st.session_state.actions)
    metrics = pd.DataFrame({
        "Metric": ["Transactions loaded", "Actionable insights shown", "Actions completed", "Transaction edits", "Category corrections", "Budget adjustments", "Goal updates", "CSV uploads", "Activation status"],
        "Value": [len(st.session_state.transactions), len(build_insights(st.session_state.transactions)), actionable, int("transaction_edit" in st.session_state.actions), int("category_correction" in st.session_state.actions), int("budget_adjustment" in st.session_state.actions), int("goal_update" in st.session_state.actions), int("csv_upload" in st.session_state.actions), "Activated" if actionable else "Not yet activated"],
    })
    st.dataframe(metrics, use_container_width=True, hide_index=True)
    st.caption("Session-level product instrumentation only. Values are generated from actual demo-session actions, not manually entered and not customer traction.")

st.divider()
st.caption("MoneyFlow MVP • Product-management case study • Synthetic/demo data only")
