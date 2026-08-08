from pydantic import BaseModel

class PetCreate(BaseModel):
    user_id :int
    pet_name:str
    species:str
    breed:str
    gender:str
    age:int
    weight:float
    photo_url: str | None = None
    
class PetResponse(BaseModel):
    id: int
    pet_name:str
    species:str
    breed:str
    gender:str
    age:int
    weight:float
    photo_url: str | None = None
    

    class Config:
        from_attributes=True

class PetUpdate(BaseModel):
    user_id :int
    pet_name:str
    species:str
    breed:str
    gender:str
    age:int
    weight:float
    photo_url: str | None = None
   
