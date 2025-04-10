import os


class Settings:
    """Application settings configuration class."""
    MOM_HOST = os.getenv("MOM_HOST", "localhost")
    MOM_PORT = os.getenv("MOM_PORT", "50051")
    
    SERVICES = {
        "SumService": {
            "host": os.getenv("SUM_HOST", "localhost"),
            "port": os.getenv("SUM_PORT", "50052"),
            "stub": "SumServiceStub",
            "methods": {
                "SumNumbers": {
                    "request": "SumNumbersRequest"
                }
            }
        },
        "MultiplicationService": {
            "host": os.getenv("MULTIPLICATION_HOST", "localhost"),
            "port": os.getenv("MULTIPLICATION_PORT", "50053"),
            "stub": "MultiplicationServiceStub",
            "methods": {
                "MultiplyNumbers": {
                    "request": "MultiplyNumbersRequest"
                }
            }
        },
        "SubtractionService": {
            "host": os.getenv("SUBTRACTION_HOST", "localhost"),
            "port": os.getenv("SUBTRACTION_PORT", "50054"),
            "stub": "SubtractionServiceStub",
            "methods": {
                "SubtractNumbers": {
                    "request": "SubtractNumbersRequest"
                }
            }
        }
    }


settings = Settings()