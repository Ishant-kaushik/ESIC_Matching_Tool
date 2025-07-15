import pandas as pd
import gradio as gr
import os
import tempfile

def match_esic_contributions(annexure_file, portal_file):
    try:
        annexure_df = pd.read_excel(annexure_file.name, skiprows=2)
        portal_df = pd.read_excel(portal_file.name, skiprows=9)

        # Normalize annexure column names
        normalized_annexure_cols = {
            str(col).strip().lower(): col for col in annexure_df.columns
        }

        esic_number_key = next((k for k in normalized_annexure_cols if 'esic' in k and 'no' in k), None)
        esic_contrib_key = next((k for k in normalized_annexure_cols if 'esic' in k and '0.75' in k), None)

        if not esic_number_key or not esic_contrib_key:
            return "ERROR: Required columns not found", None

        esic_number_col = normalized_annexure_cols[esic_number_key]
        esic_contrib_col = normalized_annexure_cols[esic_contrib_key]

        annexure_df = annexure_df.rename(columns={
            esic_number_col: 'ESIC_NO',
            esic_contrib_col: 'ANNEXURE_CONTRIB'
        })

        portal_df.columns = portal_df.columns.str.strip()
        if 'IPNo' not in portal_df.columns or 'IPContribution' not in portal_df.columns:
            return "ERROR: Required columns not found in portal file", None

        comparison_df = annexure_df.merge(
            portal_df,
            left_on='ESIC_NO',
            right_on='IPNo',
            how='inner',
            suffixes=('_annexure', '_portal')
        )

        comparison_df['ANNEXURE_CONTRIB'] = pd.to_numeric(comparison_df['ANNEXURE_CONTRIB'], errors='coerce').round(2)
        comparison_df['IPContribution'] = pd.to_numeric(comparison_df['IPContribution'], errors='coerce').round(2)
        comparison_df['Match'] = comparison_df['ANNEXURE_CONTRIB'] == comparison_df['IPContribution']

        total = len(comparison_df)
        matched = comparison_df['Match'].sum()
        mismatched = total - matched

        # Save result to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
        comparison_df.to_excel(temp_file.name, index=False)

        summary = f"""
        ✅ Total compared: {total}
        ✅ Total matched: {matched}
        ❌ Total mismatched: {mismatched}
        """

        return summary, temp_file.name

    except Exception as e:
        return f"ERROR: {str(e)}", None

# Gradio UI
iface = gr.Interface(
    fn=match_esic_contributions,
    inputs=[
        gr.File(label="Upload Annexure File (.xlsx)"),
        gr.File(label="Upload Portal File (.xlsx)")
    ],
    outputs=[
        gr.Textbox(label="Comparison Summary"),
        gr.File(label="Download Comparison Result (.xlsx)")
    ],
    title="ESIC Contribution Matcher",
    description="Upload your Annexure and Portal files to match ESIC contributions (0.75%)"
)

if __name__ == "__main__":
    iface.launch()
