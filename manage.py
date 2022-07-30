from app import create

app=create()


if __name__=='__main__':
    app.run(host='0.0.0.0',port=80,threaded=True)
