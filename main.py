# import library
from fastapi import FastAPI, HTTPException, Header
import pandas as pd


#create object/instance for FastApi clas
app =FastAPI()

#create API Key
API_key = "hck024data"



#CREATE ENDPOINY home
@app.get('/')
def home():
    return {"message": "Selamat datang di Toko Pak Edi!"}

#create endpoint data
@app.get("/data")
def read_data():
    #read data from file csv
    df = pd.read_csv("Data.csv")
    #mengembalikan data
    #convert dataframe to dictionary wit orient="records" for easc row
    return df.to_dict(orient="records")

#Create endpoint data with number of parameter id
@app.get("/data/{number_id}")
def read_item(number_id:int):
    #read data from file csv
    df = pd.read_csv("Data.csv")

    #filter data by id
    filter_data = df[df["id"] == number_id]

    # check if filtered data is empty
    if len(filter_data) == 0:
        raise HTTPException(status_code=404, detail="waduh, data yang lu cari gak ada bro, maap:)")

    #convert dataframe to dicton with orient="records" each row
    return filter_data.to_dict(orient="records")


#Create endpint update file csv data
@app.put("/items/{number_id}")
def update_item(number_id:int, nama_barang:str, harga:float):
    #read data from file csv
    df = pd.read_csv("Data.csv")

    #create dataframe from updated input
    updated_df = pd.DataFrame ({
        "id": number_id, 
        "nama_barang" : nama_barang,
        "harga" : harga
        }, index=[0])
    
    #merge updated dataframe with original dataframe
    merged_df = pd.concat([df, updated_df], ignore_index=True)

    #save
    merged_df.to_csv("Data.csv", index= False)

    return{"message": f"item with ID{number_id} has been updated successfully."}
    

@app.get("/secret")
def read_secret(api_key:str = Header(None)):
    # read data from file csv
    secret_df = pd.read_csv("secret_data.csv")

    # check if api key is valid
    if api_key != API_key:
        raise HTTPException(status_code=401, detail="API Key tidak valid.")

    raise secret_df.to_dict(orient="records")





