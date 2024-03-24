import json

# The path to your input file
input_file_path = r"C:\Users\maunu\code\bithabit_AI\src\finetuning_for_gpt3_5_turbo.jsonl"
output_file_path = r"C:\Users\maunu\code\bithabit_AI\src\test_data_for_fineTuning.jsonl"


# The system message to be included at the beginning of each conversation
system_message = {"role": "system", "content": "BitHabit is a virtual assistant created by WellPro Impact Solutions to help users develop and maintain healthy habits."}

# Open the input file and read lines
with open(input_file_path, 'r') as input_file:
    lines = input_file.readlines()

# Open the output file for writing
with open(output_file_path, 'w') as output_file:
    # Process each pair of lines
    for i in range(0, len(lines), 2):
        user_line = json.loads(lines[i].strip())
        assistant_line = json.loads(lines[i + 1].strip()) if i + 1 < len(lines) else {"role": "assistant", "content": ""}

        # Combine the system message, user line, and assistant line
        combined_message = {
            "messages": [
                system_message,
                user_line,
                assistant_line
            ]
        }
        # Write the combined message to the output file
        output_file.write(json.dumps(combined_message) + '\n')
