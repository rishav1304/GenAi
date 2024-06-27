from langchain_community.utilities import SQLDatabase
from transformers import AutoTokenizer, AutoModelForCausalLM

def mysqlconnect():
    return SQLDatabase.from_uri("mysql+pymysql://root:pwd@localhost/office")

def table_schema(db):
    return db.get_table_info()

def initialiseModel():
    model_name = "NumbersStation/nsql-350M"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return tokenizer, model
    
def getResponse(request):
    db = mysqlconnect()
    tokenizer, model = initialiseModel()
    tableSchema = table_schema(db)

    queryPrompt = f"""{tableSchema}

    -- Using valid SQLite, answer the following questions for the hierchical tables provided above.

    -- {request}

    SELECT"""

    input_ids = tokenizer(queryPrompt, return_tensors="pt").input_ids
    generated_ids = model.generate(input_ids, max_length=5000)

    rawQuery = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    query = 'SELECT' + rawQuery.split('SELECT')[-1]

    print("SQL Query sent by model: " + query)
    sqlResponse = db.run(query)

    responsePrompt = f"""On this table schema: {tableSchema}, This was the question asked: {request}
    I ran this sql query: {query}. I got this response from sql: {sqlResponse}. Write a response in english.
    """

    input_ids = tokenizer(responsePrompt, return_tensors="pt").input_ids
    generated_ids = model.generate(input_ids, max_length=500)

    response = tokenizer.decode(generated_ids[0], skip_special_tokens=True) 
    print("Final Response: \n" + response)
    return sqlResponse