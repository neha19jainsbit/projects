# Insurance Premium Analytics (Standalone Streamlit App)

This is an isolated deployment-ready project for the Streamlit dashboard originally in `Data_Insights/app1.py`.

## Project Structure

- `app.py` - Streamlit dashboard app
- `insurance.csv` - Dataset used by the app
- `requirements.txt` - Python dependencies for deployment

## Run Locally

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   streamlit run app.py
   ```

## Deploy (Streamlit Community Cloud)

1. Push this folder as its own GitHub repository.
2. In Streamlit Community Cloud, set:
   - **Main file path**: `app.py`
   - **Python requirements**: `requirements.txt`
3. Deploy.

## Notes

- This project intentionally keeps data loading local (`insurance.csv` in same folder) to avoid path issues during deployment.
