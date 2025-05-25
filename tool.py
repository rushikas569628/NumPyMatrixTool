import streamlit as st
import numpy as np

st.set_page_config(page_title="Flexible Matrix Calculator", layout="centered")
st.title("🧮 Flexible Matrix Calculator")

# Step 1: How many matrices?
matrix_count = st.radio("How many matrices do you want to use?", [1, 2])

# Step 2: Dimensions per matrix
st.markdown("### Matrix A Dimensions")
rows_a = st.number_input("Rows (A)", min_value=1, max_value=10, value=2, key="rows_a")
cols_a = st.number_input("Cols (A)", min_value=1, max_value=10, value=2, key="cols_a")

if matrix_count == 2:
    st.markdown("### Matrix B Dimensions")
    rows_b = st.number_input("Rows (B)", min_value=1, max_value=10, value=2, key="rows_b")
    cols_b = st.number_input("Cols (B)", min_value=1, max_value=10, value=2, key="cols_b")

# Step 3: Input for Matrix A
st.markdown("### Matrix A")
matrix_a = []
for i in range(int(rows_a)):
    row = []
    cols_ = st.columns(int(cols_a))
    for j in range(int(cols_a)):
        row.append(cols_[j].number_input(f"A[{i+1},{j+1}]", key=f"a_{i}_{j}"))
    matrix_a.append(row)
A = np.array(matrix_a)

# Step 4: Input for Matrix B if applicable
if matrix_count == 2:
    st.markdown("### Matrix B")
    matrix_b = []
    for i in range(int(rows_b)):
        row = []
        cols_ = st.columns(int(cols_b))
        for j in range(int(cols_b)):
            row.append(cols_[j].number_input(f"B[{i+1},{j+1}]", key=f"b_{i}_{j}"))
        matrix_b.append(row)
    B = np.array(matrix_b)

# Step 5: Operation selection
st.markdown("### Choose Operation")
if matrix_count == 1:
    operations = ["Transpose A", "Inverse A"]
else:
    operations = ["Add", "Subtract", "Multiply", "Transpose A", "Transpose B", "Inverse A", "Inverse B"]

operation = st.selectbox("Select Operation", operations)

# Step 6: Perform Operation
def perform_operation():
    try:
        if operation == "Add":
            if A.shape != B.shape:
                st.error("Addition requires matrices of the same shape.")
                return None
            return A + B
        elif operation == "Subtract":
            if A.shape != B.shape:
                st.error("Subtraction requires matrices of the same shape.")
                return None
            return A - B
        elif operation == "Multiply":
            if A.shape[1] != B.shape[0]:
                st.error("Multiplication requires A.columns == B.rows.")
                return None
            return A @ B
        elif operation == "Transpose A":
            return A.T
        elif operation == "Transpose B":
            return B.T
        elif operation == "Inverse A":
            if A.shape[0] != A.shape[1]:
                st.error("Inverse of A requires a square matrix.")
                return None
            return np.linalg.inv(A)
        elif operation == "Inverse B":
            if B.shape[0] != B.shape[1]:
                st.error("Inverse of B requires a square matrix.")
                return None
            return np.linalg.inv(B)
    except np.linalg.LinAlgError:
        st.error("Matrix is singular or non-invertible.")
    return None

# Step 7: Show result
if st.button("Calculate"):
    result = perform_operation()
    if result is not None:
        st.markdown("### ✅ Result")
        st.write(result)
