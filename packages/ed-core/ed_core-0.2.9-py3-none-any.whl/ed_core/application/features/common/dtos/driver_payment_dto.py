from datetime import datetime
from uuid import UUID

from ed_domain.core.entities.driver_payment import (DriverPayment,
                                                    DriverPaymentDetail,
                                                    DriverPaymentStatus)
from ed_domain.core.value_objects.money import Money
from pydantic import BaseModel


class DriverPaymentDto(BaseModel):
    id: UUID
    amount: Money
    status: DriverPaymentStatus
    date: datetime
    detail: DriverPaymentDetail

    @classmethod
    def from_driver_payment(
        cls,
        driver_payment: DriverPayment,
    ) -> "DriverPaymentDto":
        return cls(
            id=driver_payment["id"],
            amount=driver_payment["amount"],
            status=driver_payment["status"],
            date=driver_payment["date"],
            detail=driver_payment["detail"],
        )
