import streamlit as st
import httpx
import time
import pandas as pd
import glob

# 1. Page Configuration
st.set_page_config(page_title="LLM Evaluation and RTF", page_icon="🛡️", layout="wide")
API_URL = "http://localhost:8000/api/evaluate"

# --- DYNAMIC LOADER FUNCTIONS ---
def get_available_datasets():
    """Scans the datasets directory and returns all JSON files."""
    files = glob.glob("app/datasets/*.json")
    # Clean up Windows backslashes for a cleaner UI
    return [f.replace("\\", "/") for f in files]

# 2. Main Header
st.title("🛡️ LLM Evaluation and Red teaminng framework")
st.markdown("Automated Red Teaming and Performance Benchmarking for Large Language Models.")

# 3. Sidebar Controls
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # --- DYNAMIC DATASETS ---
    available_datasets = get_available_datasets()
    
    selected_datasets = st.multiselect(
        "Select Datasets",
        options=available_datasets,
        default=available_datasets  # Automatically selects all found files by default!
    )
    
    # --- DYNAMIC MODELS ---
    st.markdown("### Models")
    standard_models = [
        "gemini-3.5-flash", 
        "openai/gpt-4o-mini", 
        "meta-llama/llama-3.1-8b-instruct:free",
        "anthropic/claude-3-haiku"
    ]
    
    selected_models = st.multiselect(
        "Select from Presets",
        options=standard_models,
        default=["google/gemini-2.5-flash"]
    )
    
    # Allow the user to type in ANY OpenRouter model dynamically
    custom_model = st.text_input("Or inject a custom model (e.g., cohere/command-r)")
    
    st.divider()
    concurrency = st.slider("Concurrency Limit", min_value=1, max_value=5, value=2)
    
    run_button = st.button("🚀 Run Evaluation", use_container_width=True, type="primary")

# 4. Execution & Visualization Logic
if run_button:
    # Compile the final list of models (Presets + Custom Input)
    final_models = list(selected_models)
    if custom_model and custom_model not in final_models:
        final_models.append(custom_model)

    if not final_models or not selected_datasets:
        st.error("⚠️ Please select at least one model and one dataset.")
    else:
        with st.spinner(f"Evaluating {len(final_models)} model(s) across {len(selected_datasets)} dataset(s)..."):
            
            payload = {
                "models": final_models,
                "datasets": selected_datasets,
                "concurrency_limit": concurrency
            }
            
            try:
                start_time = time.time()
                
                with httpx.Client(timeout=300.0) as client:
                    response = client.post(API_URL, json=payload)
                    response.raise_for_status()
                    data = response.json()
                    
                elapsed_time = round(time.time() - start_time, 2)
                st.success(f"✅ Evaluation completed in {elapsed_time} seconds!")
                
                # 5. Render the Results
                results = data.get("results", {})
                
                for model, output in results.items():
                    st.subheader(f"📊 Results: `{model}`")
                    
                    if output.get("status") == "success":
                        metrics = output.get("metrics", {}).get("summary", {})
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Safety Alignment", f"{metrics.get('overall_safety_alignment_pct', 0)}%")
                        with col2:
                            st.metric("Avg Latency", f"{metrics.get('average_latency_seconds', 0)}s")
                        with col3:
                            st.metric("Failed Prompts", metrics.get('failed_executions', 0))
                            
                        categories = output.get("metrics", {}).get("breakdown_by_category", {})
                        if categories:
                            df = pd.DataFrame([
                                {"Category": cat, "Safety Score (%)": data["safety_alignment_pct"]}
                                for cat, data in categories.items()
                            ])
                            st.bar_chart(df, x="Category", y="Safety Score (%)", color="#1f77b4")
                            
                        st.caption(f"Raw report saved to: `{output.get('report_file')}`")
                    else:
                        st.error(f"Failed: {output.get('message')}")
                    
                    st.divider()
                    
            except httpx.ConnectError:
                st.error("❌ Failed to connect. Is your FastAPI backend running on port 8000?")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
else:
    st.info("👈 Select your parameters in the sidebar and click **Run Evaluation** to begin.")
    st.markdown("### System Status")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="API Connection", value="Awaiting Execution...")
    with col2:
        st.metric(label="Storage Engine", value="Active (JSON/Disk)")