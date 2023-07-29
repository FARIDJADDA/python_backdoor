from PIL import ImageGrab

screen_shot = ImageGrab.grab()
# screen_shot.show()
screen_shot.save("screen.png", "PNG")