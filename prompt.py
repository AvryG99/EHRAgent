def generate_prompt(question, db_config):
    examples = """
    Example 1:
    Question: "What are the average blood pressure readings for patients over 60?"
    Code:
    ```
    def query_database(connection_string):
        import pyodbc

        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        query = \"""
        SELECT AVG(vitals.blood_pressure) 
        FROM vitals 
        JOIN patients ON vitals.patient_id = patients.PatientID 
        WHERE patients.age > 60
        \"""

        cursor.execute(query)
        result = cursor.fetchone()[0]
        conn.close()

        return result
    ```

    Example 2:
    Question: "List all the patients diagnosed with diabetes."
    Code:
    ```
    def query_database(connection_string):
        import pyodbc

        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        query = \"""
        SELECT patients.FirstName, patients.LastName 
        FROM patients
        JOIN PatientDiagnoses ON patients.PatientID = PatientDiagnoses.PatientID
        JOIN Diagnoses ON PatientDiagnoses.DiagnosisID = Diagnoses.DiagnosisID
        WHERE Diagnoses.DiagnosisDescription = 'Diabetes'
        \"""

        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()

        return [(row.FirstName, row.LastName) for row in result]
    ```

    Example 3:
    Question: "What are the most common side effects of prescribed medicines?"
    Code:
    ```
    def query_database(connection_string):
        import pyodbc

        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        query = \"""
        SELECT Medicines.SideEffects, COUNT(*) as count
        FROM PatientMedicines
        JOIN Medicines ON PatientMedicines.MedicineID = Medicines.MedicineID
        GROUP BY Medicines.SideEffects
        ORDER BY count DESC
        \"""

        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()

        return [(row.SideEffects, row.count) for row in result]
    ```
    """
    
    tables_info = """
    Tables:
    - Patients (PatientID, FirstName, LastName, DateOfBirth, Gender, Address, PhoneNumber)
    - Diagnoses (DiagnosisID, DiagnosisCode, DiagnosisDescription)
    - Medicines (MedicineID, MedicineName, Dosage, SideEffects)
    - PatientDiagnoses (PatientDiagnosisID, PatientID, DiagnosisID, DiagnosisDate)
    - PatientMedicines (PatientMedicineID, PatientID, MedicineID, PrescriptionDate, Dosage)
    - Doctors (DoctorID, FirstName, LastName, Specialty, PhoneNumber)
    - PatientDoctor (PatientDoctorID, PatientID, DoctorID, AssignmentDate)
    """
    
    prompt = f"""
    You are a Python programming assistant. The doctor has asked the following question:
    "{question}"
    Write a Python script to query an SQL Server database with the following details:
    {tables_info}

    The connection string is:
    server={db_config['server']};database={db_config['database']};Trusted_Connection=yes;

    Make sure to use appropriate SQL queries and handle any potential errors.

    Use the examples below as a reference, tailored to your EHR database structure:
    {examples}
    """
    return prompt
