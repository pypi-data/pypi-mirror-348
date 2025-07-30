# ml_eval_dashboard/dashboard.py

from ml_eval_dashboard.report_generator import generate_pdf_report
import streamlit as st
import pandas as pd
from ml_eval_dashboard.evaluator import evaluate, get_task_type
from ml_eval_dashboard.visualizer import (
    plot_class_distribution,
    plot_confusion_matrix,
    plot_error_distribution,
    plot_roc_curve,
    plot_precision_recall_curve
)
from sklearn.metrics import confusion_matrix
import base64
import os

def download_link(filepath, label):
    with open(filepath, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    href = f'<a href="data:file/png;base64,{b64}" download="{os.path.basename(filepath)}" style="text-decoration:none">{label}</a>'
    return href

def display_image_with_download(image_path, caption):
    st.image(image_path, caption=caption)
    st.markdown(download_link(image_path, f"⬇️ Download {caption}"), unsafe_allow_html=True)
    st.markdown("---")

def rounded_metrics_df(metrics_dict):
    df = pd.DataFrame(metrics_dict, index=[0]).T.rename(columns={0: "Score"})
    df["Score"] = df["Score"].apply(lambda x: round(x, 4))
    return df

def run_dashboard():
    st.set_page_config(page_title="ML Evaluation Dashboard", layout="wide")
    st.title("📊 Machine Learning Evaluation Dashboard")

    st.sidebar.header("Upload & Settings")
    uploaded_files = st.sidebar.file_uploader(
        "Upload CSV files (multiple allowed)",
        accept_multiple_files=True,
        type=["csv"],
        help="Each CSV must have columns: y_true, y_pred. Optionally y_prob or y_prob_classX for classification probabilities."
    )

    if not uploaded_files:
        st.info("Please upload one or more CSV files with your predictions on the left sidebar.")
    else:
        comparison = {}
        for uploaded_file in uploaded_files:
            st.markdown(f"---\n## 📁 File: {uploaded_file.name}")

            try:
                df = pd.read_csv(uploaded_file)
            except Exception as e:
                st.error(f"Error reading {uploaded_file.name}: {e}")
                continue

            if 'y_true' not in df.columns or 'y_pred' not in df.columns:
                st.error("CSV must contain 'y_true' and 'y_pred' columns.")
                continue

            y_true = df['y_true']
            y_pred = df['y_pred']

            y_prob = None
            prob_cols = [col for col in df.columns if col.startswith('y_prob')]
            if len(prob_cols) == 1:
                y_prob = df[prob_cols[0]]
            elif len(prob_cols) > 1:
                y_prob = df[prob_cols]

            task_type = get_task_type(y_true)
            result = evaluate(y_true, y_pred)
            comparison[uploaded_file.name] = result

            st.subheader("📈 Evaluation Metrics")
            st.dataframe(rounded_metrics_df(result), use_container_width=True)

            tabs = st.tabs(["📊 Plots", "📄 Generate Report"])

            with tabs[0]:
                st.subheader("Visualizations")

                class_dist_path = plot_class_distribution(y_true)
                display_image_with_download(class_dist_path, "Class Distribution")

                if task_type == "classification":
                    if len(set(y_true)) < 20:
                        cm = confusion_matrix(y_true, y_pred)
                        cm_path = plot_confusion_matrix(cm, sorted(set(y_true)))
                        display_image_with_download(cm_path, "Confusion Matrix")

                    if y_prob is not None:
                        roc_path = plot_roc_curve(y_true, y_prob)
                        display_image_with_download(roc_path, "ROC Curve")

                        pr_path = plot_precision_recall_curve(y_true, y_prob)
                        display_image_with_download(pr_path, "Precision-Recall Curve")

                elif task_type == "regression":
                    err_dist_path = plot_error_distribution(y_true, y_pred)
                    display_image_with_download(err_dist_path, "Error Distribution")

            with tabs[1]:
                st.subheader("Download PDF Report")
                if st.button(f"📄 Generate PDF Report for {uploaded_file.name}"):
                    with st.spinner("Generating PDF report..."):
                        image_paths = {"Class Distribution": class_dist_path}

                        if task_type == "classification" and len(set(y_true)) < 20:
                            image_paths["Confusion Matrix"] = cm_path
                        if task_type == "classification" and y_prob is not None:
                            image_paths["ROC Curve"] = roc_path
                            image_paths["Precision-Recall Curve"] = pr_path
                        if task_type == "regression":
                            image_paths["Error Distribution"] = err_dist_path

                        pdf_path = generate_pdf_report(uploaded_file.name, result, image_paths)
                        with open(pdf_path, "rb") as f:
                            b64 = base64.b64encode(f.read()).decode()
                            href = f'<a href="data:application/pdf;base64,{b64}" download="{pdf_path}" style="font-size:18px; font-weight:bold">📥 Download PDF Report</a>'
                            st.markdown(href, unsafe_allow_html=True)

        if len(comparison) > 1:
            st.markdown("---")
            st.subheader("📊 Model Comparison")
            comp_df = pd.DataFrame(comparison).T
            comp_df = comp_df.round(4)
            st.dataframe(comp_df, use_container_width=True)

if __name__ == "__main__":
    run_dashboard()
