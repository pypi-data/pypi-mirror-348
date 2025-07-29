from crewai.tools import BaseTool
from typing import Type
import pandas as pd
import os
from datetime import datetime
from pydantic import BaseModel, Field
import numpy as np

class EvaluateSuppliersInput(BaseModel):
    """Input schema for EvaluateSuppliers."""
    quotation_path: str = Field(..., description="Path to the supplier quotation CSV file.")
    historical_path: str = Field(..., description="Path to the supplier historical data CSV file.")
    output_path: str = Field(..., description="Path to save the supplier evaluation CSV file.")
    weights: dict = Field(default=None, description="Optional custom weights for evaluation criteria.")

class EvaluateSuppliersTool(BaseTool):
    name: str = "Evaluate Suppliers"
    description: str = (
        "Evaluates supplier quotations based on price, delivery date, supplier rating, and historical performance."
    )
    args_schema: Type[BaseModel] = EvaluateSuppliersInput

    def _run(self, quotation_path: str, historical_path: str, output_path: str, weights: dict = None) -> str:
        try:
            quotation_path = resolve_path(quotation_path)
            historical_path = resolve_path(historical_path)
            quotation_df = pd.read_csv(quotation_path)
            historical_df = pd.read_csv(historical_path)

            merged_df = pd.merge(
                quotation_df, 
                historical_df,
                on=['Supplier_ID', 'RawMaterial_ID'],
                suffixes=('', '_hist')
            )

            if weights is None:
                weights = {
                    'price': 0.4,
                    'delivery_date': 0.25,
                    'quality': 0.35,
                }

            grouped = merged_df.groupby(['RawMaterial_ID'])
            evaluation_results = []
            current_date = datetime.now()

            for raw_material_id, group in grouped:
                raw_material_name = group.iloc[0]['RawMaterial_Name']
                purchase_order_id = group.iloc[0]['Purchase_Order_ID']
                min_price = group['RawMaterialQuoted_UnitPrice'].min()
                max_price = group['RawMaterialQuoted_UnitPrice'].max()
                price_range = max_price - min_price if max_price > min_price else 1

                group['delivery_date_obj'] = pd.to_datetime(group['Delivery_Date'])
                group['days_to_delivery'] = (group['delivery_date_obj'] - pd.Timestamp(current_date)).dt.days
                min_delivery_days = group['days_to_delivery'].min()
                max_delivery_days = group['days_to_delivery'].max()
                delivery_range = max_delivery_days - min_delivery_days if max_delivery_days > min_delivery_days else 1

                for _, row in group.iterrows():
                    price_score = 10 - ((row['RawMaterialQuoted_UnitPrice'] - min_price) / price_range * 10) if price_range > 0 else 10
                    price_score = max(0, min(10, price_score))
                    delivery_date_score = 10 - ((row['days_to_delivery'] - min_delivery_days) / delivery_range * 10) if delivery_range > 0 else 10
                    delivery_date_score = max(0, min(10, delivery_date_score))
                    supplier_rating_score = row['Supplier_Rating'] * 2
                    quality_score = row['Quality_Score'] * 2
                    on_time_delivery_score = row['OnTime_Delivery_Percentage'] / 10

                    composite_score = (
                        weights['price'] * price_score +
                        weights['delivery_date'] * delivery_date_score +
                        weights['quality'] * quality_score
                    )

                    evaluation = {
                        'RawMaterial_ID': raw_material_id,
                        'RawMaterial_Name': raw_material_name,
                        'Supplier_ID': row['Supplier_ID'],
                        'Supplier_Name': row['Supplier_Name'],
                        'Purchase_Order_ID': purchase_order_id,
                        'Price_Score': round(price_score, 2),
                        'Delivery_Date_Score': round(delivery_date_score, 2),
                        'Supplier_Rating_Score': round(supplier_rating_score, 2),
                        'Quality_Score': round(quality_score, 2),
                        'OnTime_Delivery_Score': round(on_time_delivery_score, 2),
                        'Composite_Score': round(composite_score, 2),
                        'Unit_Price': row['RawMaterialQuoted_UnitPrice'],
                        'Delivery_Date': row['Delivery_Date'],
                        'Days_To_Delivery': row['days_to_delivery'],
                        'Quantity_Offered': row['RawMaterial_Quantity']
                    }
                    evaluation_results.append(evaluation)

            evaluation_df = pd.DataFrame(evaluation_results)
            evaluation_df['Rank'] = evaluation_df.groupby(['RawMaterial_ID'])['Composite_Score'].rank(ascending=False, method='min')
            evaluation_df['Selected'] = evaluation_df['Rank'] == 1
            evaluation_df.to_csv(output_path, index=False)

            summary = f"Evaluated {len(evaluation_df)} quotations across {len(grouped)} raw materials.\n\n"
            summary += f"Evaluation results saved to {output_path}\n\n"
            summary += f"Weights used: Price: {weights['price']}, Delivery Date: {weights['delivery_date']}, Quality: {weights['quality']}\n\n"

            selected_df = evaluation_df[evaluation_df['Selected']]
            summary += "Selected suppliers:\n"
            summary += selected_df[['RawMaterial_ID', 'RawMaterial_Name', 'Supplier_Name', 'Composite_Score', 'Delivery_Date', 'Purchase_Order_ID']].to_string()
            return summary
        except Exception as e:
            return f"Error evaluating suppliers: {str(e)}"

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
