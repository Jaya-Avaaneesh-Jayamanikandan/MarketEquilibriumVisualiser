import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Market Equilibrium Visualiser",
    page_icon="📈",
    layout="wide"
)

st.title("Market Equilibrium Visualiser")
st.subheader("Built for CBSE Class 12 Commerce students")

st.markdown("""
This visualisation tool is intended to help students understand:

- Law of Demand
- Law of Supply
- Market Equilibrium
- Surplus
- Shortage
""")

# ---------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------

st.sidebar.header("Demand Settings")

demand_intercept = st.sidebar.slider(
    "Demand Intercept",
    min_value=20,
    max_value=200,
    value=120
)

demand_slope = st.sidebar.slider(
    "Demand Slope",
    min_value=0.5,
    max_value=5.0,
    value=1.5,
    step=0.1
)

st.sidebar.header("Supply Settings")

supply_intercept = st.sidebar.slider(
    "Supply Intercept",
    min_value=-50,
    max_value=100,
    value=20
)

supply_slope = st.sidebar.slider(
    "Supply Slope",
    min_value=0.5,
    max_value=5.0,
    value=1.0,
    step=0.1
)

st.sidebar.header("Market Price")

market_price = st.sidebar.slider(
    "Current Market Price",
    min_value=0,
    max_value=150,
    value=50
)

# ---------------------------------------------------
# Demand and Supply Equations
# ---------------------------------------------------

quantity = np.linspace(0, 120, 500)

demand_price = demand_intercept - demand_slope * quantity
supply_price = supply_intercept + supply_slope * quantity

# ---------------------------------------------------
# Equilibrium
# ---------------------------------------------------

equilibrium_quantity = (
    demand_intercept - supply_intercept
) / (demand_slope + supply_slope)

equilibrium_price = (
    supply_intercept +
    supply_slope * equilibrium_quantity
)

# ---------------------------------------------------
# Current Market Analysis
# ---------------------------------------------------

quantity_demanded = max(
    (demand_intercept - market_price) / demand_slope,
    0
)

quantity_supplied = max(
    (market_price - supply_intercept) / supply_slope,
    0
)

difference = quantity_demanded - quantity_supplied

if difference > 0:
    market_status = "Shortage"
elif difference < 0:
    market_status = "Surplus"
else:
    market_status = "Equilibrium"

# ---------------------------------------------------
# Metrics
# ---------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Equilibrium Price",
        f"{equilibrium_price:.2f}"
    )

with col2:
    st.metric(
        "Equilibrium Quantity",
        f"{equilibrium_quantity:.2f}"
    )

with col3:
    st.metric(
        "Market Status",
        market_status
    )

# ---------------------------------------------------
# Graph
# ---------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 7))

ax.plot(
    quantity,
    demand_price,
    label="Demand Curve",
    linewidth=3,
    color="blue"
)

ax.plot(
    quantity,
    supply_price,
    label="Supply Curve",
    linewidth=3,
    color="green"
)

# Equilibrium Point
ax.scatter(
    equilibrium_quantity,
    equilibrium_price,
    color="red",
    s=150,
    zorder=5,
    label="Equilibrium"
)

# Current Market Price
ax.axhline(
    market_price,
    color="orange",
    linestyle="--",
    linewidth=2,
    label=f"Market Price = {market_price}"
)

# Shortage / Surplus Highlight
if market_status == "Shortage":
    ax.fill_betweenx(
        [market_price - 1, market_price + 1],
        quantity_supplied,
        quantity_demanded,
        color="red",
        alpha=0.3,
        label="Shortage"
    )

elif market_status == "Surplus":
    ax.fill_betweenx(
        [market_price - 1, market_price + 1],
        quantity_demanded,
        quantity_supplied,
        color="purple",
        alpha=0.3,
        label="Surplus"
    )

ax.set_title("Market Equilibrium")
ax.set_xlabel("Quantity")
ax.set_ylabel("Price")

ax.grid(True, alpha=0.3)
ax.legend()

ax.set_xlim(0, 120)
ax.set_ylim(0, max(demand_intercept + 20, 150))

st.pyplot(fig)

# ---------------------------------------------------
# Explanation Box
# ---------------------------------------------------

st.markdown("---")

st.subheader("Economic Interpretation")

if market_status == "Shortage":
    st.error(
        f"""
        SHORTAGE

        Quantity Demanded = {quantity_demanded:.2f}

        Quantity Supplied = {quantity_supplied:.2f}

        Demand exceeds supply.

        Buyers compete for limited goods,
        pushing prices upward toward equilibrium.
        """
    )

elif market_status == "Surplus":
    st.warning(
        f"""
        SURPLUS

        Quantity Demanded = {quantity_demanded:.2f}

        Quantity Supplied = {quantity_supplied:.2f}

        Supply exceeds demand.

        Sellers reduce prices to clear excess stock.
        """
    )

else:
    st.success(
        """
        MARKET EQUILIBRIUM

        Quantity Demanded = Quantity Supplied.

        No pressure for prices to rise or fall.
        """
    )

# ---------------------------------------------------
# Exam Notes
# ---------------------------------------------------

st.markdown("---")

st.subheader("Quick Vocabulary Reference")

st.markdown("""
### Law of Demand
As price rises, quantity demanded falls.

### Law of Supply
As price rises, quantity supplied rises.

### Market Equilibrium
Occurs where Demand = Supply.

### Shortage
Price is below equilibrium price.

### Surplus
Price is above equilibrium price.
""")