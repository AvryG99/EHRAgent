from agent import LLM_Agent

if __name__ == "__main__":
    # Window Authentication
    db_config = {
        'server': '<Server_Name>',
        'database': '<Database_Name'
    }

    # Create the LLM Agent
    agent = LLM_Agent(db_config)

    # Example question from the doctor
    doctor_question = "What are all the dianosis of all the patients"

    # Process the question and get the answer
    answer = agent.process_question(doctor_question)
    print(answer)
