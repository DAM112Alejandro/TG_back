from datetime import datetime,timedelta, timezone
from typing import Annotated
from bson import ObjectId
from fastapi import Depends, HTTPException, APIRouter ,status
from pydantic import BaseModel
from passlib.context import CryptContext 
from fastapi.security import HTTPBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from db.client import db


from db.models.usuario import usuario
from config import SECRET_KEY , ALGORITHM , ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter( prefix="/auth", tags=["auth"])

brcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")   

class CreateUserRequest(BaseModel):
    username: str
    email : str
    password: str
    phone: str
    

class Token(BaseModel):
    access_token: str
    token_type: str
    
class CurrentUser(BaseModel):
    id: str
    username: str
    email: str
    phone: str
    sub:str
    rol: str
    
    
def authenticateUser(email: str, password: str):
    user = db.usuario.find_one({"email": email})
    if not user:
        return False
    if not brcrypt_context.verify(password, user["contraseña"]):
        return False
    return user

def isRegistered(email: str):
    user = db.usuario.find_one({"email": email})
    if user: return False
    else: return True

def create_token(username: str, id: ObjectId, expires_delta: timedelta):
    encode  = { 'sub': username , 'id': str(id) }
    expire = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, ALGORITHM)

async def isLogged(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("id")
        if id is None:
            raise credentials_exception
        token_data = db.usuario.find_one({"_id": ObjectId(id)})
        if token_data is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return token_data

async def get_current_user(token: str = Depends(oauth2_scheme)) -> CurrentUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("id")
        if id is None:
            raise credentials_exception
        token_data = db.usuario.find_one({"_id": ObjectId(id)})
        if token_data is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return CurrentUser(id=str(token_data["_id"]), username=token_data["nombre"], email=token_data["email"],phone = token_data["telefono"], rol=getRoleById(token_data["tipo_usuario"]), sub=getSubById(token_data["tipo_sub"]))



async def isAdmin(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("id")
        if id is None:
            raise credentials_exception
        token_data = db.usuario.find_one({"_id": ObjectId(id)})
        if token_data is None:
            raise credentials_exception
        if token_data.get("tipo_usuario") != getRole("ADMIN"):
            raise credentials_exception
    except JWTError:    
        raise credentials_exception
    return token_data    


def hashPassword(password: str):
    return brcrypt_context.hash(password)

def getRole(role: str):
    found = db.tipoUsuario.find_one({"descripcion": role})
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El rol no existe")
    return str(found["_id"])

def getSub(sub:str):
    found = db.tipoSub.find_one({"descripcion": sub})
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El sub no existe")
    return str(found["_id"])

def getRoleById(id):
    found = db.tipoUsuario.find_one({"_id": ObjectId(id)})
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El rol no existe")
    return found["descripcion"]

def getSubById(id):
    found = db.tipoSub.find_one({"_id": ObjectId(id)})
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El tipo de sub no existe")
    return found["descripcion"]

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: CreateUserRequest):
    newUser =  isRegistered(user.email)
    if(not newUser):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exist")
        
    else:
        create_user = usuario(
            nombre = user.username,
            email = user.email,
            telefono = user.phone,
            contraseña =  brcrypt_context.hash(user.password),
            tipo_usuario = getRole("CLIENTE"),
            tipo_sub= getSub("ESTANDAR")
            
        )
        user_dict = create_user.model_dump()
        db.usuario.insert_one(user_dict)
        return {"success": "User created successfully"}
    
@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm ,Depends()]):
    user = authenticateUser(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
        
    token = create_token(user['email'], user['_id'] , timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES)))
    return {"success": True, "access_token": token}

@router.get("/user")
def getCurrentUser(current_user: CurrentUser = Depends(get_current_user)):
    return current_user