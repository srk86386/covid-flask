# this file will be reposnsible for storing and retriving image graphs to and from db.

def insert_image(request):
    with open(request.GET["image_name"], "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    print encoded_string
    abc=db.database_name.insert({"image":encoded_string})
    return HttpResponse("inserted")

def retrieve_image(request):
    data = db.database_name.find()
    data1 = json.loads(dumps(data))
    img = data1[0]
    img1 = img['image']
    decode=img1.decode()
    img_tag = '<img alt="sample" src="data:image/png;base64,{0}">'.format(decode)
    return HttpResponse(img_tag)

def main(db, operation='read'):
    if operation=='read':

    pass
