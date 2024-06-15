from pydantic import BaseModel, model_validator
import validators
import socket

class DomainOrIP(BaseModel):
    domain_or_ip: str
    @model_validator(mode='after')
    def validate_domain_or_ip(cls, value):
        try:
            # Check if input is IP address
            socket.inet_pton(socket.AF_INET, value.domain_or_ip)
            return value
        except socket.error:
            pass

        try:
            # Check if input is IPv6 address
            socket.inet_pton(socket.AF_INET6, value.domain_or_ip)
            return value
        except socket.error:
            pass

        try:
            # Check if input is domain name
            validators.domain(value.domain_or_ip)
            return value
        except socket.error:
            pass

        raise ValueError(f"Invalid Domain or IP.")


class ErrorResponse(BaseModel):
    error: str
    message: str