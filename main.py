from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Authentication setup
security = HTTPBasic()

# Hardcoded authentication details
USERNAME = "s0020316830"
PASSWORD = "Ibiz@961105"

class OrderItem(BaseModel):
    ORDER_ITM: str
    VKORG: str
    VTWEG: str
    SPART: str
    STORAGE_LOC: str
    CUST_CODE: str
    PLANT_CODE: str
    CUST_NAME: str
    CUST_ADDR1: str
    CUST_ADDR2: str
    STATE: str
    PIN_CODE: str
    TRACKING_ID: str
    MATERIAL_NO: str
    FINAL_QTY: str
    INVOICE_VALUE: str
    SGST: str
    IGST: str
    CGST: str
    MARKET_PLACE: str

class InvoiceRequest(BaseModel):
    Order: List[OrderItem]

class InvoiceCancellationItem(BaseModel):
    INVOICE_NO: str
    ORDER_ITEM: str
    MARKET_PLACE: str

class InvoiceCancellationRequest(BaseModel):
    Invoice: List[InvoiceCancellationItem]

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == USERNAME and credentials.password == PASSWORD:
        return True
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/")
def home():
    return {"message": "FastAPI is running successfully!"}

@app.post("/create-invoice")
def create_invoice(invoice: InvoiceRequest, auth: bool = Depends(authenticate)):
    num_items = len(invoice.Order)  # Count of Order Items
    return {
        "message": "Post Request received successfully!!",
        "num_of_items": num_items,
        "received_data": invoice.dict()
    }

@app.post("/cancel-invoice")
def cancel_invoice(invoice_cancellation: InvoiceCancellationRequest, auth: bool = Depends(authenticate)):
    num_items = len(invoice_cancellation.Invoice)  # Count of cancellation items
    return {
        "message": "Invoice cancellation request received successfully!",
        "num_of_items": num_items,
        "received_data": invoice_cancellation.dict()
    }
