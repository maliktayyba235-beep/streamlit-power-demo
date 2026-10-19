import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import altair as alt

st.set_page_config(
    page_title="Streamlit Power Demo",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Streamlit Power Demo")
st.markdown("A tour of Streamlit's plotting & graphing capabilities.")

# ---------------------------------------------------------------------------
# Sidebar controls
# ---------------------------------------------------------------------------
st.sidebar.header("Controls")
n_points = st.sidebar.slider("Number of data points", 50, 1000, 300, step=50)
seed = st.sidebar.number_input("Random seed", 0, 100, 42)
chart_theme = st.sidebar.selectbox("Plotly theme", ["plotly", "plotly_white", "ggplot2", "simple_white"])

rng = np.random.default_rng(seed)
x = np.linspace(0, 10, n_points)
trend = np.sin(x) + 0.2 * x
noise = rng.normal(0, 0.3, n_points)
y = trend + noise

df = pd.DataFrame({"x": x, "y": y, "trend": trend, "category": rng.choice(["A", "B", "C"], n_points)})

# ---------------------------------------------------------------------------
# Metrics row
# ---------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Data points", n_points)
col2.metric("Mean y", f"{df['y'].mean():.3f}")
col3.metric("Std y", f"{df['y'].std():.3f}")
col4.metric("Max y", f"{df['y'].max():.3f}")

st.divider()

# ---------------------------------------------------------------------------
# Native Streamlit charts
# ---------------------------------------------------------------------------
st.header("1. Native Streamlit Charts")

st.subheader("Line chart")
st.line_chart(df.set_index("x")[["y", "trend"]])

st.subheader("Area chart")
st.area_chart(df.set_index("x")[["y"]])

st.subheader("Bar chart (aggregated by category)")
bar_data = df.groupby("category")["y"].mean().reset_index()
st.bar_chart(bar_data.set_index("category")["y"])

st.divider()

# ---------------------------------------------------------------------------
# Matplotlib
# ---------------------------------------------------------------------------
st.header("2. Matplotlib Figure")
fig, ax = plt.subplots(figsize=(10, 4))
ax.scatter(df["x"], df["y"], c=df["y"], cmap="viridis", s=10, alpha=0.7)
ax.plot(df["x"], df["trend"], color="red", linewidth=2, label="trend")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Scatter with trend overlay")
ax.legend()
st.pyplot(fig)

st.divider()

# ---------------------------------------------------------------------------
# Plotly interactive charts
# ---------------------------------------------------------------------------
st.header("3. Plotly Interactive Charts")

pc1, pc2 = st.columns(2)

with pc1:
    st.subheader("Plotly Express scatter")
    fig_px = px.scatter(
        df, x="x", y="y", color="category",
        title="Scatter colored by category",
        template=chart_theme,
    )
    st.plotly_chart(fig_px, use_container_width=True)

with pc2:
    st.subheader("Plotly Express line")
    fig_line = px.line(
        df, x="x", y=["y", "trend"],
        title="Signal + trend",
        template=chart_theme,
    )
    st.plotly_chart(fig_line, use_container_width=True)

st.subheader("Plotly Graph Objects: combined bar + line")
agg = df.groupby("category").agg(mean_y=("y", "mean"), count=("y", "count")).reset_index()
fig_go = go.Figure()
fig_go.add_trace(go.Bar(x=agg["category"], y=agg["mean_y"], name="mean y"))
fig_go.add_trace(go.Scatter(x=agg["category"], y=agg["count"], name="count", yaxis="y2"))
fig_go.update_layout(
    title="Bar (mean y) + Line (count)",
    yaxis=dict(title="mean y"),
    yaxis2=dict(title="count", overlaying="y", side="right"),
    template=chart_theme,
)
st.plotly_chart(fig_go, use_container_width=True)

st.subheader("Plotly 3D surface")
grid = np.linspace(-3, 3, 40)
Xg, Yg = np.meshgrid(grid, grid)
Zg = np.sin(np.sqrt(Xg**2 + Yg**2))
fig_surf = go.Figure(data=[go.Surface(z=Zg, x=grid, y=grid, colorscale="Pinkyl")])
fig_surf.update_layout(title="3D surface", template=chart_theme)
st.plotly_chart(fig_surf, use_container_width=True)

st.divider()

# ---------------------------------------------------------------------------
# Altair charts
# ---------------------------------------------------------------------------
st.header("4. Altair Charts")

st.subheader("Altair layered scatter + smooth line")
base = alt.Chart(df).encode(x="x:Q")
points = base.mark_circle(size=20, opacity=0.5).encode(y="y:Q", color="category:N")
line = base.mark_line(color="red", strokeWidth=2).encode(y="trend:Q")
st.altair_chart((points + line).properties(width=800, height=350), use_container_width=True)

st.subheader("Altair histogram")
hist = alt.Chart(df).mark_bar().encode(
    x=alt.X("y:Q", bin=alt.Bin(maxbins=30)),
    y="count():Q",
    color="category:N",
).properties(width=800, height=300)
st.altair_chart(hist, use_container_width=True)

st.divider()

# ---------------------------------------------------------------------------
# DataFrame + downloadable
# ---------------------------------------------------------------------------
st.header("5. DataFrame display")
st.dataframe(df.head(20), use_container_width=True)

st.subheader("Download sample data as CSV")
st.download_button(
    label="Download CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="sample_data.csv",
    mime="text/csv",
)

st.success("Done — that's a tour of Streamlit's plotting power!")