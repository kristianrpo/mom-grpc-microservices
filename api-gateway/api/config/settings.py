import os


class Settings:
    """Application settings configuration class."""
    MOM_HOST = os.getenv("MOM_HOST", "mom-service")
    MOM_PORT = os.getenv("MOM_PORT", "50051")
    
    SERVICES = {
        "CalculatorService": {
            "host": os.getenv("CALCULATOR_HOST", "calculator-service"),
            "port": os.getenv("CALCULATOR_PORT", "50052"),
            "stub": "CalculatorStub",
            "methods": {
                "SumNumbers": {
                    "request": "SumNumbersParameters"
                }
            }
        },
    }


settings = Settings()