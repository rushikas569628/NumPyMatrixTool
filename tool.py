# pip freeze > requirements.txt

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Advanced Matrix Calculator", layout="centered")
st.title("🧮 NumPyMatrixTool")

# --- Matrix Setup ---
matrix_count = st.number_input("How many matrices do you want to enter?", min_value=1, max_value=5, value=2)
matrices = {}
dimensions = {}

# --- Input Matrices ---
for i in range(matrix_count):
    name = chr(65 + i)  # A, B, C...
    st.markdown(f"### Matrix {name}")
    rows = st.number_input(f"Rows for Matrix {name}", min_value=1, max_value=10, value=2, key=f"r_{name}")
    cols = st.number_input(f"Cols for Matrix {name}", min_value=1, max_value=10, value=2, key=f"c_{name}")
    dimensions[name] = (rows, cols)

    data = []
    for r in range(int(rows)):
        row_vals = []
        cols_ = st.columns(int(cols))
        for c in range(int(cols)):
            val = cols_[c].number_input(f"{name}[{r+1},{c+1}]", key=f"{name}_{r}_{c}")
            row_vals.append(val)
        data.append(row_vals)
    matrices[name] = np.array(data)

# --- Heatmap Function ---
def plot_heatmap(matrix, title="Matrix Heatmap"):
    fig, ax = plt.subplots()
    sns.heatmap(matrix, annot=True, fmt=".2f", cmap="viridis", ax=ax)
    ax.set_title(title)
    st.pyplot(fig)

# --- Eigenvector Plot Function (2×2 only) ---
def plot_eigenvectors(matrix, eigvals, eigvecs, title="Eigenvector Visualization"):
    fig, ax = plt.subplots()
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.axhline(0, color='gray')
    ax.axvline(0, color='gray')

    for i in range(len(eigvals)):
        v = eigvecs[:, i]
        ax.arrow(0, 0, v[0], v[1], head_width=0.1, head_length=0.1, fc='red', ec='black')
        ax.text(v[0]*1.1, v[1]*1.1, f"v{i+1}", fontsize=10)
    ax.set_title(title)
    ax.grid(True)
    st.pyplot(fig)

# --- Operation Type Selection ---
st.markdown("### 🔧 Choose Operation Type")
op_type = st.radio("Operation Type", ["Binary (A+B, A@B)", "Unary (Transpose, Inverse, Rank, Det, Eigenvalues)"])

# --- Binary Operations ---
if op_type.startswith("Binary"):
    m1 = st.selectbox("Matrix 1", list(matrices.keys()), key="m1")
    m2 = st.selectbox("Matrix 2", list(matrices.keys()), key="m2")
    bin_op = st.selectbox("Binary Operation", ["Add", "Subtract", "Multiply"])

    if st.button("Calculate Binary Operation"):
        A = matrices[m1]
        B = matrices[m2]

        try:
            if bin_op == "Add":
                if A.shape != B.shape:
                    st.error("Addition requires same shapes.")
                else:
                    result = A + B
                    st.write("### ✅ Result")
                    st.write(result)
                    plot_heatmap(result, title="Result Heatmap")

            elif bin_op == "Subtract":
                if A.shape != B.shape:
                    st.error("Subtraction requires same shapes.")
                else:
                    result = A - B
                    st.write("### ✅ Result")
                    st.write(result)
                    plot_heatmap(result, title="Result Heatmap")

            elif bin_op == "Multiply":
                if A.shape[1] != B.shape[0]:
                    st.error("Matrix multiplication requires A.cols == B.rows")
                else:
                    result = A @ B
                    st.write("### ✅ Result")
                    st.write(result)
                    plot_heatmap(result, title="Result Heatmap")

        except Exception as e:
            st.error(f"Error: {e}")

# --- Unary Operations ---
else:
    m = st.selectbox("Select Matrix", list(matrices.keys()), key="unary")
    unary_op = st.selectbox("Unary Operation", ["Transpose", "Inverse", "Rank", "Determinant", "Eigenvalues"])

    if st.button("Calculate Unary Operation"):
        M = matrices[m]
        try:
            if unary_op == "Transpose":
                result = M.T
                st.write("### ✅ Transpose")
                st.write(result)
                plot_heatmap(result, title=f"Transpose of {m}")

            elif unary_op == "Inverse":
                if M.shape[0] != M.shape[1]:
                    st.error("Inverse requires square matrix.")
                else:
                    result = np.linalg.inv(M)
                    st.write("### ✅ Inverse")
                    st.write(result)
                    plot_heatmap(result, title=f"Inverse of {m}")

            elif unary_op == "Rank":
                rank = np.linalg.matrix_rank(M)
                st.write("### ✅ Rank:", rank)
                plot_heatmap(M, title=f"Matrix {m}")

            elif unary_op == "Determinant":
                if M.shape[0] != M.shape[1]:
                    st.error("Determinant requires square matrix.")
                else:
                    det = np.linalg.det(M)
                    st.write("### ✅ Determinant:", round(det, 4))
                    plot_heatmap(M, title=f"Matrix {m}")

            elif unary_op == "Eigenvalues":
                if M.shape[0] != M.shape[1]:
                    st.error("Eigenvalue calc requires square matrix.")
                else:
                    eigvals, eigvecs = np.linalg.eig(M)
                    st.write("### ✅ Eigenvalues:")
                    st.write(np.round(eigvals, 4))
                    st.write("### 🧭 Eigenvectors:")
                    st.write(np.round(eigvecs, 4))
                    plot_heatmap(M, title=f"Matrix {m}")
                    if M.shape == (2, 2):
                        plot_eigenvectors(M, eigvals, eigvecs)
                    else:
                        st.warning("Eigenvector visualization is supported for 2×2 matrices only.")

        except np.linalg.LinAlgError:
            st.error("Matrix is singular or invalid for this operation.")
        except Exception as e:
            st.error(f"Error: {e}")
