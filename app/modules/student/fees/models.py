from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class FeeDetail(BaseModel):
    semester: Optional[str]
    fees_to_be_collected: Optional[str]
    sponsorship_amount: Optional[str]
    scholarship_amount: Optional[str]
    refunded_amount: Optional[str]
    previously_paid: Optional[str]
    paid_amount: Optional[str]
    outstanding_amount: Optional[str]
    late_fee_outstanding: Optional[str]

class FeeTotals(BaseModel):
    total_to_be_collected: Optional[str]
    total_refunded: Optional[str]
    total_previous_paid: Optional[str]
    total_paid: Optional[str]
    total_outstanding: Optional[str]

class FeeData(BaseModel):
    fee_details: List[FeeDetail]
    totals: FeeTotals

class Receipt(BaseModel):
    sr_no: Optional[str]
    date: Optional[str]
    receipt_no: Optional[str]
    semester: Optional[str]
    payment_mode: Optional[str]
    ref_no: Optional[str]
    ref_date: Optional[str]
    ref_bank: Optional[str]
    amount: Optional[str]
    receipt_link: Optional[str]

class Transaction(BaseModel):
    sr_no: Optional[str]
    payment_date: Optional[str]
    academic_year: Optional[str]
    semester: Optional[str]
    payment_mode: Optional[str]
    total_amount: Optional[str]
    status: Optional[str]
    payment_details: Dict[str, str]

class TransactionHistory(BaseModel):
    history: List[Transaction]
    total_transaction_amount: Optional[str]

class FeeHistoryData(BaseModel):
    fee_data: FeeData
    receipts: List[Receipt]
    transactions: TransactionHistory

class FeePlanInfo(BaseModel):
    fee_plan: Optional[str]
    fees_tobe_collected: Optional[str]
    paid_amount: Optional[str]
    academic_year: Optional[str]
    scholarship_amount: Optional[str]
    refunded_amount: Optional[str]
    semester: Optional[str]
    sponsorship_amount: Optional[str]
    outstanding_amount: Optional[str]
    fee_plan_amount: Optional[str]

class FeeHead(BaseModel):
    sr_no: Optional[str]
    fee_head: Optional[str]
    currency: Optional[str]
    fee_plan_amount: Optional[str]
    fees_tobe_collected: Optional[str]
    scholarship_amount: Optional[str]
    sponsorship_amount: Optional[str]
    paid_amount: Optional[str]
    previously_paid: Optional[str]
    refunded_amount: Optional[str]
    outstanding_amount: Optional[str]

class FeePostingTotals(BaseModel):
    total_fee_plan_amount: Optional[str]
    total_fees_tobe_collected: Optional[str]
    total_scholarship_amount: Optional[str]
    total_sponsorship_amount: Optional[str]
    total_paid_amount: Optional[str]
    total_refunded_amount: Optional[str]
    total_outstanding_amount: Optional[str]

class FeePostingData(BaseModel):
    fee_plan_info: FeePlanInfo
    fee_heads: List[FeeHead]
    totals: FeePostingTotals


class PendingFeeHead(BaseModel):
    sr_no: Optional[str]
    fee_head: Optional[str]
    fees_to_be_paid: Optional[str]
    paid_amount: Optional[str]
    in_process_amount: Optional[str]
    outstanding_amount: Optional[str]

class PaymentInfo(BaseModel):
    pg_name: Optional[str]
    payment_environment: Optional[str]
    bank_account_id: Optional[str]
    semester: Optional[str]
    payment_gateway_id: Optional[str]
    payment_product_name: Optional[str]
    currency_id: Optional[str]

class PendingFeesData(BaseModel):
    semester: Optional[str]
    fee_heads: List[PendingFeeHead]
    total_fees_to_be_paid: Optional[str]
    total_paid_amount: Optional[str]
    total_in_process_amount: Optional[str]
    total_outstanding_amount: Optional[str]
    note: Optional[List[str]]
    due_date_info: Optional[str]
    payment_info: Optional[PaymentInfo]


class PaymentInitiationResponse(BaseModel):
    success: bool
    redirect_url: Optional[str]
    message: Optional[str]
