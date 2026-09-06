import re
from datetime import datetime, timezone



class InputValidator:

    @staticmethod
    def validate_name(data): #first name, last name, task name,  ....
        if not isinstance(data, str):
            raise ValueError("Input data must be a string.")
        
        data = data.strip()

        if len(data) < 2 or len(data) > 100:
            raise ValueError("Name must be between 2 and 100 characters long.")

        return data

    @staticmethod
    def validate_description(data):
        if not isinstance(data, str):
            raise ValueError("Input data must be a string.")
        
        data = data.strip()

        if len(data) > 500:
            raise ValueError("Description must be at most 500 characters long.")

        return data
        

    @staticmethod
    def validate_email(data):
        if not isinstance(data, str):
            raise ValueError("Input data must be a string.")
        
        data = data.strip()

        if len(data) < 5 or len(data) > 100:
            raise ValueError("Email must be between 5 and 100 characters long.")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", data):
            raise ValueError("Invalid email format.")

        return data

    @staticmethod
    def validate_password(password):
        if not isinstance(password, str):
            raise ValueError("Password must be a string.")

        if len(password) < 8 or len(password) > 20:
            raise ValueError("Password must be between 8 and 20 characters long.")
        
        if not re.search(r"\d", password):    #password should have at least 1 number
            raise ValueError("Password must contain at least one number, one uppercase letter, one lowercase letter, and one special character.")
        
        if not re.search(r"[A-Z]", password): #password should have at least 1 uppercase character
            raise ValueError("Password must contain at least one number, one uppercase letter, one lowercase letter, and one special character.")
        
        if not re.search(r"[a-z]", password): #password should have at least 1 lowercase character
            raise ValueError("Password must contain at least one number, one uppercase letter, one lowercase letter, and one special character.")
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-\[\]/~`+=]", password): # password should have at least 1 special character
            raise ValueError("Password must contain at least one number, one uppercase letter, one lowercase letter, and one special character.")

        return password

    @staticmethod
    def validate_difficulty(data):
        ALLOWED_DIFFICULTIES = [1, 2, 3, 4, 5]  # Assuming difficulty is rated on a scale of 1 to 5
        
        if not isinstance(data, (int, float)):
            raise ValueError("Task difficulty must be a number.")
        
        if data not in ALLOWED_DIFFICULTIES:
            raise ValueError(f"Task difficulty must be one of: {', '.join(map(str, ALLOWED_DIFFICULTIES))}")
        
        return data

    @staticmethod
    def validate_importance(data):
        ALLOWED_IMPORTANCES = [1, 2, 3, 4, 5]  # Assuming importance is rated on a scale of 1 to 5
        
        if not isinstance(data, (int, float)):
            raise ValueError("Task importance must be a number.")
        
        if data not in ALLOWED_IMPORTANCES:
            raise ValueError(f"Task importance must be one of: {', '.join(map(str, ALLOWED_IMPORTANCES))}")
        
        return data

    @staticmethod
    def validate_duration(data):
        if not isinstance(data, int):
            raise ValueError("Task duration must be an integer.")
        
        if data < 10:
            raise ValueError("Task duration must be at least 10 minutes.")
        
        return data

    @staticmethod
    def validate_deadline(data):
        if not isinstance(data, datetime):
            raise ValueError("Task deadline must be a date.")

        # Ensure the datetime is timezone-aware
        if data.tzinfo is None or data.tzinfo.utcoffset(data) is None:
            raise ValueError("Task deadline must be timezone-aware.")

        if data <= datetime.now(timezone.utc):
            raise ValueError("Task deadline must be a future date.")

        return data

    @staticmethod
    def validate_dependencies(dependencies):
        if dependencies is not None:
            if not isinstance(dependencies, list):
                raise ValueError("Dependencies must be a list.")
            for dep in dependencies:
                if not isinstance(dep, int):
                    raise ValueError("Each dependency must be an integer.")
        return dependencies or [] 

    @staticmethod
    def validate_progress(data):
        if not isinstance(data, (int, float)):
            raise ValueError("Task progress must be a number.")
        
        if data < 0 or data > 100:
            raise ValueError("Task progress must be a number between 0 and 100.")
        
        return data

    

