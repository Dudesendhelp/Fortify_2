import qrcode

def generate_qr(password):
    img = qrcode.make(password)
    return img
  
if __name__=="__main__":
  img=generate_qr("hello_world")
  img.show()