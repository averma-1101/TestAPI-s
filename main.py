from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import List, Union

app = FastAPI()

# Authentication setup
security = HTTPBasic()

# Hardcoded authentication details
USERNAME = "s0020316830"
PASSWORD = "Ibiz@961105"

# Order Item Model with type adjustments
class OrderItem(BaseModel):
    ORDER_ITM: str
    VKORG: Union[str, int]  # Can be either a string or an integer
    VTWEG: str
    SPART: Union[str, int]  # Can be either a string or an integer
    STORAGE_LOC: Union[str, int]  # Can be either a string or an integer
    CUST_CODE: Union[str, int]  # Can be either a string or an integer
    PLANT_CODE: str
    CUST_NAME: str
    CUST_ADDR1: str
    CUST_ADDR2: str
    STATE: str
    PIN_CODE: str
    TRACKING_ID: str
    MATERIAL_NO: str
    FINAL_QTY: int
    INVOICE_VALUE: Union[str, int]  # Can be either a string or an integer
    SGST: Union[str, int]  # Can be either a string or an integer
    IGST: Union[str, int]  # Can be either a string or an integer
    CGST: Union[str, int]  # Can be either a string or an integer
    MARKET_PLACE: str

class InvoiceRequest(BaseModel):
    Order: List[OrderItem]

class InvoiceCancellationItem(BaseModel):
    INVOICE_NO: str  # Fixed typo
    ORDER_ITEM: str
    MARKET_PLACE: str

class InvoiceCancellationRequest(BaseModel):
    Invoice: List[InvoiceCancellationItem]

# Model for invoice returns
class InvoiceReturnItem(BaseModel):
    InvoiceNo: str
    OrderItem: str
    MaterialNo: str
    ReturnQty: int
    ProductStatus: str
    MarketPlace: str

class InvoiceReturnRequest(BaseModel):
    Invoice: List[InvoiceReturnItem]

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == USERNAME and credentials.password == PASSWORD:
        return True
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/")
def home():
    return {"message": "FastAPI is running successfully!"}

@app.post("/create-invoice")
def create_invoice(invoice: InvoiceRequest, auth: bool = Depends(authenticate)):
    num_items = len(invoice.Order)
    return {
        "message": "Post Request received successfully!!",
        "num_of_items": num_items,
        "received_data": invoice.dict()
    }

@app.post("/cancel-invoice")
def cancel_invoice(invoice_cancellation: InvoiceCancellationRequest, auth: bool = Depends(authenticate)):
    num_items = len(invoice_cancellation.Invoice)
    return {
        "message": "Invoice cancellation request received successfully!",
        "num_of_items": num_items,
        "received_data": invoice_cancellation.dict()
    }

@app.post("/return-invoice")
def return_invoice(invoice_return: InvoiceReturnRequest, auth: bool = Depends(authenticate)):
    num_items = len(invoice_return.Invoice)
    return {
        "message": "Invoice return request received successfully!",
        "num_of_items": num_items,
        "received_data": invoice_return.dict()
    }
