from fastapi import FastAPI, HTTPException
from schema import Face


faces = []


app = FastAPI()


@app.post("/Looksmaxing")
def created_face(face: Face):
    
    score = (face.jawline + face.height + face.hair + face.skin) / 4

    if score < 2:
        return "sub3"
    
    elif score < 4:
        return "sub5"
    
    elif score < 5:
        return "ltn"
    
    elif score < 6:
        return "mtn"
    
    elif score < 8:
        return "htn"
    
    elif score < 10:
        return "CHAD"
    
    else:
        raise HTTPException(status_code=400, detail="Введите значение меньше 10")
    
