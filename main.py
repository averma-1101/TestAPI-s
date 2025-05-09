from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, root_validator
from typing import List, Union, Optional

app = FastAPI()

# Authentication setup
security = HTTPBasic()

# Hardcoded authentication details
USERNAME = "s0020316830"
PASSWORD = "Ibiz@961105"

# Order Item Model with type adjustments
class OrderItem(BaseModel):
    ORDER_ITM: str
    VKORG: Union[str, int]
    VTWEG: str
    SPART: Union[str, int]
    STORAGE_LOC: Union[str, int]
    CUST_CODE: Union[str, int]
    PLANT_CODE: str
    CUST_NAME: str
    CUST_ADDR1: str
    CUST_ADDR2: Optional[str]  # Make this field optional
    STATE: str
    PIN_CODE: str
    TRACKING_ID: str
    MATERIAL_NO: str
    FINAL_QTY: int
    INVOICE_VALUE: Union[str, int]
    SGST: Union[str, int]
    IGST: Union[str, int]
    CGST: Union[str, int]
    MARKET_PLACE: str

    @root_validator(pre=True)
    def convert_values(cls, values):
        """
        This validator will convert string numbers to integers and ensure that we handle both
        str and int formats properly.
        """
        for field in ['VKORG', 'SPART', 'STORAGE_LOC', 'CUST_CODE', 'INVOICE_VALUE', 'SGST', 'IGST', 'CGST']:
            value = values.get(field)
            if value is not None:
                # If value is a string representation of a number, convert it to an integer
                if isinstance(value, str) and value.isdigit():
                    values[field] = int(value)
        return values

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
