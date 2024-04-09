from transformers import AutoModelForCausalLM, AutoTokenizer
from schema import schema
import torch

model_name = "defog/sqlcoder-7b-2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

prompt_template = f"""## Task 
Generate a SQL query to answer the following question: {{question}}

### Database Schema
This query will run on a database whose schema is represented in this string:
{schema}

### SQL
Given the database schema, here is the SQL query that answers {{question}}:
sql
"""


def generate_sql(query):
    prompt = prompt_template.format(question=query)
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids

    outputs = model.generate(input_ids, max_length=150)
    generated_sql = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return generated_sql


query = "What have I invested in, as user with id 9?"

print(generate_sql(query))
