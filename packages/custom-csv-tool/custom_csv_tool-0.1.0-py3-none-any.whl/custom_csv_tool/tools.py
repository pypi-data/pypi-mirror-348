from crewai.tools import BaseTool
from typing import Type
import pandas as pd
import os
from pydantic import BaseModel, Field
import uuid
import datetime
import io
import random
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

def resolve_path(file_path):
    if 'data/' in file_path:
        return file_path
    if os.path.exists(file_path):
        return file_path
    data_path = os.path.join('data', file_path)
    if os.path.exists(data_path):
        return data_path
    base_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(base_dir)))
    abs_path = os.path.join(project_root, file_path)
    if os.path.exists(abs_path):
        return abs_path
    data_abs_path = os.path.join(project_root, 'data', os.path.basename(file_path))
    if os.path.exists(data_abs_path):
        return data_abs_path
    return file_path

class ReadCSVInput(BaseModel):
    file_path: str = Field(..., description="Path to the CSV file to read.")

class ReadCSVTool(BaseTool):
    name: str = "Read CSV File"
    description: str = (
        "Reads a CSV file from Azure Blob Storage and returns the data as a formatted string."
    )
    args_schema: Type[BaseModel] = ReadCSVInput

    def _run(self, file_path: str) -> str:
        try:
            print(f"Attempting to read CSV from Azure Blob: {file_path}")
            connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
            if not connection_string:
                return "Error: AZURE_STORAGE_CONNECTION_STRING environment variable not set"
            container_name = "data"
            blob_name = os.path.basename(file_path)
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            container_client = blob_service_client.get_container_client(container_name)
            blob_client = container_client.get_blob_client(blob_name)
            blob_data = blob_client.download_blob().readall()
            df = pd.read_csv(io.BytesIO(blob_data))
            return df.to_string()
        except Exception as e:
            return f"Error reading CSV file from Azure Blob Storage: {str(e)}"

class CompareInventoryInput(BaseModel):
    forecast_path: str = Field(..., description="Path to the demand forecast CSV file.")
    inventory_path: str = Field(..., description="Path to the current inventory CSV file.")

class CompareInventoryTool(BaseTool):
    name: str = "Compare Inventory"
    description: str = (
        "Compares demand forecast with current inventory and identifies raw materials that need restocking."
    )
    args_schema: Type[BaseModel] = CompareInventoryInput

    def _run(self, forecast_path: str, inventory_path: str) -> str:
        try:
            forecast_path = resolve_path(forecast_path)
            inventory_path = resolve_path(inventory_path)
            print(f"Reading forecast from: {forecast_path}")
            print(f"Reading inventory from: {inventory_path}")
            forecast_df = pd.read_csv(forecast_path)
            inventory_df = pd.read_csv(inventory_path)
            merged_df = pd.merge(
                forecast_df,
                inventory_df,
                on='RawMaterial_ID',
                suffixes=('_forecast', '')
            )
            merged_df['required_quantity'] = merged_df['RawMaterial_QuantityRequired'] - merged_df['RawMaterial_CurrentQuantity']
            shortage_df = merged_df[merged_df['required_quantity'] > 0]
            if shortage_df.empty:
                return "No raw materials need restocking. All current inventory levels are sufficient for forecast."
            else:
                result = "Raw materials that need restocking:\n\n"
                result += shortage_df[['RawMaterial_ID', 'RawMaterial_Name', 'RawMaterial_QuantityRequired',
                                      'RawMaterial_CurrentQuantity', 'required_quantity']].to_string()
                return result
        except Exception as e:
            return f"Error comparing inventory: {str(e)}"

class CreatePurchaseOrderInput(BaseModel):
    forecast_path: str = Field(..., description="Path to the demand forecast CSV file.")
    inventory_path: str = Field(..., description="Path to the current inventory CSV file.")
    output_path: str = Field(..., description="Path to save the purchase order CSV file.")

class CreatePurchaseOrderTool(BaseTool):
    name: str = "Create Purchase Order"
    description: str = (
        "Creates a purchase order CSV file for raw materials where forecasted quantity exceeds current inventory."
    )
    args_schema: Type[BaseModel] = CreatePurchaseOrderInput

    def _run(self, forecast_path: str, inventory_path: str, output_path: str) -> str:
        try:
            forecast_path = resolve_path(forecast_path)
            inventory_path = resolve_path(inventory_path)
            print(f"Reading forecast from: {forecast_path}")
            print(f"Reading inventory from: {inventory_path}")
            forecast_df = pd.read_csv(forecast_path)
            inventory_df = pd.read_csv(inventory_path)
            merged_df = pd.merge(
                forecast_df,
                inventory_df,
                on='RawMaterial_ID',
                suffixes=('_forecast', '')
            )
            merged_df['required_quantity'] = merged_df['RawMaterial_QuantityRequired'] - merged_df['RawMaterial_CurrentQuantity']
            purchase_order_df = merged_df[merged_df['required_quantity'] > 0]
            if purchase_order_df.empty:
                return "No purchase order created. All inventory levels are sufficient."
            po_df = purchase_order_df[['RawMaterial_ID', 'RawMaterial_Name', 'required_quantity']]
            po_df = po_df.rename(columns={'required_quantity': 'RawMaterial_Quantity'})
            today = datetime.datetime.now()
            po_id = f"PO-{today.strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
            po_df['Purchase_Order_ID'] = po_id
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            po_df.to_csv(output_path, index=False)
            summary = f"Purchase order {po_id} created at {output_path} with {len(po_df)} raw materials.\n\n"
            summary += "Summary of purchase order:\n"
            summary += po_df.to_string()
            return summary
        except Exception as e:
            return f"Error creating purchase order: {str(e)}"
