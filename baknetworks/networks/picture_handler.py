##picture_handler.py Networks##


# import os

# from pillow import Image

# from flask import url_for, current_app

# def add_picture(pic_upload, user_id):


#     filename = pic_upload.filename

#     ext_type = filename.split('.')[-1]

#     storage_filename = user_id+'.'+ext_type

#     filepath = os.path.join(current_app.root_path, 'static\CNN', storage_filename)

#     output_size = (200,200)

#     pic = Image.open(pic_upload)
#     pic.thumbnail(output_size)
#     pic.save(filepath)

#     return storage_filename