import streamlit as st
import pandas as pd
import numpy as np

st.title('Voltage Droop Control Simulation')

# Sidebar controls
st.sidebar.header('Parameters')
kQ_A = st.sidebar.slider('kQ_A', min_value=0.01, max_value=0.1, value=0.02, step=0.01)
kQ_B = st.sidebar.slider('kQ_B', min_value=0.01, max_value=0.1, value=0.03, step=0.01)
V_nom = st.sidebar.slider('V_nom', min_value=0.9, max_value=1.1, value=1.0, step=0.01)
Q_total = st.sidebar.slider('Q_total [MVAR]', min_value=1, max_value=20, value=10, step=1)

# Calculate Q_A and Q_B
Q_A = kQ_B * Q_total / (kQ_A + kQ_B)
Q_B = Q_total - Q_A

# Calculate final voltages
V_A = V_nom - kQ_A * Q_A
V_B = V_nom - kQ_B * Q_B

# Create data for the droop lines
Q_range = np.linspace(0, Q_total * 1.5, 100)
V_A_range = V_nom - kQ_A * Q_range
V_B_range = V_nom - kQ_B * Q_range

# Create DataFrame for the droop lines
df_droop = pd.DataFrame({
    'Q': Q_range,
    f'Source A (kQ={kQ_A:.2f})': V_A_range,
    f'Source B (kQ={kQ_B:.2f})': V_B_range
})

# Create DataFrame for operating points
df_points = pd.DataFrame({
    'Q': [Q_A, Q_B],
    'V': [V_A, V_B],
    'Source': ['A', 'B']
})

# Display results
col1, col2 = st.columns(2)

with col1:
    st.subheader("System Parameters")
    st.write(f"Source A: Q = {Q_A:.2f} MVAR, V = {V_A:.2f} pu")
    st.write(f"Source B: Q = {Q_B:.2f} MVAR, V = {V_B:.2f} pu")
    st.write(f"Total Load: Q = {Q_total:.2f} MVAR")

with col2:
    st.subheader("Voltage Droop Characteristics")
    
    # Using Streamlit's native line chart
    st.line_chart(df_droop.set_index('Q'))
    
    # Add operating points using scatter chart
    st.scatter_chart(
        df_points,
        x='Q',
        y='V',
        color='Source',
        size=[100] * len(df_points)  # Fixed size for all points
    )

# Add explanatory text
st.markdown("""
### About this Simulation
This simulation demonstrates voltage droop control in a power system with two sources sharing reactive power load.
- **kQ_A** and **kQ_B**: Droop coefficients for sources A and B
- **V_nom**: Nominal voltage
- **Q_total**: Total reactive power load
""")
