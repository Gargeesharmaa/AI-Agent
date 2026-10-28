from pydantic import BaseModel, Field

class Answer(BaseModel):
    answer:str = Field(description="the answer that is needed for the uer question")
    conversation:bool = Field(description="this is an indicator to know if the conversation"\
                              "should still continue or no. if the agent has made the direction about the refund this should be False"
                              "if the conversation dtill need more talf then it's True", default=True)

class PurchaseItem(BaseModel):
    name:str = Field(description="name of the item purchased")