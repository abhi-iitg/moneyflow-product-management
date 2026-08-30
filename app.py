import io
from datetime import date
import pandas as pd
import streamlit as st

if "actions" not in st.session_state:
    st.session_state.actions = set()

st.set_page_config(
    page_title="MoneyFlow — Financial Check-in",
    page_icon="💸",
    layout="wide",
)

CATEGORIES = [
    "Income", "Housing", "Food", "Transport", "Shopping",
    "Entertainment", "Bills", "Health", "Education",
    "Travel", "Subscriptions", "Other"
]

DEMO_DATA = [
    ["2026-08-01", "Salary", 60000, "Income"],
    ["2026-08-02", "Rent", -18000, "Housing"],
    ["2026-08-03", "Swiggy", -620, "Food"],
    ["2026-08-04", "Uber", -280, "Transport"],
    ["2026-08-05", "Netflix", -499, "Subscriptions"],
    ["2026-08-06", "Amazon", -1450, "Shopping"],
    ["2026-08-07", "Electricity", -1800, "Bills"],
    ["2026-08-08", "Zomato", -740, "Food"],
    ["2026-08-10", "Gym", -1200, "Health"],
    ["2026-08-11", "College Books", -900, "Education"],
    ["2026-08-13", "Uber", -310, "Transport"],
    ["2026-08-15", "Restaurant", -1250, "Food"],
    ["2026-08-17", "Amazon", -890, "Shopping"],
    ["2026-08-19", "Flight Booking", -5200, "Travel"],
    ["2026-08-21", "Electricity", -1650, "Bills"],
    ["2026-08-23", "Swiggy", -680, "Food"],
    ["2026-08-25", "Uber", -290, "Transport"],
    ["2026-08-26", "Subscription", -299, "Subscriptions"],
    ["2026-08-27", "Zomato", -560, "Food"],
    ["2026-08-28", "Shopping", -1750, "Shopping"],
]

DEFAULT_BUDGETS = {
    "Housing": 18000, "Food": 5000, "Transport": 2500,
    "Shopping": 4000, "Entertainment": 2000, "Bills": 3500,
    "Health": 2000, "Education": 2000, "Travel": 6000,
    "Subscriptions": 1000, "Other": 2000
}

def normalize_transactions(df):
    """Validate and normalize a user CSV into MoneyFlow's canonical schema."""
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
        raise ValueError(
            "CSV is missing required columns: "
            + ", ".join(missing)
            + ". Required columns: date, merchant, amount. "
            + "Optional: category."
        )

    out = pd.DataFrame()
    out["date"] = pd.to_datetime(df[mapped["date"]], errors="coerce")
    out["merchant"] = df[mapped["merchant"]].astype(str).str.strip()
    out["amount"] = pd.to_numeric(
        df[mapped["amount"]].astype(str).str.replace(",", "", regex=False),
        errors="coerce",
    )
    if "category" in mapped:
        out["category"] = df[mapped["category"]].astype(str).str.strip()
    else:
        out["category"] = ""

    invalid = out["date"].isna() | out["merchant"].eq("") | out["amount"].isna()
    if invalid.any():
        st.warning(f"{int(invalid.sum())} row(s) failed validation and were removed.")

    out = out.loc[~invalid].copy()
    out["category"] = out["category"].where(
        out["category"].isin(CATEGORIES), ""
    )
    out["category"] = out.apply(
        lambda r: r["category"] if r["category"] else infer_category(r["merchant"], r["amount"]),
        axis=1,
    )
    return out.sort_values("date").reset_index(drop=True)

def infer_category(merchant, amount):
    """Simple transparent rule-based categorization for the MVP."""
    m = merchant.lower()
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
    return "Other" if amount < 0 else "Income"

def load_demo():
    return normalize_transactions(pd.DataFrame(
        DEMO_DATA, columns=["date", "merchant", "amount", "category"]
    ))

def init_state():
    if "transactions" not in st.session_state:
        st.session_state.transactions = load_demo()
    if "budgets" not in st.session_state:
        st.session_state.budgets = DEFAULT_BUDGETS.copy()
    if "goal_name" not in st.session_state:
        st.session_state.goal_name = "Emergency Fund"
    if "goal_target" not in st.session_state:
        st.session_state.goal_target = 50000.0
    if "goal_saved" not in st.session_state:
        st.session_state.goal_saved = 15000.0
    if "actions" not in st.session_state:
        st.session_state.actions = set()

def money(x):
    return f"₹{x:,.0f}"

def get_metrics(df):
    income = df.loc[df.amount > 0, "amount"].sum()
    expenses = -df.loc[df.amount < 0, "amount"].sum()
    net = income - expenses
    return income, expenses, net

def insights(df):
    income, expenses, net = get_metrics(df)
    spending = -df.loc[df.amount < 0].groupby("category")["amount"].sum().sort_values(ascending=False)
    items = []

    if expenses > income:
        items.append(("⚠️", "Expenses exceed income", "Review discretionary spending before adding new commitments.", "Review transactions"))
    if not spending.empty:
        top_cat = spending.index[0]
        top_val = spending.iloc[0]
        items.append(("📌", f"{top_cat} is your largest spending category", f"You spent {money(top_val)} here in the loaded period.", "Review category"))
    if "Subscriptions" in spending.index and spending["Subscriptions"] > 1000:
        items.append(("🔁", "Recurring subscription spend is notable", "Review subscriptions and keep only the services you actively use.", "Review subscriptions"))
    if net > 0:
        items.append(("💡", "Positive cash flow", f"You have {money(net)} left after recorded expenses.", "Update savings goal"))

    return items[:3]

init_state()

st.title("💸 MoneyFlow")
st.caption("Privacy-first personal finance check-in • Working MVP • Synthetic demo data")

with st.sidebar:
    st.header("Data")
    uploaded = st.file_uploader(
        "Upload a CSV",
        type=["csv"],
        help="Required columns: date, merchant, amount. Optional: category.",
    )
    if uploaded:
        try:
            df_new = pd.read_csv(uploaded)
            st.session_state.transactions = normalize_transactions(df_new)
            st.success("CSV loaded successfully.")
        except Exception as e:
            st.error(str(e))

    if st.button("Reset to demo data", use_container_width=True):
        st.session_state.transactions = load_demo()
        st.session_state.actions = set()
        st.rerun()

    st.divider()
    st.info(
        "Demo only. Use synthetic or non-sensitive data. "
        "Do not upload bank credentials, OTPs, card numbers, or other secrets."
    )

df = st.session_state.transactions.copy()

# Dashboard
income, expenses, net = get_metrics(df)
spending = -df.loc[df.amount < 0].groupby("category")["amount"].sum().sort_values(ascending=False)

st.subheader("Your financial check-in")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Income", money(income))
c2.metric("Expenses", money(expenses))
c3.metric("Net cash flow", money(net))
safe_to_spend = max(net * 0.35, 0)
c4.metric("Illustrative safe-to-spend", money(safe_to_spend), help="Demo heuristic only, not financial advice.")

st.divider()

left, right = st.columns([1.3, 1])
with left:
    st.subheader("What changed?")
    ins = insights(df)
    if not ins:
        st.success("No major insight detected.")
    for icon, title, body, action in ins:
        with st.container(border=True):
            st.markdown(f"### {icon} {title}")
            st.write(body)
            key = f"{title}-{action}"
            if st.button(action, key=key):
                st.session_state.actions.add(key)
                st.success("Action recorded for this demo session.")

with right:
    st.subheader("Spending by category")
    if spending.empty:
        st.info("No expenses available.")
    else:
        st.bar_chart(spending)

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["Transactions", "Plan", "Goal", "Product Metrics"])

with tab1:
    st.subheader("Transactions")
    search = st.text_input("Search merchant", "")
    view = df.copy()
    if search:
        view = view[view.merchant.str.contains(search, case=False, na=False)]

    edited = st.data_editor(
        view[["date", "merchant", "amount", "category"]].assign(
            date=view["date"].dt.date
        ),
        use_container_width=True,
        hide_index=True,
        column_config={
            "date": st.column_config.DateColumn("Date"),
            "amount": st.column_config.NumberColumn("Amount (₹)", format="₹%.0f"),
            "category": st.column_config.SelectboxColumn(
                "Category", options=CATEGORIES, required=True
            ),
        },
        disabled=["date", "merchant", "amount"],
        key="transaction_editor",
    )

    if st.button("Save category corrections"):
        if not view.empty:
            for idx, row in edited.iterrows():
                original_idx = idx
                st.session_state.transactions.loc[original_idx, "category"] = row["category"]
            st.session_state.actions.add("category_correction")
            st.success("Category corrections saved for this session.")
            st.rerun()

with tab2:
    st.subheader("Flexible budget")
    st.write("Set monthly category limits. These are planning inputs, not financial advice.")
    for category in sorted(st.session_state.budgets):
        spent = float(spending.get(category, 0))
        col1, col2, col3 = st.columns([2, 1, 2])
        col1.write(category)
        new_budget = col2.number_input(
            f"Budget for {category}",
            min_value=0.0,
            value=float(st.session_state.budgets[category]),
            step=500.0,
            key=f"budget_{category}",
            label_visibility="collapsed",
        )
        st.session_state.budgets[category] = new_budget
        st.session_state.actions.add("budget_adjustment")
        status = max(new_budget - spent, 0)
        col3.progress(
            min(spent / new_budget, 1.0) if new_budget else 0,
            text=f"{money(spent)} spent • {money(status)} remaining",
        )

with tab3:
    st.subheader("Savings goal")
    st.session_state.goal_name = st.text_input("Goal name", st.session_state.goal_name)
    st.session_state.goal_target = st.number_input(
        "Target amount (₹)", min_value=1.0,
        value=float(st.session_state.goal_target), step=1000.0
    )
    st.session_state.goal_saved = st.number_input(
        "Amount saved so far (₹)", min_value=0.0,
        value=float(st.session_state.goal_saved), step=500.0
    )
    st.session_state.actions.add("goal_update")
    progress = min(st.session_state.goal_saved / st.session_state.goal_target, 1.0)
    st.progress(progress, text=f"{progress:.0%} complete")
    st.metric("Remaining", money(max(st.session_state.goal_target - st.session_state.goal_saved, 0)))

with tab4:
    st.subheader("Product analytics — demo session")
    actionable = len(st.session_state.actions)
    activated = int(actionable > 0)
    metrics = pd.DataFrame({
        "Metric": [
            "Transactions loaded",
            "Actionable insights shown",
            "Actions completed",
            "Activation status",
        ],
        "Value": [
            len(df),
            len(insights(df)),
            actionable,
            "Activated" if activated else "Not yet activated",
        ]
    })
    st.dataframe(metrics, use_container_width=True, hide_index=True)
    st.caption(
        "These are session-level product instrumentation values, not market results or customer traction."
    )

st.divider()
st.caption("MoneyFlow MVP • Product-management case study • Synthetic/demo data only")
